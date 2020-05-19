from backend.admin import admin_bp
from flask import g, render_template, redirect, url_for, request
from flask import flash, jsonify
from backend.models import ecomoStream, db, LoveManage, User, SalaryStand
from backend.models import salaryeCon, ecomoStream
import datetime, math, os
from backend import redis_store
from hashlib import md5
from backend.utils.generateEcon import PDFGenerator
from backend.utils.generatePng import generatepdf
from sqlalchemy import and_

TIME = {
    "11111111111111111111": 1,
    "222222222222222222222": 2,
    "3333333333333333333333": 3,
    "4444444444444444444444": 4,
}

IoSalaryType = {"True": True, "False": False}

# def require_route(func):
#     def wrapper(*args, **kwargs):
#         id = request.args.get("id")
#         print(id)
#         if id and id == redis_store.get("order_id"):
#             # flash("页面失效")
#             return redirect(url_for('admin.index'))
#         else:
#             return func(*args, **kwargs)
#     return wrapper


@admin_bp.before_request
def check_spread():
    if request.path == url_for("admin.spreadSalary"):
        id = request.args.get("id")
        # print(id, redis_store.get("spreadId"))
        if id and id == redis_store.get("spreadId").decode("utf-8"):
            # 发放工资
            return redirect(url_for("admin.index"))


@admin_bp.route("/manage/salary/spread", methods=["GET", "POST"])
def spreadSalary():
    if request.method == "POST":
        rst = {"code": 200}
        curDate = datetime.datetime.utcnow().strftime("%Y-%m")
        for man in LoveManage.query.all():
            _sendSalary(man.user)
            _savespreadLog(man.user)
            for worker in man.manworkers.all():
                _sendSalary(worker.user)
                _savespreadLog(worker.user)
                for lineworker in worker.manworkers.all():
                    _sendSalary(lineworker.user)
                    _savespreadLog(lineworker.user)
        return jsonify(rst)
    else:
        lineworkerNum = 0
        workerNum = 0
        manNum = 0
        econResult = []
        manUser = LoveManage.query.all()
        for man in manUser:
            manNum += 1
            team = {}
            team["name"] = man.user.username
            team["leader"] = man.user.account
            loveworker = man.manworkers.all()
            workerNum += len(loveworker)
            lineworker = []
            for worker in loveworker:
                manworkers = worker.manworkers.all()
                if manworkers:
                    lineworkerNum += 1
                    lineworker.extend(manworkers)
            team["num"] = len(loveworker) + len(lineworker)
            orderNum = 0
            # serviceIds = [for worker in lineworker]
            serviceList = []
            for worker in lineworker:
                serviceIds = worker.serviceId.all()
                if serviceIds:
                    serviceList.extend(serviceIds)
            for serviceId in serviceList:
                orders = serviceId.orderLink.all()
                if orders:
                    orderNum += len(orders)
            team["orderNum"] = orderNum
            # com salary
            team["salary"] = _comSalary(man)
            econResult.append(team)
        spreadId = md5()
        spreadId.update("{}".format(datetime.datetime.utcnow()).encode("utf-8"))
        redis_store.set("spreadId", spreadId.hexdigest(), ex=3000)
        flag = _checkSalary()
        salary = 0
        if flag == True:
            curMonth = datetime.datetime.utcnow().strftime("%Y-%m")
            salary = _sumSalary(curMonth)
        print(flag)
        return render_template(
            "admin/manage/spreadSalary.html",
            econResult=econResult,
            lineworkerNum=lineworkerNum,
            workerNum=workerNum,
            manNum=manNum,
            spreadId=spreadId.hexdigest(),
            time=datetime.datetime.utcnow(),
            flag=flag,
            salary=salary,
        )


def _sumSalary(month):
    econ = sum(
        [
            econ.salaryNum
            for econ in salaryeCon.query.filter(salaryeCon.salaryMonth == month).all()
        ]
    )
    return econ


def _checkSalary():
    curMonth = datetime.datetime.utcnow().strftime("%Y-%m")
    flag = True
    users = User.query.filter(and_(User.level > 2, User.level < 64)).all()
    for user in users:
        if user.salaryeconLink.filter(salaryeCon.salaryMonth == curMonth).first():
            pass
        else:
            flag = False
    return flag


