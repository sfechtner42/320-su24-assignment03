"""
Unittests for main.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock

from peewee import SqliteDatabase

import main
from socialnetwork_model import StatusModel
from user_status import UserStatusCollection


class TestMainUserFunctions(unittest.TestCase):
    """
    testing class for main.py accounts functions
    """

    def setUp(self):
        """
        set up for testing
        """
        self.mock_user_collection = Mock()

    def test_init_user_collection(self):
        """
        test initializing user collection
        """
        with patch("users.UserCollection") as mock_user_collection:
            collection = main.init_user_collection()
            mock_user_collection.assert_called_once()
            self.assertIsNotNone(collection)

    def test_load_users_success(self):
        """
        test loading users into database from csv file
        """
        mock_dictreader = MagicMock()
        mock_dictreader.__iter__.return_value = [
            {
                "USER_ID": "Test",
                "EMAIL": "test@uw.edu",
                "NAME": "Test",
                "LASTNAME": "Test",
            },
            {
                "USER_ID": "SF",
                "EMAIL": "safe@uw.edu",
                "NAME": "Sabrina",
                "LASTNAME": "Fechtner",
            },
        ]

        with patch("builtins.open", create=True), patch(
            "csv.DictReader", return_value=mock_dictreader
        ), patch("main.UserModel.insert_many") as mock_insert_many, patch(
            "main.db.atomic", MagicMock()
        ):
            result = main.load_users("test.csv")
            self.assertTrue(result)
            mock_insert_many.assert_called_once()
            self.assertEqual(
                mock_insert_many.call_args[0][0],
                [
                    {
                        "user_id": "Test",
                        "user_email": "test@uw.edu",
                        "user_name": "Test",
                        "user_last_name": "Test",
                    },
                    {
                        "user_id": "SF",
                        "user_email": "safe@uw.edu",
                        "user_name": "Sabrina",
                        "user_last_name": "Fechtner",
                    },
                ],
            )

    def test_load_users_failure(self):
        """
        test error loading users into database from csv file
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = main.load_users("nonexistent.csv")
            self.assertFalse(result)

    def test_add_user(self):
        """
        test adding user to database
        """
        self.mock_user_collection.add_user.return_value = True
        result = main.add_user(
            "SC", "sesame@uw.edu", "Sesame", "Chan", self.mock_user_collection
        )
        self.assertTrue(result)
        self.mock_user_collection.add_user.assert_called_once_with(
            "SC", "sesame@uw.edu", "Sesame", "Chan"
        )

    def test_update_user(self):
        """
        test updating user in database
        """
        self.mock_user_collection.modify_user.return_value = True
        result = main.update_user(
            "SC", "newemail@uw.edu", "Sesame", "Chan", self.mock_user_collection
        )
        self.assertTrue(result)
        self.mock_user_collection.modify_user.assert_called_once_with(
            "SC", "newemail@uw.edu", "Sesame", "Chan"
        )

    def test_delete_user(self):
        """
        test deleting user in database
        """
        self.mock_user_collection.delete_user.return_value = True
        result = main.delete_user("SF", self.mock_user_collection)
        self.assertTrue(result)
        self.mock_user_collection.delete_user.assert_called_once_with("SF")

    def test_search_user(self):
        """
        test searching user in database
        """
        user_mock = Mock(user_id="SF")
        self.mock_user_collection.search_user.return_value = user_mock
        result = main.search_user("SF", self.mock_user_collection)
        self.assertEqual(result.user_id, "SF")


class TestMainStatusFunctions(unittest.TestCase):
    """
    testing class for main.py for status functions
    """

    def setUp(self):
        """
        set up for testing
        """
        self.mock_status_collection = Mock()

    def test_init_status_collection(self):
        """
        test initializing status collection
        """
        with patch("user_status.UserStatusCollection") as mock_status_collection:
            collection = main.init_status_collection()
            mock_status_collection.assert_called_once()
            self.assertIsNotNone(collection)

    def test_load_status_updates_success(self):
        """
        test loading status updates into database from csv file
        """
        # Set up an in-memory SQLite database
        database = SqliteDatabase(":memory:")
        database.bind([StatusModel])
        database.connect()
        database.create_tables([StatusModel])

        # Create an instance of UserStatusCollection with the in-memory database
        UserStatusCollection(database)

        # Mock data and setup for foreign key table
        mock_user_model = MagicMock()
        mock_user_model.select.return_value = [{"user_id": "SF"}]

        # Mock csv.DictReader to simulate reading from CSV
        mock_dictreader = MagicMock()
        mock_dictreader.__iter__.return_value = [
            {"STATUS_ID": "SF1", "USER_ID": "SF", "STATUS_TEXT": "Hello"},
            {"STATUS_ID": "SF2", "USER_ID": "SF", "STATUS_TEXT": "World!"},
        ]

        # Mock database atomic and StatusModel insert
        with patch("builtins.open", create=True), patch(
            "csv.DictReader", return_value=mock_dictreader
        ), patch("main.db.atomic"), patch(
            "main.StatusModel.insert_many"
        ) as mock_insert_many, patch(
            "main.UserModel", mock_user_model
        ):

            result = main.load_status_updates("test_status.csv")
            self.assertTrue(result)
            self.assertEqual(mock_insert_many.call_count, 1)

        # Clean up the in-memory database
        database.drop_tables([StatusModel])
        database.close()

    def test_load_status_updates_failure(self):
        """
        test error loading status updates into database from csv file
        """
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = main.load_status_updates("nonexistent.csv")
            self.assertFalse(result)

    def test_add_status(self):
        """
        test adding status to database
        """
        self.mock_status_collection.add_status.return_value = True
        result = main.add_status(
            "SF", "status1", "Hello World!", self.mock_status_collection
        )
        self.assertTrue(result)
        self.mock_status_collection.add_status.assert_called_once_with(
            "status1", "SF", "Hello World!"
        )

    def test_update_status(self):
        """
        test updating status in database
        """
        self.mock_status_collection.modify_status.return_value = True
        result = main.update_status(
            "status1", "SF", "Updated Status!", self.mock_status_collection
        )
        self.assertTrue(result)
        self.mock_status_collection.modify_status.assert_called_once_with(
            "status1", "SF", "Updated Status!"
        )

    def test_delete_status(self):
        """
        test deleting status in database
        """
        self.mock_status_collection.delete_status.return_value = True
        result = main.delete_status("status1", self.mock_status_collection)
        self.assertTrue(result)
        self.mock_status_collection.delete_status.assert_called_once_with("status1")

    def test_search_status(self):
        """
        test searching status in database
        """
        status_mock = Mock(status_id="status1")
        self.mock_status_collection.search_status.return_value = status_mock
        result = main.search_status("status1", self.mock_status_collection)
        self.assertEqual(result.status_id, "status1")


if __name__ == "__main__":
    unittest.main()
