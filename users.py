"""
Classes for user information for the social network project
revised to work with database
"""

# pylint: disable=R0903

from loguru import logger
from peewee import IntegrityError, DoesNotExist
from socialnetwork_model import UserModel

# set-up logging for users.py
logger.remove()
logger.add("log_file_{time:YYYY_MMM_DD}.log")
# logger.add(sys.stderr, level="ERROR")
# logger.info("users.py is imported")
# logger.error("Problem here users.py")
# logger.debug("Debug here users.py")


class UserCollection:
    """
    Contains a collection of Users objects
    """

    def __init__(self, database):
        self.database = database
        logger.debug("user database created and linked")

    def add_user(self, user_id, email, user_name, user_last_name):
        """
        Adds a new user to the collection
        """
        try:
            with self.database.transaction():
                result = UserModel.create(
                    user_id=user_id,
                    user_email=email,
                    user_name=user_name,
                    user_last_name=user_last_name,
                )
                result.save()
                # logger.info("User ID %s successfully added", user_id)
                return True
        except IntegrityError:
            logger.debug("User ID %s already exists", user_id)
            return False

    def modify_user(self, user_id, email, user_name, user_last_name):
        """
        Modifies an existing user
        """
        with self.database.transaction():
            result = self.search_user(user_id)
            if result:
                result.user_email = email
                result.user_name = user_name
                result.user_last_name = user_last_name
                result.save()
                logger.debug("User ID %s successfully modified", user_id)
                return True
            logger.debug("User ID %s does not exist", user_id)
            return False

    def delete_user(self, user_id):
        """
        Deletes an existing user
        """
        with self.database.transaction():
            result = self.search_user(user_id)
            if result:
                result.delete_instance()
                logger.debug("User ID %s successfully deleted", user_id)
                return True
            logger.debug("User ID %s cannot be deleted as it does not exist", user_id)
            return False

    def search_user(self, user_id):
        """
        Searches for user data
        """
        try:
            with self.database.transaction():
                result = UserModel.get(UserModel.user_id == user_id)
                logger.debug("User ID %s found", user_id)
                return result
        except DoesNotExist:
            logger.debug("User ID %s cannot be found", user_id)
            return False
