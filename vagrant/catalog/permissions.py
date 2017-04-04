from datastore import session
from datastore.item import Item
from users import UserUtils


class Permissions(object):
    """
    Determines and represents the permissions available on a given resource
    in a given context
    """

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
        belongs_to_user = \
            category.user_id == UserUtils.get_authenticated_user_id()

        is_in_use = \
            session.query(Item). \
            filter_by(category_id=category.id). \
            count()

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
