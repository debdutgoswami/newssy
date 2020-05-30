import datetime, uuid
from api import bcrypt, app
from api.models import db
from sqlalchemy.dialects.postgresql import ARRAY

# Database ORMs
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    joined_on =db.Column(db.String)
    name_changed_on = db.Column(db.String)
    admin = db.Column(db.Boolean)
    preferences = db.Column(ARRAY(db.String))
    saved_article = db.Column(ARRAY(db.String))
    email_notify = db.Column(db.Boolean)
    confirmed = db.Column(db.Boolean)
    VERIFIED = db.Column(db.Boolean) # verified tick like Twitter

    def __init__(self, name, email, password, preferences=None, saved_article=None, email_notify=False, confirmed=False):
        self.public_id = uuid.uuid4()
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.admin = False
        self.joined_on = datetime.datetime.utcnow()
        self.email_notify = email_notify
        self.name_changed_on = self.joined_on
        self.confirmed = confirmed
        self.preferences = preferences
        self.saved_article = saved_article
        self.VERIFIED = False

    def __repr__(self):
        return f"<User(name={self.name}, admin={self.admin})>"
