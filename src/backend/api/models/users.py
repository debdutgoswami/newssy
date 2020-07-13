import datetime, uuid
from api import bcrypt, app
from api.models import db
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.mutable import Mutable

class MutableList(Mutable, list):
    def append(self, value):
        list.append(self, value)
        self.changed()

    @classmethod
    def coerce(cls, key, value):
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

# Database ORMs
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    joined_on =db.Column(db.String(30))
    name_changed_on = db.Column(db.String(30))
    admin = db.Column(db.Boolean)
    preferences = db.Column(ARRAY(db.String(100)))
    saved_article = db.Column(MutableList.as_mutable(ARRAY(db.String(100))))
    email_notify = db.Column(db.Boolean)
    confirmed = db.Column(db.Boolean)
    VERIFIED = db.Column(db.Boolean) # verified tick like Twitter
    BANNED = db.Column(db.Boolean)
    banned_on = db.Column(db.String(30))

    def __init__(self, first_name, last_name, email, password, email_notify=False):
        self.public_id = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.admin = False
        self.joined_on = datetime.datetime.utcnow()
        self.email_notify = email_notify
        self.name_changed_on = self.joined_on
        self.confirmed = False
        self.preferences = None
        self.saved_article = None
        self.VERIFIED = False
        self.BANNED = False
        self.banned_on = None

    def __repr__(self):
        return f"<User(name={self.first_name}, admin={self.admin})>"
