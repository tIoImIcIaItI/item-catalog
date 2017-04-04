from sqlalchemy import Column, Integer, String

from datastore import Base


class User(Base):
    """
    Provides a representation of an application user,
    suitable for use with the sqlalchemy orm
    """
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    picture = Column(String(250))
