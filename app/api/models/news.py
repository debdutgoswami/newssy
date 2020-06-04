from api.models import db
from sqlalchemy.dialects.postgresql import BYTEA, REAL

class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, unique=True, nullable=False) # refering to url safe and unique
    # obtained by scraping
    country = db.Column(db.String, nullable=False)
    title = db.Column(BYTEA, unique=True, nullable=False)
    body = db.Column(BYTEA, nullable=False)
    source = db.Column(db.String, nullable=False) # name of the news vendor
    lastupdated = db.Column(db.String, nullable=False) # time the news was added
    # obtained from Ml model
    category = db.Column(db.String)
    accuracy = db.Column(REAL)

    def __repr__(self):
        return f"<News(title={self.title}, source={self.source}, lastupdated={self.lastupdated})>"
