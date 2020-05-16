import os
from flask import Flask, render_template, jsonify, session
from flask import g

# from flask_sqlalchemy import SQLAlchemy
import click
from flask.cli import with_appcontext
from instance.config import DevConfig, ProConfig
from flask_redis import FlaskRedis

# from flask_celery import Celery
from flask_cors import CORS
from backend.models import Info

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

    @app.route("/")
    def index():
        # serviceAddr = request.args.get("serviceAddr")
        # serviceType = Info.SERVICETYPE.get(request.args.get("serviceType"))
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
