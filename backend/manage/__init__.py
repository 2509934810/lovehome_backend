from flask import Blueprint, render_template, redirect, g
from flask import session, url_for
from backend.models import User

manage_bp = Blueprint("manage", __name__, url_prefix="/manage")

# @manage_bp.route("login", method=["GET", "POST"])
# def login():
#     if POST:
#         return redirect("manage.index")
#     else:
#         return render_template('manage/login.html')

from .user import *
from .service import *
from .order import *
from .salary import *
from .Preferential import *


@manage_bp.before_request
def check_manage():
    # 从session获得用户ID
    userAc = session.get("userId")
    if userAc:
        user = User.query.filter_by(account=userAc).first()
        if user.manLink.first() or user.workerLink.first():
            g.user = user
            pass
    else:
        return redirect(url_for("auth.login"))


@manage_bp.route("/", methods=["GET"])
def index():
    user = g.user
    manUsers = []
    if user.level == 8:
        manUsers = user.workerLink.first().manworkers.all()
    elif user.level > 8:
        manUsers = user.manLink.first().manworkers.all()
        # print(manUsers)
    return render_template("manage/index.html", user=user, manUsers=manUsers)
