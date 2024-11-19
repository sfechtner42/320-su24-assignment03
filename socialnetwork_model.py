"""
implements database as a social network model
"""

# pylint: disable=R0903

from peewee import (
    Model,
    SqliteDatabase,
    CharField,
    ForeignKeyField,
)


db = SqliteDatabase("database.db", pragmas={"foreign_keys": 1})
db.connect()


class BaseModel(Model):
    """
    model that all allows db to be called in with
    """

    class Meta:
        """
        initialize database
        """

        database = db


class UserModel(BaseModel):
    """
    database for users
    """

    user_id = CharField(primary_key=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    user_email = CharField()


class StatusModel(BaseModel):
    """
    database for statuses
    """

    status_id = CharField(primary_key=True, max_length=30)
    user_id = ForeignKeyField(UserModel, backref="statuses", on_delete="CASCADE")
    status_text = CharField(max_length=250)


db.create_tables([UserModel, StatusModel])
db.close()
