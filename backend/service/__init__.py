from flask import Blueprint, render_template, redirect, request, jsonify
from flask import g, url_for
from backend.models import Info, LoveLineWorker, BaseUser, Service, db
from functools import wraps

service_bp = Blueprint("service", __name__, url_prefix="/service")


@service_bp.route("homeservice")
def homeservice():
    serviceAddr = request.args.get("serviceAddr")
    serviceType = Info.SERVICETYPE.get(request.args.get("serviceType"))
    if serviceType:
        services = Info.query.filter(db.and_(Info.serviceType==serviceType, Info.access==True)).all()
    else:
        services = Info.query.filter_by(access=True).all()
    # serviceAddr = Info.query.
    return render_template("service/index.html", services=services)


@service_bp.route("/req")
def req():
    id = request.args.get("id")
    service = Info.query.filter_by(id=id).first()
    user = g.user
    # print(service)
    return render_template("service/req.html", user=user, service=service)


def check_login(func):
    @wraps(func)
    def getresult(*args, **kwargs):
        user = g.user
        # print(user)
        if user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))

    return getresult


# @check_login
@service_bp.route("/confirm", methods=["GET", "POST"])
@check_login
def confirmservice():
    if request.method == "POST":
        user = g.user
        arg = request.form
        serverId = request.args.get("id")
        # print(serverId)
        UserAccount = arg.get("account")
        UserName = arg.get("username")
        UserTele = arg.get("telephone")
        UserAddr = arg.get("addr")
        SerAccount = arg.get("serAccount")
        serTime = arg.get("serTime")
        print(serTime, request.form, UserAccount)
        userId = BaseUser.query.filter_by(userAc=UserAccount).first().id
        # 服务人员Id
        serId = LoveLineWorker.query.filter_by(userAc=SerAccount).first().id
        order = Service()
        order.create(
            customerId=userId,
            providerId=serverId,
            ServiceAddr=UserAddr,
            preStartTime=serTime,
        )
        db.session.add(order)
        db.session.commit()
        return redirect(url_for("user.index"))
    else:
        id = request.args.get("id")
        if id:
            service = Info.query.filter_by(id=id).first()
            user = g.user
            return render_template(
                "user/confirmService.html", user=user, service=service
            )
        else:
            return redirect(url_for("service.req"))
