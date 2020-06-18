import sqlalchemy, os, uuid
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import BYTEA, REAL
from sqlalchemy.orm import sessionmaker

from secrets_db import URI

PATH_TO_DB = os.path.join(os.getcwd(), 'app', 'database', 'newsfeed.db')

engine = create_engine(URI,echo=True)
Session = sessionmaker(bind=engine)
# metadata = MetaData()
Base = declarative_base()

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    public_id = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    title = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False, unique=True)
    # body = Column(BYTEA, nullable=False)
    source = Column(String, nullable=False)
    lastupdated = Column(String, nullable=False)
    category = Column(String, nullable=False)

    def __repr__(self):
        return f"<News(title={self.title}, source={self.source}, lastupdated={self.lastupdated})>"

#news = Table('news', metadata, autoload=True, autoload_with=engine)


def addToNews(country: str, title: str, url:str, source: str, lastupdated: str, category: str):
    session = Session()

    try:
        news = News(
            public_id = str(uuid.uuid4()),
            country = country,
            title = title,
            url = url,
            # body = body,
            source = source,
            lastupdated = lastupdated,
            category = category
        )
    
        session.add(news)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        return
