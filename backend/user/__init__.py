from flask import Blueprint, g, redirect, url_for, render_template, session
from backend.models import User

user_bp = Blueprint("user", __name__, url_prefix="/user")


@user_bp.before_request
def check_login():
    user = session.get("userId")
    if user:
        user = User.query.filter_by(account=user).first()
        if user:
            g.user = user
        else:
            g.user = None
            return redirect(url_for("auth.login"))
    else:
        return redirect(url_for("auth.login"))


from .service import *
from .orderque import *
from .prefer import *


@user_bp.route("/")
def index():
    user = g.user
    orders = []
    if user.level == 4:
        services = user.lineworkerLink.first().serviceId.all()
        for service in services:
            orders.extend(service.orderLink.all())
    else:
        orders.extend(user.baseuserLink.first().orderLink.all())
    return render_template("user/index.html", orders=orders)


@user_bp.route("/support")
def support():
    user = g.user
    serviceInfo = []
    serviceInfos = user.lineworkerLink.first()
    if serviceInfos:
        serviceInfo = serviceInfos.serviceId.filter_by(access=True).all()
    return render_template(
        "user/worker/support.html", serviceInfo=serviceInfo, user=user
    )
