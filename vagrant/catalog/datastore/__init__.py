from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datastore import config

Base = declarative_base()
engine = create_engine(URL(**config.DATABASE))
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
