from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

# from . import db
from hashlib import md5
import random

db = SQLAlchemy()

# db.Model =db.make_declarative_db.Model(db.Model)
class User(db.Model):
    LEVEL = {
        "USER_LOW": 1,
        "USER_MID": 2,
        "WORKER": 4,
        "MANAGE_LOW": 8,
        "MANAGE_MID": 16,
        "MANAGE_HIG": 32,
        "ADMIN": 64,
    }

    SEX = {"man": True, "woman": False}

    account = db.Column(db.String(20), primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.Text, nullable=False)
    addr = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(30), nullable=True)
    telephone = db.Column(db.String(15), nullable=True)
    level = db.Column(db.Integer, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    actived = db.Column(db.Boolean, nullable=False, default=False)
    # loginInfo = db.relationship("loginTb", backref="user", lazy="dynamic")
    sex = db.Column(db.Boolean, nullable=True)
    age = db.Column(db.Integer, nullable=False, default=0)
    acType = db.Column(db.Boolean, default=False)
    head_photo = db.Column(db.String(100), nullable=True)
    # service = db.relationship("Service", backref="user", lazy="dynamic")
    avatorLink = db.relationship("Avator", backref="user", lazy="dynamic")
    chatLink = db.relationship("UserLinkRoom", backref="user", lazy="dynamic")
    manLink = db.relationship(
        "LoveManage",
        backref=db.backref("user", uselist=False),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    workerLink = db.relationship(
        "LoveWorker",
        backref=db.backref("user", uselist=False),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    lineworkerLink = db.relationship(
        "LoveLineWorker",
        backref=db.backref("user", uselist=False),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    baseuserLink = db.relationship(
        "BaseUser",
        backref=db.backref("user", uselist=False),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    salaryStandLink = db.relationship(
        "SalaryStand",
        backref=db.backref("user", uselist=False),
        lazy="dynamic",
        cascade="all, delete-orphan",
    )
    salaryeconLink = db.relationship(
        "salaryeCon", backref=db.backref("user"), lazy="dynamic"
    )
    loginInfoLink = db.relationship("loginTb", backref=db.backref("user"), lazy="dynamic")

    def __repr__(self):
        return "<Post %r>" % self.account

    def createUser(self, account, password, role, username):
        self.account = account
        self.password = password
        self.level = self.LEVEL.get(role)
        self.username = username

    def addPermission(self, role):
        self.level = self.LEVEL.get(role)

    def revertPermission(self):
        self.level = self.LEVEL.get("USER_LOW")

    def updateInfo(self, username, email, telephone, sex, age, actived):
        self.username = username
        self.email = email
        self.telephone = telephone
        self.sex = sex
        self.age = age
        self.actived = actived

    @staticmethod
    def checkRoot(DbLevel, UserLevel):
        return DbLevel == UserLevel


class UserAddr(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    code = db.Column(db.String(30), nullable=False)


class Avator(db.Model):
    Id = db.Column(db.String(100), primary_key=True)
    path = db.Column(db.Text)
    userId = db.Column(db.String(20), db.ForeignKey("user.account"))

class salaryeCon(db.Model):
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    createTime = db.Column(db.DateTime, default=datetime.utcnow())
    userId = db.Column(db.String(20), db.ForeignKey("user.account"))
    salaryNum = db.Column(db.Integer, nullable=False, default=0)
    salaryMonth = db.Column(db.String(20), nullable=False)


class SalaryStand(db.Model):
    SALARYTYPE = {"no": 0, "loading": 1, "done": 2}
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    startTime = db.Column(db.DateTime, default=datetime.utcnow())
    salaryNum = db.Column(db.Integer, nullable=False, default=3000)
    userId = db.Column(db.String(20), db.ForeignKey("user.account", ondelete="CASCADE"))
    spreadType = db.Column(db.Integer, default=0)

    def createInfo(self, userId, salaryNum):
        self.userId = userId
        self.salaryNum = salaryNum


class LoveManage(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    level = db.Column(db.Integer, nullable=False, default=0)
    userAc = db.Column(db.String(20), db.ForeignKey("user.account", ondelete="CASCADE"))
    manworkers = db.relationship("LoveWorker", backref="lovemanage", lazy="dynamic")
    salaryLink = db.relationship(
        "Salary", backref=db.backref("lovemanage"), lazy="dynamic"
    )
    perferCardLink = db.relationship("perferCard", backref="lovemanage", lazy="dynamic")
    orderResultLink = db.relationship(
        "orderResult", backref=db.backref("lovemanage"), lazy="dynamic"
    )


# 线上工作者
class LoveWorker(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    level = db.Column(db.Integer, nullable=False, default=0)
    userAc = db.Column(db.String(20), db.ForeignKey("user.account", ondelete="CASCADE"))
    manId = db.Column(db.String(100), db.ForeignKey("love_manage.id"))
    manworkers = db.relationship("LoveLineWorker", backref="loveworker", lazy="dynamic")
    salaryLink = db.relationship(
        "Salary", backref=db.backref("loveworker"), lazy="dynamic"
    )


# 线下工作者
class LoveLineWorker(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    level = db.Column(db.Integer, nullable=False, default=0)
    userAc = db.Column(db.String(20), db.ForeignKey("user.account", ondelete="CASCADE"))
    manId = db.Column(db.String(100), db.ForeignKey("love_worker.id"))
    serviceId = db.relationship("Info", backref="lovelineworker", lazy="dynamic")
    salaryLink = db.relationship(
        "Salary", backref=db.backref("lovelineworker"), lazy="dynamic"
    )


# 基本用户，一般为其他用户
class BaseUser(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    level = db.Column(db.Integer, nullable=False, default=0)
    userAc = db.Column(db.String(20), db.ForeignKey("user.account", ondelete="CASCADE"))
    orderLink = db.relationship("Service", backref="baseuser", lazy="dynamic")
    quickorder = db.relationship("quickOrder", backref="baseuser", lazy="dynamic")
    cardLink = db.relationship("userperferCard", backref="baseuser", lazy="dynamic")

    def createInfo(self, level, userAc):
        id = md5()
        id.update("{}".format(userAc).encode("utf-8"))
        self.id = id.hexdigest()
        self.level = level
        self.userAc = userAc


class Info(db.Model):
    __tablename__ = "Info"
    # TIMETYPE = {
    #     # 家政保姆
    #     "1": 1,  # 小时工
    #     "H_WORKER_H": 4,  # 高级小时工
    #     "M_WORKER": 2,  # 月
    #     "M_WORKER_H": 8,  # 月 高级
    # }
    SERVICETYPE = {"yuesao": 1, "xiaoshi": 2, "baomu": 4}
    id = db.Column(db.String(100), primary_key=True)
    head_photo = db.Column(db.String(80), nullable=False)
    # timeType = db.Column(db.Integer, nullable=False, default=1)
    serviceType = db.Column(db.Integer, nullable=False, default=1)
    live_addr = db.Column(db.Text, nullable=False)
    avg_salary = db.Column(db.Integer, nullable=False, default=0)
    # 表示服务受到许可
    access = db.Column(db.Boolean, nullable=False, default=False)
    serviceLink = db.Column(
        db.String(100), db.ForeignKey("love_line_worker.id", ondelete="CASCADE")
    )
    orderLink = db.relationship("Service", backref="info", lazy="dynamic")
    quickorder = db.relationship("quickOrder", backref="info", lazy="dynamic")

    def __repr__(self):
        return "{}".format(self.id)

    def createInfo(self, id, head_photo, serviceType, live_addr, salary, serviceLink):
        self.id = id
        self.head_photo = head_photo
        self.serviceType = self.SERVICETYPE.get(serviceType)
        self.live_addr = live_addr
        self.avg_salary = self._salary(salary)
        self.serviceLink = serviceLink

    def activeAcc(self, set=False):
        if set:
            self.access = True
        else:
            self.access = False

    def changeTimeType(self, timeType):
        self.timeType = self.TIMETYPE.get(timeType)

    def _salary(self, salary, radio=1.5):
        return salary * radio

    # print(salary, timeType, self.TIMETYPE[timeType])
    # if self.TIMETYPE[timeType] > 2:
    #     return salary * radio
    # else:
    #     return salary


class Salary(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    send_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    salary_num = db.Column(db.Float, nullable=False, default=0)
    manId = db.Column(db.String(100), db.ForeignKey("love_manage.id"))
    workerId = db.Column(db.String(100), db.ForeignKey("love_worker.id"))
    lineworkerId = db.Column(db.String(100), db.ForeignKey("love_line_worker.id"))


# # add worker table


class loginTb(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20), db.ForeignKey("user.account"))
    loginTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    loginSite = db.Column(db.Text, nullable=False, default="shanxi")
    def createData(self, userId, loginSite):
        self.user_id = userId
        self.loginSite = loginSite


# create db
# 订单
class Service(db.Model):
    ORDERTYPE = {
        "loading": 1,
        "received": 2,
        "doing": 4,
        "done": 8,
        "nopay": 16,
        "pay": 32,
    }
    # TIMECELL = {"hour": 1, "day": 2, "month": 4, "year": 8}
    # SERVICETYPE = {
    #     "清洁工": 1,  # 清洁工
    #     "保姆": 2,  # bao
    # }
    ORDERREVIEW = {"bad": 1, "mid": 2, "good": 4}
    id = db.Column(db.String(100), primary_key=True)
    customerId = db.Column(db.String(100), db.ForeignKey("base_user.id"))
    providerId = db.Column(db.String(100), db.ForeignKey("Info.id"))
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # serviceType = db.Column(db.Integer, nullable=False)
    ServiceAddr = db.Column(db.Text, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    preStartTime = db.Column(db.DateTime, nullable=False)
    startTime = db.Column(db.DateTime, nullable=True)
    endTime = db.Column(db.DateTime, nullable=True)
    payTime = db.Column(db.DateTime, nullable=True)
    orderType = db.Column(db.Integer, nullable=False, default=1)
    orderReq = db.relationship("orderReq", backref="order", lazy="dynamic")
    # 评论
    orderReview = db.Column(db.Integer, nullable=False, default=4)
    orderResultLink = db.relationship(
        "orderResult", backref=db.backref("order", uselist=False), lazy="dynamic"
    )
    # econRel = db.relationship("ecomoStream", backref=db.backref("order", uselist=False), lazy="dynamic")
    def __repr__(self):
        return self.id

    def create(self, customerId, providerId, ServiceAddr, preStartTime):
        id = md5()
        key = customerId + str(random.randrange(1, 10000000))
        id.update(key.encode("utf-8"))
        self.id = id.hexdigest()
        self.customerId = customerId
        self.providerId = providerId
        # print(serviceType)
        self.ServiceAddr = ServiceAddr
        self.orderType = self.ORDERTYPE.get("loading")
        self.preStartTime = preStartTime
        self.salary = 0

    def actived(self):
        self.orderType = self.ORDERTYPE.get("received")

    def start(self):
        self.startTime = datetime.utcnow
        self.orderType = self.ORDERTYPE.get("start")

    def doing(self):
        self.orderType = self.ORDERTYPE.get("doing")

    def done(self):
        self.endTime = datetime.utcnow
        self.orderType = self.ORDERTYPE.get("done")

    def pay(slef):
        self.payTime = datetime.utcnow
        self.orderType = self.ORDERTYPE.get("pay")


# class serviceEcon(db.Model):



class orderResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(db.String(100), db.ForeignKey("service.id"))
    checkNumId = db.Column(db.String(100), db.ForeignKey("love_manage.id"))
    result = db.Column(db.Integer, nullable=False, default=3)

    def createInfo(self, orderId, checkNumId, result):
        self.orderId = orderId
        self.checkNumId = checkNumId
        self.result = result


# 申诉请求
class orderReq(db.Model):
    TYPE = {"notSolve": 1, "doing": 2, "solved": 4}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(db.String(100), db.ForeignKey("service.id", ondelete="CASCADE"))
    reqType = db.Column(db.Integer, nullable=False)
    reqBody = db.Column(db.Text, nullable=False)

    def create(self, orderId, reqBody):
        self.orderId = orderId
        self.reqBody = reqBody
        self.reqType = 1


# class chatRoom(db.Model):
#     bodyType = {"noread": 1, "read": 2}
#     Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     roomId = db.Column(db.Integer, unique=True)
#     sendId = db.Column(db.String(20))
#     reveId = db.Column(db.String(20))
#     msgBody = db.Column(db.Text)
#     sendTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
#     chatType = db.Column(db.Integer, nullable=False, default=1)

#     def createInfo(self, sendId, reveId, msgBody, roomId):
#         self.roomId = roomId
#         self.sendId = sendId
#         self.reveId = reveId
#         self.msgBody = msgBody
#         self.chatType = 1


# 快速订单
class quickOrder(db.Model):
    SERVICETYPE = {"yuesao": 1, "xiaoshi": 2, "baomu": 4}
    SEX = {"no": 0, "man": 1, "woman": 2}
    QUICKTYPE = {"loading": 1, "doing": 2, "done": 4}
    Id = db.Column(db.String(100), primary_key=True)
    userLink = db.Column(db.String(100), db.ForeignKey("base_user.id"))
    serviceLink = db.Column(db.String(100), db.ForeignKey("Info.id"))
    age = db.Column(db.Integer, nullable=True)
    sex = db.Column(db.Integer, nullable=True)
    serviceType = db.Column(db.Integer, nullable=False)
    createTime = db.Column(db.DateTime, default=datetime.utcnow())
    preStartTime = db.Column(db.DateTime, nullable=False)
    addr = db.Column(db.Text, nullable=False)
    quickType = db.Column(db.Integer, nullable=False, default=1)

    def createInfo(
        self, Id, userLink, serviceType, preStartTime, addr, age=None, sex=None
    ):
        self.Id = Id
        self.userLink = userLink
        self.serviceType = self.SERVICETYPE.get(serviceType)
        self.preStartTime = preStartTime
        self.age = age
        self.sex = self.SEX.get(sex)
        self.quickType = 1
        self.addr = addr


# 资金流
class ecomoStream(db.Model):
    STREAMTYPE = {"service": 1, "gongzi": 2}
    ECONTYPE = {"out": True, "in": False}
    SERVICETYPE = {"yuesao": 1, "xiaoshi": 2, "baomu": 4, "gongzi": 8}
    id = db.Column(db.String(100), primary_key=True)
    econNum = db.Column(db.Integer, nullable=False, default=0)
    createTime = db.Column(db.DateTime, default=datetime.utcnow())
    serviceType = db.Column(db.Integer, nullable=False)
    econType = db.Column(db.Boolean, nullable=False, default=True)
    streamType = db.Column(db.Integer, nullable=False)

    def createInfo(self, id, econNum, serviceType, streamType=None):
        self.id = id
        self.econNum = econNum
        # self.orderId = orderId
        self.serviceType = serviceType
        self.streamType = ecomoStream.STREAMTYPE.get(streamType, 1)


class perferCard(db.Model):
    Id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cardId = db.Column(db.String(100), unique=True)
    manId = db.Column(db.String(100), db.ForeignKey("love_manage.id"))
    # userId = db.Column(db.String(100), nullable=True)
    cardNum = db.Column(db.Integer, nullable=False, default=0)
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    expireTime = db.Column(db.Integer, nullable=False, default=30)
    userlink = db.relationship(
        "userperferCard",
        backref=db.backref("perfercard", uselist=False),
        lazy="dynamic",
    )

    def createInfo(self, cardId, manId, cardNum):
        self.cardId = cardId
        self.manId = manId
        self.cardNum = cardNum
        # self.userId = userId


class userperferCard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cardType = db.Column(db.Boolean, default=False)
    cardId = db.Column(db.Integer, db.ForeignKey("perfer_card.Id"))
    userId = db.Column(db.String(100), db.ForeignKey("base_user.id"))

    def createInfo(self, cardId, userId):
        self.cardId = cardId
        self.userId = userId

class UserLinkRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userAccount = db.Column(db.String(20), db.ForeignKey("user.account"))
    roomId = db.Column(db.String(100), db.ForeignKey("chat_room.id"))
    def createInfo(self, userAccount, roomId):
        self.userAccount = userAccount
        self.roomId = roomId
class ChatRoom(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    roomLink= db.relationship("UserLinkRoom", backref="chatroom", lazy="dynamic")
    chatLink = db.relationship("Chat", backref=db.backref("chatroom"), lazy="dynamic")
    roomType = db.Column(db.Integer, nullable=False, default=1)
    def createRoom(self,id, roomType=1):
        self.id = id
        self.roomType = roomType
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roomId = db.Column(db.String(100), db.ForeignKey("chat_room.id"))
    fromUser = db.Column(db.String(20), db.ForeignKey("user.account"))
    toUser = db.Column(db.String(20), db.ForeignKey("user.account"))
    msgBody = db.Column(db.Text)
    createTime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    readType = db.Column(db.Boolean, default=False)
    def createInfo(self, roomId, fromUser, toUser, msgBody):
        self.roomId = roomId
        self.fromUser = fromUser
        self.toUser = toUser
        self.msgBody = msgBody