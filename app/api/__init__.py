from flask import Flask, Blueprint
from flask_wtf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'yoursecretkey'

from api.routes import api

app.register_blueprint(api, url_prefix='/api')