from . import manage_bp
from flask import render_template, g, redirect, request, url_for
from backend.models import User, LoveLineWorker, LoveManage, db, Info
from backend.models import Service


@manage_bp.route("/service/")
def service():
    lineworkers = []
    workers = []
    try:
        user = g.user
        worker = user.manLink.first()
        if worker:
            workers = worker.manworkers.all()
        for worker in workers:
            lineworkers.extend(worker.manworkers.all())
    except Exception as e:
        print(e)
    return render_template(
        "manage/service/index.html", workers=workers, lineworkers=lineworkers
    )


@manage_bp.route("/service/lineNotControl")
def lineNotControl():
    lineWorkers = []
    workers = LoveLineWorker.query.filter_by(manId=None).all()
    return render_template("manage/service/lineNotControl.html", workers=workers)


@manage_bp.route("/service/line/despread/<account>", methods=["GET", "POST"])
def lineDespread(account):
    if request.method == "POST":
        accounts = request.form["account"]
        manAcoount = request.form["level"]
        # print(accounts, manAcoount, request.form)
        user = LoveLineWorker.query.filter_by(userAc=accounts).first()
        print(user)
        user.manId = manAcoount
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("manage.lineNotControl"))
    else:
        accounts = account.split(",")
        # print(accounts)
        user = g.user
        manworkers = (
            LoveManage.query.filter_by(userAc=user.account).first().manworkers.all()
        )
        # print(manworkers)
        return render_template(
            "manage/service/lineDespread.html", manworkers=manworkers, accounts=accounts
        )


# 后台管理
@manage_bp.route("/service/req")
def serviceReq():
    user = g.user
    serviceReqList = []
    # 仅仅只对普通后台管理生效
    workers = user.workerLink.first().manworkers.all()
    # print(workers)
    for worker in workers:
        # serviceInfo = worker.serviceId.filter_by(access=False).all()
        serviceInfo = worker.serviceId.all()
        # print(serviceInfo)
        serviceReqList.extend(serviceInfo)
    print(serviceReqList)
    # print(serviceReqList)
    return render_template("manage/service/req.html", serviceReqList=serviceReqList)


@manage_bp.route("/service/actived", methods=["GET"])
def actived():
    try:
        id = request.args.get("id")
        service = Info.query.filter_by(id=id).first()
        service.access = True
        db.session.add(service)
        db.session.commit()
    except:
        return redirect(url_for("manage.serviceReq"))
    return redirect(url_for("manage.serviceReq"))

    # return render_template('manage/service/req.html')


@manage_bp.route("/service/order/active")
def activeOrder():
    try:
        orderId = request.args.get("id")
        order = Service.query.filter_by(id=orderId).first()
        order.orderType = 2
        order.info.lovelineworker.user.acType = True
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        print(e)
        return redirect(url_for("manage.notSolve"))
    return redirect(url_for("manage.order"))


@manage_bp.route("/order")
def order():
    orders = []
    user = g.user
    workers = []
    if user.level > 8 and user.level < 64:
        try:
            Workers = user.manLink.first().manworkers.all()
            linewokersList = []
            for worker in Workers:
                linewokersList.extend(worker.manworkers.all())
            for lineworker in linewokersList:
                orderList = [
                    serviceId.orderLink.all()
                    for serviceId in lineworker.serviceId.all()
                    if serviceId.orderLink
                ]
                for order in orderList:
                    orders.extend(order)
        except Exception as e:
            print(e)
        return render_template("manage/order/index.html", orders=orders)
    try:
        workers = g.user.workerLink.first().manworkers.all()
    except:
        print("error")
    for worker in workers:
        for service in worker.serviceId.all():
            orders.extend(service.orderLink.all())
    return render_template("manage/order/index.html", orders=orders)


# 解决获得他管理的员工的未处理订单
@manage_bp.route("/service/order/notsolve")
def notSolve():
    orders = []
    workers = []
    try:
        if g.user.level == 8:
            workers = g.user.workerLink.first().manworkers.all()
        elif g.user.level > 8 and g.user.level < 64:
            for worker in g.user.manLink.first().manworkers.all():
                workers.extend(worker.manworkers.all())
            print(workers)
    except Exception as e:
        print(e)
        print(g.user)
        print("error")
    for worker in workers:
        for service in worker.serviceId.all():
            orders.extend(service.orderLink.filter_by(orderType=1).all())
    return render_template("manage/order/notsolve.html", orders=orders)


@manage_bp.route("/show")
def show():
    user = g.user
    if user.level > 8:
        workersList = []
        workersList = (
            User.query.filter_by(account=user.account)
            .first()
            .manLink.first()
            .manworkers.all()
        )
        print(workersList)
        lineworkerList = [
            worker.manworkers.all() for worker in workersList if worker.manworkers.all()
        ]
        hourList = []
        # print(lineworkerList, workersList)
        return render_template(
            "manage/show.html", workersList=workersList, lineworkerList=lineworkerList
        )
