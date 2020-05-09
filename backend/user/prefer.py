from backend.user import user_bp
from flask import g, render_template, redirect, url_for
from backend.models import perferCard, userperferCard


@user_bp.route("/user/prefer/")
def prefercard():
    user = g.user
    cardlist = (
        user.baseuserLink.first()
        .cardLink.filter(userperferCard.cardType == False)
        .all()
    )
    print(cardlist)
    return render_template("user/preferCard.html", cardlist=cardlist)
