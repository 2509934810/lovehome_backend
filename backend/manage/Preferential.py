from backend.manage import manage_bp
from flask import g, render_template, redirect, request, url_for
from backend.models import User, perferCard, userperferCard, db, BaseUser


@manage_bp.route("/baseuser/list")
def baseuserList():
    user = g.user
    users = User.query.filter(User.level < 4).all()
    prefercard = [
        card
        for card in user.manLink.first().perferCardLink.all()
        if card.userlink.first() is None
    ]
    card300 = [card for card in prefercard if card.cardNum == 300]
    card500 = [card for card in prefercard if card.cardNum == 500]
    card800 = [card for card in prefercard if card.cardNum == 800]
    cardDict = {}
    cardDict["300"] = card300
    cardDict["500"] = card500
    cardDict["800"] = card800
    return render_template(
        "manage/user/baseUserlist.html",
        users=users,
        prefercard=prefercard,
        cardDict=cardDict,
    )


@manage_bp.route("/base/user/list/send", methods=["GET", "POST"])
def sendcard():
    if request.method == "POST":
        id = request.args.get("id")
        preferCardId = request.form["preferCardId"]
        card = perferCard.query.filter(perferCard.Id == preferCardId).first()
        usercard = userperferCard()
        # usercard.cardType = False
        userId = BaseUser.query.filter(BaseUser.userAc == id).first().id
        usercard.createInfo(cardId=card.Id, userId=userId)
        db.session.add(usercard)
        db.session.commit()
        return redirect(url_for("manage.baseuserList"))
    else:
        id = request.args.get("id")
        # user = User.query.filter(User.account==id).first()
        user = g.user
        prefercards = [
            card
            for card in user.manLink.first().perferCardLink.all()
            if card.userlink.first() is None
        ]
        # print(prefercards)
        return render_template(
            "manage/user/sendpreferCard.html", id=id, prefercards=prefercards
        )
