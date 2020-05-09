from flask import Blueprint, request, g, jsonify, render_template
from backend.models import ChatRoom, db, UserLinkRoom, Chat, User
# from backend.models 
from random import randrange
from hashlib import md5
import json
chat_bp = Blueprint("chat", __name__, url_prefix="/chat")


@chat_bp.route("/", methods=["GET"])
def chat():
    user = g.user
    roomId = request.args.get("roomId")
    chatRoom = None
    chatmsg = []
    if roomId:
        chatmsg = Chat.query.filter(Chat.roomId == roomId).order_by(Chat.createTime).all()[-15:-1]
    else:
        chatmsg = []
    return render_template("chat/index.html", user=user, chatmsg=chatmsg)


@chat_bp.route("/spread", methods=["POST"])
def spread():
    msg = json.loads(request.data)
    roomId = msg.get("roomId")
    message = msg.get("messsage")
    print(roomId, message)
    userIds = UserLinkRoom.query.filter(UserLinkRoom.roomId == roomId).all()
    for userId in userIds:
        chat = Chat()
        chat.createInfo(roomId=roomId, fromUser=g.user.account, toUser=userId.userAccount, msgBody=message)
        db.session.add(chat)
    db.session.commit()
    # print()
    return jsonify({"code": 200})

@chat_bp.route("/hello", methods=["POST"])
def hello():
    user = g.user
    if user:
        return jsonify({"code": 200, "data": "Welcome to loveHome"})
    else:
        return jsonify({"code": 200, "data": "please login"})


@chat_bp.route("/sendmsg", methods=["POST"])
def sendmsg():
    # print(request)
    msg = request.get_json().get("message")
    user = g.user
    if user:
        id = md5()
        id.update("{}_{}".format(user, randrange(1, 100000)).encode("utf-8"))
        id = id.hexdigest()
        try:
            chat = ChatRoom()
            chat.createRoom(id)
            db.session.add(chat)
        except Exception as e:
            print(e)
            return jsonify({"code": 500})
        userLinkRoom = UserLinkRoom()
        userLinkRoom.createInfo(user.account, roomId=id)
        db.session.add(userLinkRoom)
        manWorkers = getAllMan()
        for man in manWorkers:
            userLinkRoom = UserLinkRoom()
            userLinkRoom.createInfo(userAccount=man, roomId=id)
            db.session.add(userLinkRoom)
            chat = Chat()
            chat.createInfo(roomId=id, fromUser=user.account, toUser=man, msgBody=msg)
            db.session.add(chat)
        db.session.add(chat)
        db.session.commit()
    return jsonify({"code": 200, "data": f"{msg}", "from": user.account})
def getAllMan():
    allMan = User.query.filter(User.level > 4).all()
    manAccount = [man.account for man in allMan]
    return manAccount