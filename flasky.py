import os
from backend import create_app

# from models import db
from flask_script import Manager, Shell
from instance.config import ProConfig, DevConfig
from backend.database import db

ENV = {"development": DevConfig, "production": ProConfig}

app = create_app(ENV.get(os.getenv("FLASK_ENV"), DevConfig))
manage = Manager(app)

if __name__ == "__main__":
    manage.run()
