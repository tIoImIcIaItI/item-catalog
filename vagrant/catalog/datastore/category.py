from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from datastore import Base
from user import User


class Category(Base):
    """
    Provides a representation of a catalog category,
    suitable for use with the sqlalchemy orm
    """
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """
        Provides a representation of a category,
        suitable for conversion to JSON format
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }
