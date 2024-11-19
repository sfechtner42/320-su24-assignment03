"""
Unittests users.py
"""

import unittest
from peewee import SqliteDatabase
import users
from socialnetwork_model import UserModel


class TestUsers(unittest.TestCase):
    """
    Testing class for users.py
    """

    def setUp(self):
        """
        create testing database in memory
        """
        self.database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
        self.database.bind([UserModel])
        self.database.connect()
        self.database.create_tables([UserModel])
        self.user_collection = users.UserCollection(self.database)
        # create test user to add to database
        user_id = "testuser"
        email = "test@user.com"
        user_name = "test"
        user_last_name = "user"
        self.user_collection.add_user(user_id, email, user_name, user_last_name)

    def tearDown(self):
        """
        tear down to reset database
        """
        self.database.drop_tables([UserModel])
        self.database.close()

    def test_user_add_valid_user(self):
        """
        test adding user to database
        """
        test_id = "anothertestuser"
        test_email = "anothertest@user.com"
        test_name = "anothertest"
        test_last_name = "user"
        result = self.user_collection.add_user(
            test_id, test_email, test_name, test_last_name
        )
        self.assertEqual(result, True)

    def test_user_add_invalid_user(self):
        """
        test to add invalid user to database
        """
        test_id = "testuser"
        test_email = "test@user.com"
        test_name = "test"
        test_last_name = "user"
        result = self.user_collection.add_user(
            test_id, test_email, test_name, test_last_name
        )
        self.assertEqual(result, False)

    def test_user_modify_valid_user(self):
        """
        test to modify user in database
        """
        modify_id = "testuser"
        modified_email = "testuser@uw.edu"
        modified_name = "test"
        modified_last_name = "user"
        result = self.user_collection.modify_user(
            modify_id, modified_email, modified_name, modified_last_name
        )
        self.assertEqual(result, True)

    def test_user_modify_invalid_user(self):
        """
        test to modify invalid user in database
        """
        # create bad id with data
        modify_id = "faketestuser"
        modified_email = "faketest@user.com"
        modified_name = "faketest"
        modified_last_name = "user"
        result = self.user_collection.modify_user(
            modify_id, modified_email, modified_name, modified_last_name
        )
        self.assertEqual(result, False)

    def test_user_delete_valid_user(self):
        """
        test to delete user in database
        """
        delete_id = "testuser"
        result = self.user_collection.delete_user(delete_id)
        self.assertEqual(result, True)

    def test_user_delete_invalid_user(self):
        """
        test to delete invalid user in database
        """
        delete_id = "faketestuser"
        result = self.user_collection.delete_user(delete_id)
        self.assertEqual(result, False)

    def test_user_search_valid_user(self):
        """
        test to search user in database
        """
        search_id = "testuser"
        result = self.user_collection.search_user(search_id)
        self.assertEqual(result.user_id, search_id)

    def test_user_search_invalid_user(self):
        """
        test to search invalid user in database
        """
        search_id = "nonexistent"
        result = self.user_collection.search_user(search_id)
        self.assertEqual(result, False)
