import datetime, uuid
from api import db, bcrypt, app
from sqlalchemy.dialects.postgresql import ARRAY

# Database ORMs
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    joined_on =db.Column(db.String)
    admin = db.Column(db.Boolean)
    preferences = db.Column(ARRAY)
    email_notify = db.Column(db.Boolean)
    whatsapp_notify = db.Column(db.Boolean)
    confirmed = db.Column(db.Boolean)

    def __init__(self, name, email, password, preferences=None, admin=False, email_notify=False, whatsapp_notify=False, confirmed=False):
        self.public_id = uuid.uuid4()
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.joined_on = datetime.datetime.utcnow()
        self.email_notify = email_notify
        self.whatsapp_notify = whatsapp_notify
        self.confirmed = confirmed

    def __repr__(self):
        return f"<User(name={self.name}, admin={self.admin})>"
