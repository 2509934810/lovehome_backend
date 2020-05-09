from . import user_bp
from flask import g, session, render_template, redirect, url_for
from flask import request
import os, random
from hashlib import md5
from backend.models import Info, db, LoveLineWorker, Service, ecomoStream
from backend.models import userperferCard, perferCard
from backend import redis_store
from datetime import datetime
import datetime as time


@user_bp.route("/service/req", methods=["GET", "POST"])
def serviceReq():
    if request.method == "POST":
        print(request.form)
        account = request.form["account"]
        username = request.form["username"]
        serviceType = request.form["serviceType"]
        photo = request.files.get("upload")
        fileend = photo.filename.split(".")[-1]
        if fileend not in ["jpg", "png", "jpeg"]:
            return redirect(url_for("user.serviceReq"))
        else:
            # add service todo
            try:
                service = Info()
                basepath = os.path.abspath(os.path.curdir)
                photopath = os.path.join(
                    basepath,
                    "backend/static/img/{}-{}.jpg".format(
                        account, random.randrange(1, 100000)
                    ),
                )
                photo.save(photopath)
                headPhotoPath = photopath.split("static/")[1]
                id = md5()
                id.update("{}{}".format(account, serviceType).encode("utf-8"))
                serviceLink = LoveLineWorker.query.filter_by(userAc=account).first().id
                service.createInfo(
                    id=id.hexdigest(),
                    head_photo=headPhotoPath,
                    serviceType=serviceType,
                    live_addr="陕西",
                    salary=200,
                    serviceLink=serviceLink,
                )
                db.session.add(service)
                db.session.commit()
            except Exception as e:
                print(e)
                return redirect(url_for("user.serviceReq"))
        return redirect(url_for("user.support"))
    else:
        user = g.user
        return render_template("user/worker/serviceReq.html", user=user)


@user_bp.route("/user/reqList")
def reqList():
    user = g.user
    services = []
    service = (
        LoveLineWorker.query.filter_by(userAc=user.account)
        .first()
        .serviceId.filter_by(access=False)
        .all()
    )
    if service:
        services.extend(service)
    return render_template("user/worker/reqlist.html", user=user, services=services)


@user_bp.route("/service/notstart")
def notStart():
    orders = []
    # try:
    user = g.user.baseuserLink.first()
    orders = user.orderLink.filter(Service.orderType < 4).all()
    # except:
    #     print("an error")
    return render_template("user/notstart.html", orders=orders)


@user_bp.route("/service/doing")
def doing():
    orders = []
    try:
        user = g.user.baseuserLink.first()
        orders = user.orderLink.filter_by(orderType=4).all()
    except:
        print("an error")
    return render_template("user/doing.html", orders=orders)


@user_bp.route("/service/order/active")
def activeOrder():
    user = g.user.baseuserLink.first()
    id = request.args.get("id")
    orderList = [order.id for order in user.orderLink.all()]
    # print(type(id), id in orderList, type(orderList[0]))
    if id not in orderList:
        # 记录安全数据库
        return redirect(url_for("auth.logout"))
    else:
        order = Service.query.filter_by(id=id).first()
        order.orderType = 4
        order.startTime = datetime.utcnow()
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("user.index"))


@user_bp.route("/service/stop", methods=["GET", "POST"])
def stop():
    if request.method == "POST":
        id = request.args.get("id")
        preferCardId = request.form["prefercard"]
        cardId = None
        if preferCardId != "no":
            cardId = preferCardId.split("_")[0]
        print(id, redis_store.get("{}_payid".format(g.user.account)))
        if id != redis_store.get("{}_payid".format(g.user.account)).decode("utf-8"):
            return redirect(url_for("auth.logout"))
        # goto 处理支付功能
        order = Service.query.filter_by(id=id).first()
        # 如果支付
        if request.form["salary"] != redis_store.get(
            "{}_pay".format(g.user.account)
        ).decode("utf-8"):
            print("支付不成功")
        # 支付后订单状态
        order.orderType = 32
        # 资金流
        econ = ecomoStream()
        md = md5()
        md.update(
            "{}{}".format(datetime.utcnow(), random.randrange(1000, 10000)).encode(
                "utf-8"
            )
        )
        # 检查是否使用优惠卡，支付逻辑
        salary = redis_store.get(f"{g.user.account}_pay")
        if salary:
            salary = int(salary.decode("utf-8"))
        else:
            return redis_store(url_for("user.doing"))
        if not cardId is None:
            card = perferCard.query.filter_by(cardId=cardId).first()
            if _check_expire(card.createTime, card.expireTime):
                usercard = card.userlink.first()
                usercard.cardType = True
                db.session.add(usercard)
                db.session.commit()
                salary = order.salary - card.cardNum
        # 添加资金流动流
        econId = md.hexdigest()
        econ.createInfo(id=econId, econNum=salary, serviceType=order.info.serviceType)
        econ.econNum = redis_store.get(f"{g.user.account}_pay").decode("utf-8")
        # econ.serviceType =
        order.salary = salary
        db.session.add(econ)
        db.session.commit()

        # 如果未支付
        # order.orderType=16
        # order.salary=0
        # formId = request.form["account"]
        return redirect(url_for("user.doing"))
    else:
        order = []
        user = g.user.baseuserLink.first()
        id = request.args.get("id")
        orderList = [order.id for order in user.orderLink.filter_by(orderType=4).all()]
        if id not in orderList:
            return redirect(url_for("auth.logout"))
        else:
            order = Service.query.filter_by(id=id).first()
            curTime = datetime.utcnow()
            print(curTime)
            startTime = order.startTime
            # print(curTime-startTime)
            serviceTime = curTime - startTime
            paySalary = _getSalary(serviceTime, order.salary)
            redis_store.setex("{}_pay".format(order.baseuser.userAc), 300, paySalary)
            redis_store.set("{}_payid".format(order.baseuser.userAc), order.id)
            cards = [
                card
                for card in user.cardLink.all()
                if card.cardType == False
                and _check_expire(
                    card.perfercard.createTime, card.perfercard.expireTime
                )
            ]
            print(cards)
            return render_template(
                "user/stop.html",
                order=order,
                serviceTime=serviceTime,
                curTime=str(curTime).split(".")[0],
                salary=paySalary,
                cards=cards,
            )


def _check_expire(createTime, expire):
    expireTime = createTime + time.timedelta(days=expire)
    if expireTime > datetime.utcnow():
        return True
    else:
        return False


def _getSalary(serviceTime, salary):
    return 3000


@user_bp.route("/service/done")
def done():
    orders = []
    try:
        user = g.user.baseuserLink.first()
        orders = user.orderLink.filter(Service.orderType > 8).all()
    except Exception as e:
        print(e)
    return render_template("user/done.html", orders=orders)
