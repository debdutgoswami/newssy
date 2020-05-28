from flask import Flask, Blueprint, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from celery import Celery

import os

app = Flask(__name__, template_folder=os.path.join(os.getcwd(),'api','email','templates'))

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

CELERY_TASK_LIST = [
    'api.celery'
]

celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from api.routes import api

app.register_blueprint(api, url_prefix='/api')