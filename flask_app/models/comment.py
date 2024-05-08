from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint

# from flask_app.models.user import User


class Comment:
    _db = "housemates_db"

    # this constructor accepts a dictionary as input
    def __init__(self, data):
        self.id = data["id"]
        self.comment = data["comment"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.chore_id = data["chore_id"]
        self.user_id = data["user_id"]

    @classmethod
    def create(cls, form_data):
        """Creates a new comment from a form"""

        query = """
        INSERT INTO comments
        (comment, user_id, chore_id)
        VALUES (%(comment)s, %(user_id)s, %(chore_id)s);
        """
        connectToMySQL(Comment._db).query_db(query, form_data)
        return

    @classmethod
    def delete(clas, form_data):
        """Deletes a chore from the database"""

        query = """
        DELETE FROM comments 
        WHERE user_id=%(user_id)s
        AND chore_id = %(chore_id)s;
        """
        connectToMySQL(Comment._db).query_db(query, form_data)
        return
