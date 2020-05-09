from . import admin_bp
from flask import flash
from flask import render_template, redirect, g, request, url_for
from flask_sqlalchemy import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models import User, db, LoveManage, LoveWorker, LoveLineWorker, BaseUser
from hashlib import md5


@admin_bp.route("/user/add", methods=["GET", "POST"])
def addUser():
    if request.method == "POST":
        account = request.form["account"]
        username = request.form["username"]
        password = request.form["password"]
        level = request.form["level"]
        print(level)
        if account and username and password and level:
            try:
                user = User()
                user.createUser(
                    account=account,
                    password=generate_password_hash(password),
                    role=level,
                    username=username,
                )
                db.session.add(user)
                # db.session.commit()
                levelNum = User.LEVEL.get(level)
                print(levelNum, type(levelNum))
                if levelNum > 8:
                    loveman = LoveManage()
                    loveman.userAc = account
                    loveman.level = User.LEVEL.get(level)
                    md = md5()
                    md.update(f"{account}".encode("utf-8"))
                    loveman.id = md.hexdigest()
                    db.session.add(loveman)
                    db.session.commit()
                elif levelNum == 8:
                    loveworker = LoveWorker()
                    loveworker.userAc = account
                    loveworker.level = User.LEVEL.get(level)
                    md = md5()
                    md.update(f"{account}".encode("utf-8"))
                    loveworker.id = md.hexdigest()
                    db.session.add(loveworker)
                    db.session.commit()
                elif levelNum == 4:
                    lineWorker = LoveLineWorker()
                    md = md5()
                    md.update(f"{account}".encode("utf-8"))
                    lineWorker.id = md.hexdigest()
                    lineWorker.level = User.LEVEL.get(level)
                    lineWorker.userAc = account
                    db.session.add(lineWorker)
                    db.session.commit()
                else:
                    baseuser = BaseUser()
                    baseuser.userAc = account
                    baseuser.level = User.LEVEL.get(level)
                    md = md5()
                    md.update(f"{account}".encode("utf-8"))
                    baseuser.id = md.hexdigest()
                    db.session.add(baseuser)
                    db.session.commit()
            except sqlalchemy.exc.IntegrityError:
                flash("添加失败")
                return redirect(url_for("admin.index"))
        return redirect(url_for("admin.index"))
    else:
        return render_template("admin/user/add.html")


@admin_bp.route("/user/delete", methods=["POST", "GET"])
def deleteUser():
    if request.method == "GET":
        deleteIdStr = request.args.get("IdList")
        if deleteIdStr:
            deleteIdList = [id for id in deleteIdStr.split(",")]
            # print(deleteId, type(deleteId))
            for deleteId in deleteIdList:
                user = User.query.filter_by(account=deleteId).first()
                if user is None:
                    continue
                db.session.delete(user)
            db.session.commit()
            return redirect(url_for("admin.index"))
        else:
            return redirect(url_for("admin.index"))
    else:
        return redirect(url_for("admin.index"))


@admin_bp.route("/user/select", methods=["GET"])
def selectUser():
    seAccount = request.args.get("account")
    userType = request.args.get("userType")
    actived = request.args.get("actived")
    if seAccount or userType or actived:
        if seAccount:
            user = User.query.filter_by(account=seAccount).all()
            return render_template("admin/index.html", users=user)
        if userType:
            user = User.query.filter_by(level=User.LEVEL.get(userType)).all()
            return render_template("admin/index.html", users=user)
        if actived:
            actived = True if actived == "True" else False
            print(actived, type(actived))
            user = User.query.filter_by(actived=actived).all()
            return render_template("admin/index.html", users=user)
        else:
            pass
    else:
        return redirect(url_for("admin.index"))


@admin_bp.route("/user/change", methods=["GET", "POST"])
def changeInfo():
    if request.method == "POST":
        account = request.form["account"]
        password = request.form["password"]
        username = request.form["username"]
        level = request.form["level"]
        print(account, password, username, level)
        user = User.query.filter_by(account=account).first()
        if user:
            if account or password or level or username:
                user.account = account
                user.username = username
                user.level = User.LEVEL.get(level, 1)
                user.password = generate_password_hash(password)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for("admin.selectUser", account=account))
            else:
                return redirect(url_for("admin.index"))
        else:
            return redirect(url_for("admin.index"))
    else:
        account = request.args.get("account")
        user = User.query.filter_by(account=account).first()
        if user:
            return render_template("admin/user/change.html", user=user)
        else:
            return redirect(url_for("admin.index"))
