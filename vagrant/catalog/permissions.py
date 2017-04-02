from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database_setup import Item
from users import UserUtils

Base = declarative_base()
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Permissions(object):
    def __init__(self, create, read, update, delete):
        self.create = create
        self.read = read
        self.update = update
        self.delete = delete

    @staticmethod
    def get_user_permissions_for_category(category):
        """
        :param category: Category 
        :rtype: Permissions
        """

        def category_is_in_use(category_id):
            return session.query(Item).filter_by(
                category_id=category_id).count()

        belongs_to_user = True
        # TODO: re-introduce owning user fields to Category
        # category.user_id == UserUtils.get_authenticated_user_id()

        is_in_use = \
            category_is_in_use(category.id)

        return Permissions(
            create=True,
            read=True,
            update=belongs_to_user,
            delete=belongs_to_user and not is_in_use)

    @staticmethod
    def get_user_permissions_for_item(item):
        """
        :param item: Item 
        :rtype: Permissions
        """
        belongs_to_user = \
            item.user_id == UserUtils.get_authenticated_user_id()

        return Permissions(
            create=True,
            read=True,
            update=belongs_to_user,
            delete=belongs_to_user)
