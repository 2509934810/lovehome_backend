from flask import render_template, redirect, url_for
from flask import request, g, jsonify
from . import manage_bp
from backend.models import quickOrder, db, Service, orderResult
from backend.utils.generateOrder import PDFGenerator
from backend.utils.generatePng import generatepdf
from hashlib import md5
import os, datetime


@manage_bp.route("/quickOrder")
def quickorder():
    orders = quickOrder.query.filter(quickOrder.quickType < 4)
    return render_template("manage/order/quickOrder.html", orders=orders)


@manage_bp.route("/spreadquick")
def spreadquick():
    if request.method == "POST":
        pass
    else:
        serviceList = []
        qorder = []
        user = g.user
        id = request.args.get("id")
        serviceList = []
        qorder = quickOrder.query.filter_by(Id=id).first()
        if user.level == 8:
            try:
                lineworkers = user.workerLink.first().manworkers.all()
                for lineworker in lineworkers:
                    serviceList.extend(
                        [
                            service
                            for service in lineworker.serviceId.all()
                            if service.serviceType == qorder.serviceType
                        ]
                    )
                print(serviceList, user.workerLink.first().manworkers.all())
            except:
                pass
        return render_template(
            "manage/order/spreadQuick.html", serviceList=serviceList, order=qorder
        )


@manage_bp.route("/confirmquick")
def confirmQuick():
    serviceId = request.args.get("serviceId")
    qorderId = request.args.get("orderId")
    order = quickOrder.query.filter_by(Id=qorderId).first()
    order.serviceLink = serviceId
    order.quickType = 2
    db.session.add(order)
    db.session.commit()
    return redirect(url_for("manage.spreadquick"))


@manage_bp.route("/orderInfo")
def orderInfo():
    id = request.args.get("id")
    order = None
    order = Service.query.filter_by(id=id).first()
    return render_template("manage/order/orderInfo.html", order=order)


@manage_bp.route("/order/research", methods=["GET", "POST"])
def orderResearch():
    orderId = request.args.get("id")
    if request.method == "POST":
        try:
            result = orderResult()
            result.createInfo(
                orderId=orderId,
                checkNumId=g.user.manLink.first().id,
                result=int(request.form["result"]),
            )
            db.session.add(result)
            db.session.commit()
        except Exception as e:
            print(e)
        return redirect(url_for("manage.order"))
    else:
        orderId = request.args.get("id")
        order = Service.query.filter_by(id=orderId).first()
        print(order)
        return render_template("manage/order/research.html", order=order)


@manage_bp.route("/order/resultLog")
def orderResultLog():
    results = orderResult.query.filter_by(checkNumId=g.user.manLink.first().id).all()
    return render_template("manage/order/resultLog.html", results=results)


@manage_bp.route("/order/<id>/print", methods=["GET"])
def printorder(id):
    # print(id)
    order = Service.query.filter_by(id=id).first()
    filename = md5()
    filename.update(
        "{}_{}".format(order.id, datetime.datetime.utcnow()).encode("utf-8")
    )
    filename = filename.hexdigest()
    basePath = os.path.abspath(os.path.curdir)
    filepath = os.path.join(basePath, "backend/static/img/order/{}/".format(order.id))
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    # print(filepath)
    pdf = PDFGenerator(filepath=filepath, filename=filename)
    pdf.genTaskPDF(order)
    filepath = filepath + filename + ".pdf"
    print(filepath)
    rsp = generatepdf(filepath).get("path")
    filepath = "http://" + os.getenv("AVATOR_SERVER") + "/" + rsp
    # print(filepath)
    return jsonify({"code": 200, "data": "{}".format(filepath)})
