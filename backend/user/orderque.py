from . import user_bp
from flask import request, redirect, render_template, url_for
from flask import g, jsonify
from backend import redis_store
from backend.models import User, db, Service, orderReq, LoveLineWorker, quickOrder
from backend.models import quickOrder, BaseUser
from sqlalchemy import or_
from hashlib import md5
from datetime import datetime


@user_bp.route("/order/question", methods=["GET", "POST"])
def orderque():
    if request.method == "POST":
        id = request.args.get("id")
        id2 = request.form["orderId"]
        orderType = request.form["orderType"]
        account = request.form["account"]
        orderBody = request.form["orderBody"]
        order = Service.query.filter_by(id=id).first()
        if id != id2 or order is None:
            return jsonify({"code": 500})
        # Store in db
        orderreq = orderReq()
        orderreq.create(orderId=id, reqBody=orderBody)
        db.session.add(orderreq)
        db.session.commit()
        return redirect(url_for("user.index"))
    else:
        id = request.args.get("id")
        user = g.user
        # redis_store.set("")
        # orderList = [order for order in user.baseuser.orderLink.all()]
        # orderIdList = [ order.id for order in  orderList]
        order = user.baseuserLink.first().orderLink.filter_by(id=id).first()
        if order is None:
            # 记载安全数据库
            return redirect(url_for("auth.logout"))
        return render_template("user/orderque.html", order=order)


@user_bp.route("/user/orderReq")
def reqLists():
    user = g.user
    reqlist = []
    if user.level < 4:
        try:
            orderlist = user.baseuserLink.first().orderLink.all()
            for order in orderlist:
                if order.orderReq.first():
                    reqlist.append(order.orderReq.first())
        except Exception as e:
            print(e)
    return render_template("orderreq/index.html", reqlist=reqlist)


@user_bp.route("/worker/order/doing")
def workerDoing():
    user = g.user
    orders = []
    services = (
        LoveLineWorker.query.filter_by(userAc=user.account).first().serviceId.all()
    )
    for service in services:
        orders = [
            order for order in service.orderLink.filter_by(orderType=4).all() if order
        ]
    print(orders)
    return render_template("user/worker/orderdoing.html", orders=orders)
    # return jsonify({"code": 200})


@user_bp.route("/worker/order/done")
def workerDone():
    user = g.user
    services = (
        LoveLineWorker.query.filter_by(userAc=user.account).first().serviceId.all()
    )
    for service in services:
        orders = [
            order
            for order in service.orderLink.filter(
                or_(Service.orderType == 16, Service.orderType == 32)
            ).all()
            if order
        ]
    print(orders)
    return render_template("user/worker/orderdone.html", orders=orders)


@user_bp.route("/quickOrder", methods=["GET", "POST"])
def quickO():
    if request.method == "POST":
        print(request.form)
        serviceType = request.form["serviceType"]
        preStartTime = request.form["preStartTime"]
        sex = request.form["sex"]
        age = request.form["age"]
        user = g.user
        Id = md5()
        Id.update("{}_tmp{}".format(user.account, datetime.now()).encode("utf-8"))
        qorder = quickOrder()
        # print(user.baseuserLink.all())
        print(BaseUser.query.filter(BaseUser.userAc==user.account).all())
        qorder.createInfo(
            Id=Id.hexdigest(),
            userLink=user.baseuserLink.first().id,
            serviceType=serviceType,
            preStartTime=preStartTime,
            age=age,
            sex=sex,
            addr="shanxi1",
        )
        db.session.add(qorder)
        db.session.commit()
        return redirect(url_for("user.index"))
    else:
        user = g.user
        if user:
            return render_template("orderreq/quickOrder.html")
        else:
            return redirect(url_for("auth.login"))


@user_bp.route("/tmpOrder")
def tmpOrder():
    user = g.user
    if user:
        orders = (
            user.baseuserLink.first().quickorder.filter(quickOrder.quickType < 4).all()
        )
        print(orders)
        return render_template("user/tmpOrder.html", orders=orders)
