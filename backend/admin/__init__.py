from flask import render_template, g, Blueprint, jsonify, request, redirect, url_for
from flask import session
from backend.models import User, db
from flask_sqlalchemy import sqlalchemy
import math
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

from .userCrud import *
from .userMan import *
from .manage import *
from .order import *
from .salary import *


@admin_bp.before_request
def check_login():
    userId = session["userId"]
    user = User.query.filter_by(account=userId).first()
    if user and user.level == 64:
        pass
    else:
        session.clear()
        return redirect(url_for("auth.login"))


@admin_bp.route("/")
def indexs():
    return jsonify({"code": "200"})


@admin_bp.route("/login", methods=["GET"])
def login():
    return render_template("admin/login.html")


@admin_bp.route("/index")
def index():
    pageNum = request.args.get("pageNum")
    if pageNum:
        pageNum = int(pageNum)
    else:
        pageNum = 1
    allUser = User.query.all()
    allPage = math.ceil(len(allUser)/10)
    print(allPage, pageNum)
    user = allUser[(pageNum-1)*10:pageNum*10]
    if user:
        return render_template("admin/index.html",users=user,pageNum=pageNum, allPage = allPage)
    else:
        return render_template("admin/index.html")


@admin_bp.route("/logout")
def logout():
    user = session.get("userId")
    if user:
        session.clear()
    return redirect(url_for("index"))
