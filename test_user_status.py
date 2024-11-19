"""
Unittests for user_status.py
"""

import unittest
from peewee import SqliteDatabase
import user_status
from socialnetwork_model import UserModel, StatusModel


class TestUserStatus(unittest.TestCase):
    """
    Testing class for user_status.py
    """

    def setUp(self):
        """
        Set up to create mock database
        """
        # set up database to be used in tests below
        self.database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
        self.database.bind([UserModel, StatusModel])
        self.database.connect()
        self.database.create_tables([UserModel, StatusModel])
        self.status_collection = user_status.UserStatusCollection(self.database)
        user_id = "testuser"
        email = "test@user.com"
        user_name = "test"
        user_last_name = "user"
        with self.database.transaction():
            result = UserModel.create(
                user_id=user_id,
                user_email=email,
                user_name=user_name,
                user_last_name=user_last_name,
            )
            result.save()
        test_status_id = "testuser-1"
        test_id = "testuser"
        test_text = "My first status post"
        self.status_collection.add_status(test_status_id, test_id, test_text)

    def tearDown(self):
        """
        tear down function to reset database
        """
        self.database.drop_tables([UserModel, StatusModel])
        self.database.close()

    def test_add_valid_status(self):
        """
        test to add status
        """
        test_status_id = "testuser-2"
        test_id = "testuser"
        test_text = "this is my second entry!"
        result = self.status_collection.add_status(test_status_id, test_id, test_text)
        self.assertEqual(result, True)

    def test_add_duplicate_status(self):
        """
        test to add status with duplicate ID
        """
        test_status_id = "testuser-1"
        test_id = "testuser"
        test_text = "My first status post"
        result = self.status_collection.add_status(test_status_id, test_id, test_text)
        self.assertEqual(result, False)

    def test_add_status_no_foreign_key(self):
        """
        test to add without a foreign key
        """
        test_status_id = "testuser-1"
        test_id = "testuserdoesnotexist"
        test_text = "My first status post"
        result = self.status_collection.add_status(test_status_id, test_id, test_text)
        self.assertEqual(result, False)

    def test_modify_valid_status(self):
        """
        test to modify valid status
        """
        modify_status_id = "testuser-1"
        modified_id = "testuser"
        modified_text = "My first modified post"
        result = self.status_collection.modify_status(
            modify_status_id, modified_id, modified_text
        )
        self.assertEqual(result, True)

    def test_modify_invalid_status(self):
        """
        test to modify invalid status
        """
        modify_status_id = "testuser-99999"
        modified_id = "testuser"
        modified_text = "this better not work"
        result = self.status_collection.modify_status(
            modify_status_id, modified_id, modified_text
        )
        self.assertEqual(result, False)

    def test_modify_status_no_foreign_key(self):
        """
        test to modify status with no foreign key
        """
        modify_status_id = "testuser-1"
        modified_id = "testuserthatDNE"
        modified_text = "this better not work"
        result = self.status_collection.modify_status(
            modify_status_id, modified_id, modified_text
        )
        self.assertEqual(result, False)

    def test_delete_valid_status(self):
        """
        test to delete valid status
        """
        # status id to delete
        delete_status_id = "testuser-1"
        result = self.status_collection.delete_status(delete_status_id)
        self.assertEqual(result, True)

    def test_delete_invalid_status(self):
        """
        test to delete invalid status
        """
        delete_status_id = "testuser-99999"
        result = self.status_collection.delete_status(delete_status_id)
        self.assertEqual(result, False)

    def test_search_valid_status(self):
        """
        test to search valid status
        """
        search_status_id = "testuser-1"
        result = self.status_collection.search_status(search_status_id)
        self.assertEqual(result.status_id, search_status_id)

    def test_search_invalid_status(self):
        """
        test to search invalid status
        """
        search_status_id = "testuser-99999"
        result = self.status_collection.search_status(search_status_id)
        self.assertEqual(result, False)
