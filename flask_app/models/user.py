from flask import flash
from re import compile
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask_app.models import chore
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
# PASSWORD_REGEX = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")


class User:
    _db = "housemates_db"

    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.full_name = data["full_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.favorite_movie = data["favorite_movie"]
        self.hobby = data["hobby"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.chores = []

    @staticmethod
    def register_form_is_valid(form_data):
        """This method validates the registration form."""

        is_valid = True

        if len(form_data["username"].strip()) == 0:
            flash("Please enter first name.", "register")
            is_valid = False
        elif len(form_data["username"].strip()) < 2:
            flash("First name must be at least two characters", "register")
            is_valid = False

        if len(form_data["full_name"].strip()) == 0:
            flash("Please enter last name.", "register")
            is_valid = False
        elif len(form_data["full_name"].strip()) < 2:
            flash("Last name must be at least two characters", "register")
            is_valid = False

        if len(form_data["email"].strip()) == 0:
            flash("Please enter email.", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email address invalid.", "register")
            is_valid = False

        if len(form_data["password"].strip()) == 0:
            flash("Please enter password.", "register")
            is_valid = False
        elif len(form_data["password"].strip()) < 8:
            flash("Password must be at least eight characters.", "register")
            is_valid = False
        elif form_data["password"] != form_data["confirm_password"]:
            flash("Passwords do not match.", "register")
            is_valid = False

        if len(form_data["favorite_movie"].strip()) == 0:
            flash("Please enter favorite movie.", "register")
            is_valid = False
        elif len(form_data["favorite_movie"].strip()) < 2:
            flash("Movie title must be at least two characters", "register")
            is_valid = False

        if len(form_data["hobby"].strip()) == 0:
            flash("Please enter hobby.", "register")
            is_valid = False
        elif len(form_data["hobby"].strip()) < 2:
            flash("Hobby must be at least two characters", "register")
            is_valid = False

        return is_valid

    @staticmethod
    def login_form_is_valid(form_data):
        """This method validates the login form."""

        is_valid = True

        if len(form_data["email"].strip()) == 0:
            flash("Please enter email.", "login")
            is_valid = False
        elif not EMAIL_REGEX.match(form_data["email"]):
            flash("Email address invalid.", "login")
            is_valid = False

        if len(form_data["password"].strip()) == 0:
            flash("Please enter password.", "login")
            is_valid = False
        elif len(form_data["password"].strip()) < 8:
            flash("Password must be at least eight characters.", "login")
            is_valid = False

        return is_valid

    @classmethod
    def register(cls, user_data):
        """This method creates a new user in the database"""

        query = """
        INSERT INTO users
        (username, full_name, email, password, favorite_movie, hobby)
        VALUES
        (%(username)s, %(full_name)s, %(email)s, %(password)s, %(favorite_movie)s, %(hobby)s);
        """

        user_id = connectToMySQL(User._db).query_db(query, user_data)
        return user_id

    @classmethod
    def find_all_users(cls):
        """Find all users in the DB"""

        query = "SELECT * FROM users;"
        list_of_dicts = connectToMySQL(User._db).query_db(query)

        print("************** ALL USERS **************")
        pprint(list_of_dicts)
        print("************** ALL USERS **************")

        users = []
        for each_dict in list_of_dicts:
            user = User(each_dict)
            users.append(user)
        return users

    @classmethod
    def find_by_email(cls, email):
        """Finds a user by email."""

        query = """SELECT * FROM users WHERE email = %(email)s;"""
        data = {"email": email}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user

    @classmethod
    def find_by_id(cls, user_id):
        """Finds a user by user_id."""

        query = """SELECT * FROM users WHERE id = %(user_id)s;"""
        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)
        if len(list_of_dicts) == 0:
            return None
        user = User(list_of_dicts[0])
        return user

    @classmethod
    def find_by_id_with_chores(cls, user_id):
        """Finds one user by id and related chores in the database."""

        query = """
        SELECT * FROM users
        LEFT JOIN chores 
        ON users.id = chores.user_id
        WHERE users.id = %(user_id)s;
        """
        data = {"user_id": user_id}
        list_of_dicts = connectToMySQL(User._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pprint(list_of_dicts[0])
        user = User(list_of_dicts[0])
        for each_dict in list_of_dicts:
            if each_dict["chore.id"] != None:
                chore_data = {
                    "id": each_dict["chores.id"],
                    "chore_title": each_dict["chores.chore_title"],
                    "due_date": each_dict["chores.due_date"],
                    "complete": each_dict["chores.complete"],
                    "chore_description": each_dict["chores.chore_description"],
                    "estimated_time": each_dict["chores.estimated_time"],
                    "roommate_points": each_dict["chores.roommate_points"],
                    "created_at": each_dict["chores.created_at"],
                    "updated_at": each_dict["chores.updated_at"],
                    "user_id": each_dict["user_id"],
                }
            chore = chore.Chore(chore_data)
            user.chores.append(chore)

        return user
