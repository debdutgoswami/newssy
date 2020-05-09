from flask import Flask, Blueprint, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from api.routes import api

app.register_blueprint(api, url_prefix='/api')