def _sendSalary(user):
    curMonth = datetime.datetime.utcnow().strftime("%Y-%m")
    curmonthSalary = user.salaryeconLink.filter(
        salaryeCon.salaryMonth == curMonth
    ).all()
    if curmonthSalary:
        pass
    else:
        salaryecon = salaryeCon()
        salaryecon.userId = user.account
        salaryecon.salaryNum = user.salaryStandLink.first().salaryNum
        salaryecon.salaryMonth = curMonth
        db.session.add(salaryecon)
        db.session.commit()


def _savespreadLog(user):
    id = md5()
    id.update("{}_{}".format("salary", datetime.datetime.utcnow()).encode("utf-8"))
    econ = ecomoStream()
    econ.id = id.hexdigest()
    econ.econNum = user.salaryStandLink.first().salaryNum
    econ.econType = False
    econ.serviceType = 8
    econ.streamType = 2
    db.session.add(econ)
    db.session.commit()


def _comSalary(man):
    salary = 0
    salary += man.user.salaryStandLink.first().salaryNum
    for worker in man.manworkers.all():
        salary += worker.user.salaryStandLink.first().salaryNum
    return salary


# todo add filter info to frontend
@admin_bp.route("/manage/salary")
def salary():
    user = g.user
    # streams = ecomoStream.query.filter_by()
    inSalary = 0
    outSalary = 0
    sumSalary = 0
    timerange = request.args.get("timerange")
    ioSalary = request.args.get("iosalary")
    econstreams, insalary, outsalary, sumsalary = getSalaryInfo(timerange, ioSalary)
    print(econstreams, insalary, outsalary, sumsalary)
    return render_template(
        "admin/manage/salary.html",
        econstreams=econstreams,
        insalary=insalary,
        outsalary=outsalary,
        sumsalary=sumsalary,
    )


def getSalaryInfo(timeRange, ioSalary):
    if timeRange and ioSalary:
        if TIME.get(timeRange) in [1, 2, 3, 4]:
            econstreams, insalary, outsalary, sumsalary = getInfoFromdate(
                TIME.get(timeRange), ioSalary
            )
        else:
            econstreams, insalary, outsalary, sumsalary = None, None, None, None
    elif timeRange:
        econstreams, insalary, outsalary, sumsalary = getInfoFromdate(timeRange, "True")
    elif ioSalary:
        econstreams, insalary, outsalary, sumsalary = getInfoFromdate(1, ioSalary)
    else:
        econstreams, insalary, outsalary, sumsalary = getInfoFromdate(1, "True")
    return econstreams, insalary, outsalary, sumsalary


def getInfoFromdate(timeInfo, ioSalary):
    time_format = "%Y-%m-01"
    if timeInfo == 1:
        curMouth = datetime.datetime.utcnow().strftime(time_format)
    elif timeInfo == 2:
        curMouth = (datetime.datetime.utcnow() - datetime.timedelta(weeks=12)).strftime(
            time_format
        )
    elif timeInfo == 3:
        curMouth = (datetime.datetime.utcnow() - datetime.timedelta(weeks=56)).strftime(
            time_format
        )
    elif timeInfo == 4:
        curMouth = (
            datetime.datetime.utcnow() - datetime.timedelta(weeks=118)
        ).strftime(time_format)
    else:
        curMouth = datetime.datetime.utcnow().strftime(time_format)
    # 获取所有的最进一个月的
    econstreams = ecomoStream.query.filter(
        db.and_(
            ecomoStream.createTime > curMouth,
            ecomoStream.econType == IoSalaryType.get(ioSalary, True),
        )
    ).all()
    inSalary = sum(
        [
            econ.econNum
            for econ in ecomoStream.query.filter(
                db.and_(ecomoStream.createTime > curMouth, ecomoStream.econType == True)
            ).all()
        ]
    )
    # print(inSalary)
    outSalary = sum(
        [
            econ.econNum
            for econ in ecomoStream.query.filter(
                db.and_(
                    ecomoStream.createTime > curMouth, ecomoStream.econType == False
                )
            ).all()
        ]
    )
    sumSalary = sum(
        [
            econ.econNum
            for econ in ecomoStream.query.filter(
                ecomoStream.createTime > curMouth
            ).all()
        ]
    )
    return econstreams, inSalary, outSalary, sumSalary


@admin_bp.route("/manage/salary/manage")
def manageSalary():
    users = User.query.filter(User.level > 2).all()
    salaryList = [info.salaryNum for info in SalaryStand.query.all()]
    infoNum = len(salaryList)
    if infoNum == 0:
        infoNum = 1
    print(sum(salaryList), infoNum)
    avgSalary = round(sum(salaryList) / infoNum)
    return render_template(
        "admin/manage/salaryStand.html", users=users, avgSalary=avgSalary
    )


