from flask_cors import CORS

from flask import Flask, Blueprint, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from api.models import db
from api.email import mail

from celery import Celery

import os

app = Flask(__name__, static_folder='./build', static_url_path='/',template_folder=os.path.join(os.getcwd(),'api','email','templates'))

CORS(app)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # for initializing refactored cyclic imports
bcrypt = Bcrypt(app)
mail.init_app(app) # for initializing refactored cyclic imports

CELERY_TASK_LIST = [
    'api.celery'
]

celery = Celery(__name__, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

from api.routes import api

app.register_blueprint(api, url_prefix='/api')

@app.route('/')
def index():
    # serves index.html generated from REACT
    return app.send_static_file('index.html')