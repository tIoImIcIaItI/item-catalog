from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False, unique=True)
    picture = Column(String(250))


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name
        }


class Item(Base):
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
        return {
            'id': self.id,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'title': self.title,
            'description': self.description
        }

# create global data store objects
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)

# BOOTSTRAP CODE TO POPULATE AN OTHERWISE EMPTY DATABASE
# AFTER A USER HAS BEEN CREATED
#
# if __name__ == '__main__':
#     session = DBSession()
#
#     user = session.query(User).first()
#
#     session.add(Category(name='Soccer', user_id=user.id))
#     session.add(Category(name='Basketball', user_id=user.id))
#     session.add(Category(name='Baseball', user_id=user.id))
#     session.add(Category(name='Frisbee', user_id=user.id))
#     session.add(Category(name='Snowboarding', user_id=user.id))
#     session.add(Category(name='Rock Climbing', user_id=user.id))
#     session.add(Category(name='Foosball', user_id=user.id))
#     session.add(Category(name='Skating', user_id=user.id))
#     session.add(Category(name='Hockey', user_id=user.id))
#
#     session.commit()
#
#     cat = session.query(Category).filter_by(name='Soccer').one()
#
#     session.add(Item(title='Soccer Ball', category_id=cat.id,
#                      user_id=user.id))
#     session.add(Item(title='Goal', category_id=cat.id, user_id=user.id))
#     session.add(Item(title='Shin Guards', category_id=cat.id,
#                      user_id=user.id))
#
#     session.commit()