@admin_bp.route("/manage/salary/set/", methods=["GET", "POST"])
def setSalary():
    if request.method == "POST":
        print(request.form)
        level = request.form["levelType"]
        salaryNum = request.form["salaryNum"]
        print(level, salaryNum)
        if level and salaryNum:
            try:
                if level == "128":
                    for user in User.query.filter(User.level > 2).all():
                        if user.salaryStandLink.first():
                            salaryStand = user.salaryStandLink.first()
                            print("1")
                        else:
                            salaryStand = SalaryStand()
                            print(2)
                        salaryStand.salaryNum = salaryNum
                        salaryStand.userId = user.account
                        db.session.add(salaryStand)
                    db.session.commit()
                else:
                    for user in User.query.filter(User.level == level).all():
                        if user.salaryStandLink.first():
                            salaryStand = user.salaryStandLink.first()
                        else:
                            salaryStand = SalaryStand()
                        salaryStand.salaryNum = salaryNum
                        salaryStand.userId = user.account
                        db.session.add(salaryStand)
                    db.session.commit()
            except Exception as e:
                print(e)
                pass
        else:
            flash("请输入完整数据")
            print("error")
        return redirect(url_for("admin.manageSalary"))
    else:
        # if id:
        #     user = User.query.filter(User.account=id).first()
        #     # salaryStand = user.salaryStandLink.first()
        #     # if salaryStand:
        #     return render_template("admin/manage/setSalary.html")
        return render_template("admin/manage/setSalary.html")


@admin_bp.route("/manage/salary/set/<id>", methods=["GET", "POST"])
def setSalarys(id):
    if request.method == "POST":
        account = request.form["account"]
        # print(request.form)
        salaryNum = request.form["salaryNum"]
        tag = redis_store.get("salaryset_{}".format(id))
        # print(tag)
        assert account == id
        if tag:
            user = User.query.filter(User.account == id).first()
            salaryStandLink = user.salaryStandLink.first()
            if salaryStandLink:
                salaryStandLink.salaryNum = salaryNum
                salaryStandLink.userId = id
            else:
                salaryStandLink = SalaryStand()
                salaryStandLink.salaryNum = salaryNum
                salaryStandLink.userId = id
            db.session.add(salaryStandLink)
            db.session.commit()
        return redirect(url_for("admin.manageSalary"))
        # if id:
        #     user = User.query.filter(User.account=id).first()
        #     salaryInfo = user.salaryStandLink.first()
        #     if salaryInfo:
        #         salaryInfo.salaryNum =
        pass
    else:
        user = User.query.filter(User.account == id).first()
        if user:
            redis_store.set("salaryset_{}".format(user.account), "tag", ex=30000)
            return render_template("admin/manage/setSalary2.html", user=user)


@admin_bp.route("/manage/salary/print")
def printsalary():
    curmonth = datetime.datetime.utcnow().strftime("%Y-%m-01")
    econstream = ecomoStream.query.filter(ecomoStream.createTime > curmonth).all()
    print(econstream)
    econs = {}
    econs["inCon"] = sum(
        [econ.econNum for econ in econstream if econ.econType == False]
    )
    econs["outCon"] = sum(
        [econ.econNum for econ in econstream if econ.econType == True]
    )
    econs["salary"] = sum(
        [econ.econNum for econ in econstream if econ.serviceType == 4]
    )
    # order
    filename = "econ" + datetime.datetime.utcnow().strftime("%Y-%m-%d %H-%M-%S")
    econs["filename"] = filename
    basepath = os.path.abspath(os.path.curdir)
    filepath = os.path.join(
        basepath,
        "backend/static/img/admin/econstream/{}/".format(
            datetime.datetime.utcnow().strftime("%Y-%m-01")
        ),
    )
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    doc = PDFGenerator(filename=filename, filepath=filepath)
    doc.genTaskPDF(econs)
    filePath = os.path.join(filepath, "{}.pdf".format(filename))
    rsp = generatepdf(filePath).get("path")
    print(filePath, rsp)
    os.remove(filePath)
    pdfLink = "http://" + os.getenv("AVATOR_SERVER") + "/" + rsp
    return jsonify({"code": 200, "data": pdfLink})
