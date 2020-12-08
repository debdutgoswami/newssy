from . import db

_NEWS_SOURCE = ['Times of India', 'BBC']


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)  # refering to url safe and unique
    # obtained by scraping
    country = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(400), unique=True, nullable=False)
    body = db.Column(db.String(400), nullable=False)
    img_url = db.Column(db.String(400), nullable=False)
    url = db.Column(db.String(400), nullable=False, unique=True)

    source = db.Column(db.String(100), nullable=False)  # name of the news vendor
    lastupdated = db.Column(db.String(100), nullable=False)  # time the news was added
    # obtained from Ml model
    category = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<News(title={self.title}, source={self.source}, lastupdated={self.lastupdated})>"
