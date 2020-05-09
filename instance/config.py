import os
from datetime import timedelta


class BaseConfig(object):
    DEBUG = True
    DATA_PER_PAGE = 6
    CELERY_BROKER_URL = ("redis://localhost:6379/1",)
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CELERYBEAT_SCHEDULE = {
        # 定义任务名称：import_data
        # 执行规则：每600秒运行一次
        "import_data": {"task": "import_data", "schedule": timedelta(seconds=600)}
    }

class ProConfig(BaseConfig):
    REDIS_URL = "redis://{}:6379/0".format(os.getenv("REDIS_SERVER"))
    AUTH_REDIS = "redis://{}:6379/3".format(os.getenv("REDIS_SERVER"))
    SECRET_KEY = "123456789"
    DIALECT = "mysql"
    DRIVER = "pymysql"
    USERNAME = "root"
    PASSWORD = "lei123"
    HOST = "{}".format(os.getenv("MYSQL_SERVER"))
    PORT = "3306"
    DATABASE = "lei"
    URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    WTF_CSRF_SECRET_KEY = "random key for form"


class DevConfig(BaseConfig):
    REDIS_URL = "redis://127.0.0.1:6379/0"
    AUTH_REDIS = "redis://localhost:6379/3"
    SECRET_KEY = "123456789"
    DIALECT = "mysql"
    DRIVER = "pymysql"
    USERNAME = "lei"
    PASSWORD = "lei123"
    HOST = "127.0.0.1"
    PORT = "3306"
    DATABASE = "lei"
    URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )
    SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    ARTICLES_PER_PAGE = 10
    COMMENTS_PER_PAGE = 6
    WTF_CSRF_SECRET_KEY = "random key for form"
