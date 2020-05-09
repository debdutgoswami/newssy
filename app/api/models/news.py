from api import db
from sqlalchemy.dialects.postgresql import BYTEA, REAL

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True, nullable=False)
    country = db.Column(db.String, nullable=False)
    title = db.Column(BYTEA, unique=True, nullable=False)
    body = db.Column(BYTEA, nullable=False)
    source = db.Column(db.String, nullable=False)
    lastupdated = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    accuracy = db.Column(REAL)

    def __repr__(self):
        return f"<News(title={self.title}, source={self.source}, lastupdated={self.lastupdated})>"
