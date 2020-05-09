from flask_socketio import socketio, emit, SocketIO, join_room, leave_room
from flask import g
from backend.models import db, chatRoom
from backend import redis_store
from random import randrange
from datetime import datetime

socketapp = SocketIO()


@socketapp.on("new_login")
def newlogin(msg):
    # print(msg)
    user = g.user
    if not user is None:
        data = {"code": "received"}
        emit("received", data)
    else:
        roomId = randrange(1000, 10000)
        # if redis_store.get()
        # redis_store.set("tmp_{}".format(roomId), datetime.timestamp(), ex=30000)
        # info = chatRoom()
        # info.createInfo(sendId="tmp_user", reveId="all", msgBody=msg)
        # db.session.add(info)
        # db.session.commit()
        data = {"code": "请登陆后咨询"}
        emit("received", data)


@socketapp.on("send_msg")
def sendmsg(msg):
    user = g.user
    if not user is None:

        data = {"code": "received"}
        emit("received", data)
    else:
        roomId = randrange(1000, 10000)
        data = {"code": "请登陆后咨询"}
        emit("received", data)
