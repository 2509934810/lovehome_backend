from flask import render_template, request
from backend.admin import admin_bp
from backend.models import Service


@admin_bp.route("/orderList")
def orderList():
    orders = Service.query.all()
    return render_template("admin/order/index.html", orders=orders)


@admin_bp.route("/order/search")
def searchOrder():
    id = request.args.get("id")
    orders = Service.query.filter_by(id=id).all()
    return render_template("admin/order/index.html", orders=orders)
