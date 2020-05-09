from flask import render_template, redirect, request
from . import admin_bp
from backend.models import db, User


@admin_bp.route("/user/Info")
def userInfo():
    account = request.args.get("account")
    print(account)
    user = User.query.filter_by(account=account).first()
    # print(user)
    manworkers = []
    if user.level > 8:
        manworkers = user.manLink.first().manworkers.all()
    elif user.level == 8:
        manworkers = user.workerLink.first().manworkers.all()
    # elif user.level == 4:
    #     manworkers = user.lineworkerLink.first().manworkers.all()
    return render_template("admin/user/Info.html", user=user, manworkers=manworkers)
