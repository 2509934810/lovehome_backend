from flask import render_template, redirect, g
from flask import request, jsonify, url_for
from . import admin_bp
from backend import redis_store
from backend.models import User, db, perferCard, LoveManage
from hashlib import md5
from random import randrange


@admin_bp.route("/manage")
def manage():
    midMan = []
    lowMan = []
    worker = []
    lineWorker = []
    baseUser = []
    # account = request.args.get("account")
    # print(account)
    manId = request.args.get("manId")
    lowId = request.args.get("lowId")
    # print(users)
    if manId or lowId:
        if manId:
            user = User.query.filter_by(account=manId).first()
            midMan.append(user)
            # print(user)
            # 获得总监账户的职务表
            man = user.manLink.first()
            if man:
                lowWorkers = man.manworkers.all()
                if lowWorkers:
                    # 经理
                    lowMan.extend(lowWorkers)
                    for lowworker in lowWorkers:
                        lowmans = lowworker.manworkers.all()
                        if lowmans:
                            # 添加所有的员工
                            lowMan.extend(lowmans)
                            for lowman in lowmans:
                                lineworker = lowman.manworkers.all()
                                if lineworker:
                                    lineWorker.extend(lineworker)

    else:
        users = User.query.all()
        for user in users:
            if user.level == 32:
                midMan.append(user)
            elif user.level == 16:
                lowMan.append(user)
            elif user.level == 8:
                worker.append(user)
            elif user.level == 4:
                lineWorker.append(user)
            else:
                baseUser.append(user)
    print(midMan)
    return render_template(
        "admin/manage/index.html",
        midMan=midMan,
        lowMan=lowMan,
        worker=worker,
        lineWorker=lineWorker,
        baseUser=baseUser,
    )


@admin_bp.route("/manage/salary/spreadperfreCard", methods=["GET", "POST"])
def spreadperfreCard():
    # print(request.method)
    if request.method == "POST":
        id = request.form["id"]
        print(request.form)
        checkId = redis_store.get("{}_spreadCard".format(id)).decode("utf-8")
        if checkId != "True":
            return jsonify({"code": 5000})
        else:
            try:
                # print(id)
                card1 = int(request.form["card1"])
                card2 = int(request.form["card2"])
                card3 = int(request.form["card3"])
                _spreadCard(id, card1, 800)
                _spreadCard(id, card2, 500)
                _spreadCard(id, card3, 300)
            except Exception as e:
                print(e)
            return redirect(url_for("admin.getperfreCard"))

    else:
        id = request.args.get("id")
        redis_store.set("{}_spreadCard".format(id), "True", ex=30000)
        return render_template("admin/manage/spreadPreferCard.html", id=id)


def _spreadCard(id, num, money):
    if num:
        while num > 0:
            card = perferCard()
            cardId = md5()
            manId = LoveManage.query.filter(LoveManage.userAc == id).first()
            # baseUserId= User.query.filter(User.account=="111111111").first()
            # print(baseUserId)
            cardId.update(
                "{}_{}_{}".format(id, randrange(1, 1000000), num).encode("utf-8")
            )
            card.createInfo(cardId=cardId.hexdigest(), manId=manId.id, cardNum=money)
            db.session.add(card)
            num -= 1
        db.session.commit()
    else:
        pass


@admin_bp.route("/manage/salary/perfreCard")
def getperfreCard():
    # perfercard = perferCard.query.all()
    manUsers = LoveManage.query.all()
    rsp = []
    for manuser in manUsers:
        manInfo = {}
        manInfo["account"] = manuser.userAc
        manInfo["level"] = manuser.level
        # 线上
        manworkers = manuser.manworkers.all()
        manInfo["workerNum"] = len(manworkers)
        lineworkerNum = 0
        lineserverNum = 0
        try:
            for manworker in manworkers:
                lineworkers = manworker.manworkers.all()
                lineworkerNum += len(lineworkers)
                for lineworker in lineworkers:
                    lineserverNum += len(lineworker.serviceId.all())
        except Exception as e:
            print(e)
        manInfo["lineworkerNum"] = lineworkerNum
        manInfo["serviceNum"] = lineserverNum
        manInfo["cardNum"] = len(manuser.perferCardLink.all())
        manInfo["cardMNum"] = sum(
            [card.cardNum for card in manuser.perferCardLink.all()]
        )
        rsp.append(manInfo)
        # print(rsp)
    return render_template("admin/manage/perferCard.html", rsps=rsp)
