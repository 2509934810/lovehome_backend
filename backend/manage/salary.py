from flask import g, render_template, redirect, url_for
from backend.manage import manage_bp
from backend.models import ecomoStream, db, User


@manage_bp.route("/salarystream")
def salarystream():
    ecnoList = []
    user = g.user
    if user.level < 4:
        orders = (
            User.query.filter_by(account=user.account)
            .first()
            .baseuserLink.first()
            .orderLink.all()
        )
        if orders:
            try:
                ecnoList = [
                    order.econRel.first()
                    for order in orders
                    if not order.econRel.first() is None
                ]
            except Exception as e:
                print(e)
    print(ecnoList)
    return render_template("salary/index.html", ecnoList=ecnoList)
