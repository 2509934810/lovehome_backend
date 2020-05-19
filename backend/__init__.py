import os, re
from flask import Flask, render_template, jsonify, session
from flask import g, request
# from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext
from instance.config import DevConfig, ProConfig
from flask_redis import FlaskRedis

# from flask_celery import Celery
from flask_cors import CORS
from backend.models import Info
from backend.utils.generateVal import generate as generateval
from backend.utils.generaeMail import SendMail
from backend.utils.generateVal import getRandomStr
redis_store = FlaskRedis()


ENV = {"development": DevConfig, "production": ProConfig}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.add_template_global(os.environ.get("AVATOR_SERVER"), "avator")
    if test_config:
        app.config.from_object(test_config)
    else:
        config = ENV.get(os.environ.get("FLASK_ENV"), DevConfig)
        app.config.from_object(config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    app.jinja_env.variable_start_string = "[["
    app.jinja_env.variable_end_string = "]]"
    from backend.models import db

    db.init_app(app)
    # init_app(app)

    redis_store.init_app(app)
    # celery.init_app(app)
    # 注册auth redis
    # auth_store.init_app(app)
    from backend.auth import auth_bp

    app.register_blueprint(auth_bp)

    from backend.admin import admin_bp

    app.register_blueprint(admin_bp)

    from backend.manage import manage_bp

    app.register_blueprint(manage_bp)
    from backend.user import user_bp

    app.register_blueprint(user_bp)
    # 初始化socketapp
    # from backend.socketApp import socketapp
    # socketapp.init_app(app)
    # from backend.admin import admin_bp
    # app.register_blueprint(admin_bp)

    # from backend.api import api_bp
    # app.register_blueprint(api_bp)

    from backend.service import service_bp

    app.register_blueprint(service_bp)

    from backend.chat import chat_bp

    app.register_blueprint(chat_bp)
    # from backend.manage import manage_bp
    # app.register_blueprint(manage_bp)

    from backend.models import User

    @app.before_request
    def check_login():
        user = User.query.filter_by(account=session.get("userId")).first()
        if user:
            g.user = user
        else:
            g.user = None

    @app.route("/sendemail")
    def sendeamil():
        if g.user is None:
            return jsonify({"code": 500})
        SS = ""
        email = request.args.get("mail")
        if not re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',email):
            return jsonify({"code": 500})
        try:
            for i in range(6):
                SS += getRandomStr()
            mail = SendMail(text=SS, sender="lovehome", receiver="Dear cumtomer", subject="Val", address="{}".format(email))
            mail.send()
            redis_store.set("email_{}".format(g.user.account), SS)
        except Exception as e:
            print(e)
            return jsonify({"code": 500})
        return jsonify({"code": 200})
    @app.route("/generatePng")
    def generatePng():
        SS, pngPath = generateval()
        print(SS, pngPath)
        return jsonify({"pngPath": pngPath, "avator": os.getenv("AVATOR_SERVER")})

    @app.route("/")
    def index():
        # serviceAddr = request.args.get("serviceAddr")
        # serviceType = Info.SERVICETYPE.get(request.args.get("serviceType"))
        # SS, pngPath = generateval()
        # print(SS, pngPath)
        serviceType = None
        if serviceType:
            services = Info.query.filter(db.and_(Info.serviceType==serviceType, Info.access==True)).all()
        else:
            services = Info.query.filter_by(access=True).all()
        return render_template("index.html", services = services)

    @app.route("/404")
    def pageNotFound():
        data = {"code": 404, "info": "page not found"}
        return jsonify(data)
    return app
