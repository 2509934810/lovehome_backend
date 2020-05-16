from flask import g, session, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from flask import jsonify, flash
import hashlib
from . import manage_bp
from backend.models import User, db, LoveWorker, LoveLineWorker
from backend.models import UserAddr
from backend.utils.generatePng import generate
# from sqlalchemy.exc import *
import random
import os
@manage_bp.route("/userInfo")
def userInfo():
    user = g.user
    return render_template("manage/user/info.html", user=user)


@manage_bp.route("/dispatchWorker")
def dispatch():
    user = g.user
    manUsers = []
    if user.level == 8:
        manUsers = user.workerLink.first().manworkers.all()
    elif user.level > 8:
        manUsers = user.manLink.first().manworkers.all()
    manUsers = [user for user in manUsers if user.user.acType == False]
    return render_template("manage/index.html", user=user, manUsers=manUsers)


@manage_bp.route("/workerInfo")
def workerInfo():
    manUsers = []
    account = request.args.get("account")
    user = User.query.filter_by(account=account).first()
    if user.level == 8:
        manUsers = user.workerLink.first().manworkers.all()
    return render_template("manage/user/workerInfo.html", user=user, manUsers=manUsers)


@manage_bp.route("/notcontro")
def userNotContro():
    user = g.user
    # 根据user mid Man 获的所有未分配的员工 目的 给他的经理分配
    # 如果是总监， 获得所有线上员工， 他管理的经理
    # 如果是经理 获得所有下线劳动人员
    # 如果是线上劳动人员， 获得他管理的线下劳动人员
    # 如果是管理员 获得所有总监 经理 员工
    # if user.level == 32:
    #     workers = User.query.filter(and_(User.level==8, User.))
    # 此处只做了线下员工的分层管理
    workersList = []
    if user.level > 8:
        Workers = User.query.filter_by(level=8).all()
        for worker in Workers:
            workerLink = worker.workerLink.first()
            # print(workerLink.manId is None)
            # 新建用户可能会导致两个数据不一致，所以目前解决一个不一致问题
            if workerLink and workerLink.manId is None:
                # print(worker)
                workersList.append(worker)
    # print(workersList)
    return render_template("manage/notControl.html", workers=workersList)


@manage_bp.route("/despread", methods=["GET"])
def despread():
    try:
        account = request.args.get("useraccount")
        user = User.query.filter_by(account=account).first()
        if g.user.level >= 16:
            if user and g.user:
                print(g.user.account)
                Link = user.workerLink.first()
                print(Link)
                Link.manId = g.user.manLink.first().id
                db.session.add(Link)
                db.session.commit()

        return jsonify({"code": 200})
    except:
        return jsonify({"code": 501})


@manage_bp.route("/user/add", methods=["GET", "POST"])
def addUser():
    if request.method == "POST":
        try:
            account = request.form["account"]
            username = request.form["username"]
            password = request.form["password"]
            level = request.form["level"]
            if level == "MANAGE_LOW":
                user = User()
                user.createUser(
                    account=account,
                    password=generate_password_hash(password),
                    role=level,
                    username=username,
                )
                db.session.add(user)
                db.session.commit()
                sha = hashlib.md5()
                sha.update(account.encode("utf-8"))
                loveworker = LoveWorker()
                loveworker.id = sha.hexdigest()
                loveworker.level = 8
                loveworker.manId = g.user.manLink.first().id
                loveworker.userAc = account
                db.session.add(loveworker)
                db.session.commit()
        except Exception as e:
            flash("用户已存在")
        return redirect(url_for("manage.index"))
    else:
        user = g.user
        return render_template("manage/user/add.html", user=user)


@manage_bp.route("/deleteRel")
def deleteRel():
    # 针对经理
    if g.user.level == 16:
        account = request.args.get("useraccount")
        if account:
            print(account)
            user = User.query.filter_by(account=account).first()
            if user:
                Link = user.workerLink.first()
                Link.manId = None
                print(user, Link.manId)
                db.session.add(Link)
                db.session.commit()
                return jsonify({"code": 200})
    return jsonify({"code": 500})


@manage_bp.route("/user/actived", methods=["GET", "POST"])
def activedUser():
    user = g.user
    if request.method == "POST":
        formdata = request.form
        print(formdata)
        username = formdata["username"]
        sex = formdata["sex"]
        age = formdata["age"]
        addr = formdata["province"] +"  " + formdata["city"]
        tele = formdata["telephone"]
        email = formdata["email"]
        # 验证效验码
        photo = request.files.get("upload")
        fileend = photo.filename.split(".")[-1]
        if fileend not in ["jpg", "png", "jpeg"]:
            return redirect(url_for("user.serviceReq"))
        try:
            if username and sex and age and addr and tele and email:
                buser = User.query.filter_by(account=user.account).first()
                buser.username = username
                buser.sex = User.SEX.get(sex, None)
                # buser.addr = addr
                buser.telephone = tele
                buser.email = email
                buser.age=age
                # 检查是否可以激活
                buser.addr = addr
                buser.actived = True
                # buser.confirmCode
                basepath = os.path.abspath(os.path.curdir)
                photopath = os.path.join(
                    basepath,
                    "backend/static/img/{}-{}.jpg".format(
                        user.account, random.randrange(1, 100000)
                    ),
                )
                photo.save(photopath)
                rsp = generate(photopath)
                print(rsp)
                if rsp.get("code")== 200:
                    headPhotoPath=rsp.get("path")
                    os.remove(photopath)
                else:
                    return jsonify({"code": 500})
                buser.head_photo=headPhotoPath
                db.session.add(buser)
                db.session.commit()
        except Exception as e:
            print(e)
            return redirect(url_for("manage.userInfo"))
        finally:
            return redirect(url_for("manage.userInfo"))
    else:
        province = list(set([addr.province for addr in UserAddr.query.all()]))
        return render_template("manage/user/actived.html", user=user, provinces=province)


@manage_bp.route("/api/<province>")
def getcity(province):
    print(type(province))
    citys = [city.city for city in UserAddr.query.filter_by(province=province).all()]
    return jsonify({"code": 200, "citys": citys})