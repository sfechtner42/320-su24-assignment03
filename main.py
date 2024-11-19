"""
Main driver for a simple social network project
"""

import csv

from peewee import chunked

import users
import user_status
from socialnetwork_model import db, StatusModel, UserModel


# pylint: disable = E1120
def init_user_collection():
    """
    Creates and returns a new instance of UserCollection
    """
    return users.UserCollection(db)


def init_status_collection():
    """
    Creates and returns a new instance of UserStatusCollection
    """
    return user_status.UserStatusCollection(db)


def load_users(filename):
    """
    Opens a CSV file with user data and adds it to an existing instance of UserCollection
    """
    try:
        with open(filename, encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            user_data = [
                {
                    "user_id": row["USER_ID"],
                    "user_email": row["EMAIL"],
                    "user_name": row["NAME"],
                    "user_last_name": row["LASTNAME"],
                }
                for row in reader
                if all(
                    key in row and row[key]
                    for key in ["USER_ID", "EMAIL", "NAME", "LASTNAME"]
                )
            ]
            if user_data:
                with db.atomic():  # Use transactions
                    for batch in chunked(
                        user_data, 100
                    ):  # Adjust the batch size as needed
                        UserModel.insert_many(batch).execute()
            return True
    except (FileNotFoundError, KeyError):
        return False


def load_status_updates(filename):
    """
    Opens a CSV file with status data and adds it to an existing instance of UserStatusCollection
    or directly to the database using insert_many.
    """
    try:
        with open(filename, encoding="utf-8", newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            status_data = [
                {
                    "status_id": row["STATUS_ID"],
                    "user_id": row["USER_ID"],
                    "status_text": row["STATUS_TEXT"],
                }
                for row in reader
                if all(
                    key in row and row[key]
                    for key in ["STATUS_ID", "USER_ID", "STATUS_TEXT"]
                )
            ]
            if status_data:
                with db.atomic():  # Use transactions
                    for batch in chunked(
                        status_data, 100
                    ):  # Adjust the batch size as needed
                        StatusModel.insert_many(batch).execute()
            return True
    except (FileNotFoundError, KeyError):
        return False


def add_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Creates a new instance of Users and stores it in user_collection
    """
    return user_collection.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    """
    Updates the values of an existing user
    """
    return user_collection.modify_user(user_id, email, user_name, user_last_name)


def delete_user(user_id, user_collection):
    """
    Deletes a user from user_collection.
    """
    return user_collection.delete_user(user_id)


def search_user(user_id, user_collection):
    """
    Searches for a user in user_collection(which is an instance of UserCollection).
    """
    return user_collection.search_user(user_id)


def add_status(user_id, status_id, status_text, status_collection):
    """
    Creates a new instance of UserStatus and stores it in status_collection
    """
    return status_collection.add_status(status_id, user_id, status_text)


def update_status(status_id, user_id, status_text, status_collection):
    """
    Updates the values of an existing status_id
    """
    return status_collection.modify_status(status_id, user_id, status_text)


def delete_status(status_id, status_collection):
    """
    Deletes a status_id from status_collection.
    """
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    """
    Searches for a status in status_collection
    """
    return status_collection.search_status(status_id)
