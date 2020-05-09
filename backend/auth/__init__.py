from flask import Blueprint, render_template, redirect
from flask import request, session, url_for, g
from flask import flash
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import User, BaseUser, db

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            account = request.form["account"]
            username = request.form["username"]
            password = request.form["password"]
            user = User()
            user.createUser(
                account=account,
                password=generate_password_hash(password),
                role="USER_LOW",
                username=username,
            )
            db.session.add(user)
            db.session.commit()
            baseLink = BaseUser()
            baseLink.createInfo(level=1, userAc=account)
            db.session.add(baseLink)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("注册失败")
            return redirect(url_for("auth.register"))
        return redirect(url_for("auth.login"))
    else:
        return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        account = request.form["account"]
        password = request.form["password"]
        print(account, password)
        user = User.query.filter_by(account=account).first()
        print(user)
        if user:
            print(user.password, password)
            print(check_password_hash(user.password, password))
            if check_password_hash(user.password, password):
                session["userId"] = user.account
                g.user = user
                return redirect(url_for("index"))
        else:
            return redirect(url_for("auth.login"))
    return render_template("auth/login.html")


@auth_bp.route("/logout")
def logout():
    user = session.get("userId")
    if user:
        session.clear()
    return redirect(url_for("index"))
