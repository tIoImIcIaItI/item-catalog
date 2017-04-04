from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from category import Category
from datastore import Base
from user import User


class Item(Base):
    """
    Provides a representation of a catalog item,
    suitable for use with the sqlalchemy orm
    """
    __tablename__ = 'item'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    description = Column(String(250))

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        """
        Provides a representation of an item,
        suitable for conversion to JSON format
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'title': self.title,
            'description': self.description
        }
