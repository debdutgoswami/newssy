import sqlalchemy
import uuid
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from secrets_db import URI

engine = create_engine(URI, echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    public_id = Column(String, unique=True, nullable=False)
    country = Column(String, nullable=False)
    title = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False, unique=True)
    body = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    lastupdated = Column(String, nullable=False)
    category = Column(String, nullable=False)

    def __repr__(self):
        return f"<News(title={self.title}, source={self.source}, lastupdated={self.lastupdated})>"


def addToNews(country: str, title: str, url: str, source: str, lastupdated: str, body: str, img_url: str,
              category: str):
    session = Session()

    try:
        news = News(
            public_id=str(uuid.uuid4()),
            country=country,
            title=title,
            url=url,
            body=body,
            img_url=img_url,
            source=source,
            lastupdated=lastupdated,
            category=category
        )

        session.add(news)
        session.commit()
    except sqlalchemy.exc.IntegrityError:
        return
