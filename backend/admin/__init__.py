from flask import render_template, g, Blueprint, jsonify, request, redirect, url_for
from flask import session
from backend.models import User, db
from flask_sqlalchemy import sqlalchemy

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
    user = User.query.all()
    # print(user)
    if user:
        print(user)
        return render_template("admin/index.html", users=user)
    else:
        return render_template("admin/index.html")


@admin_bp.route("/logout")
def logout():
    user = session.get("userId")
    if user:
        session.clear()
    return redirect(url_for("index"))
