import os
from flask import Flask
from flask_bcrypt import Bcrypt
from celery import Celery

from .models import db
from .email import mail


app = Flask(
    __name__, template_folder=os.path.join(os.getcwd(), "api", "email", "templates")
)

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)  # for initializing refactored cyclic imports
bcrypt = Bcrypt(app)
mail.init_app(app)  # for initializing refactored cyclic imports

CELERY_TASK_LIST = ["api.celery"]

celery = Celery(__name__, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)

from .routes import api

app.register_blueprint(api, url_prefix="/api")
