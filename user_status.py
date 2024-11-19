"""
classes to manage the user status messages
"""

from peewee import IntegrityError, DoesNotExist
from loguru import logger
from socialnetwork_model import StatusModel


# set-up logging for user_status.py
# logger.remove()
# logger.add("log_file_{time:YYYY_MMM_DD}.log")
# logger.add(sys.stderr, level="ERROR")


class UserStatusCollection:
    """
    Collection of UserStatus messages
    """

    def __init__(self, database):
        self.database = database
        logger.debug("user database created and linked")

    def add_status(self, status_id, user_id, status_text):
        """
        add a new status message to the collection
        """
        try:
            with self.database.transaction():
                result = StatusModel.create(
                    status_id=status_id, user_id=user_id, status_text=status_text
                )
                result.save()
                # logger.debug("Status ID %s successfully added", status_id)
                return True
        except IntegrityError:
            # logger.debug("Status ID %s cannot be added", status_id)
            return False

    def modify_status(self, status_id, user_id, status_text):
        """
        Modifies a status message
        """
        try:
            with self.database.transaction():
                result = self.search_status(status_id)
                if result:
                    result.user_id = user_id
                    result.status_text = status_text
                    result.save()
                    logger.info("Status ID %s successfully modified", status_id)
                    return True
                logger.info(
                    "Status ID %s cannot be deleted as it does not exist", status_id
                )
                return False
        except IntegrityError:
            logger.debug("User ID %s status cannot be modified", user_id)
            return False

    def delete_status(self, status_id):
        """
        deletes the status message with id, status_id
        """
        with self.database.transaction():
            result = self.search_status(status_id)
            if result:
                result.delete_instance()
                logger.info("Status ID %s successfully deleted", status_id)
                return True
            logger.debug("Status ID %s does not exist", status_id)
            return False

    def search_status(self, status_id):
        """
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        """
        try:
            with self.database.transaction():
                result = StatusModel.get(StatusModel.status_id == status_id)
                logger.info("Status ID %s successfully found", status_id)
                return result
        except DoesNotExist:
            logger.debug("Status ID %s cannot be found", status_id)
            return False
