from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask_app.models.user import User
from flask_app.models import comment


class Chore:
    _db = "housemates_db"

    # this constructor accepts a dictionary as input
    def __init__(self, data):
        self.id = data["id"]
        self.chore_title = data["chore_title"]
        self.due_date = data["due_date"]
        self.complete = data["complete"]
        self.chore_description = data["chore_description"]
        self.estimated_time = data["estimated_time"]
        self.roommate_points = data["roommate_points"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None
        self.comments = []

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the registration form."""

        is_valid = True

        if len(form_data["chore_title"].strip()) == 0:
            flash("Please enter chore_title.", "register")
            is_valid = False
        elif len(form_data["chore_title"].strip()) < 2:
            flash("Chore title must be at least two characters", "register")
            is_valid = False

        # date validator
        if len(form_data["due_date"]) == 0:
            flash("Please enter due_date.")
            is_valid = False
        else:
            try:
                datetime.strptime(form_data["due_date"], "%Y-%m-%d")
            except:
                flash("Invalid release_year.")
                is_valid = False

        # if len(form_data["user_id"].strip()) == 0:
        #     flash("Please enter user_id.", "register")
        #     is_valid = False
        # elif len(form_data["user_id"].strip()) < 2:
        #     flash("user_id must be at least two characters", "register")
        #     is_valid = False

        # radio button validator
        # if "complete" not in form_data:
        #     flash("Please enter completion status")
        #     is_valid = False
        # elif form_data["complete"] not in ["0", "1"]:
        #     flash("Please select a completion status")
        #     is_valid = False

        if form_data["roommate_points"] not in ["1", "2", "3", "4", "5"]:
            flash("Please select a number 1 through 5")
            is_valid = False

        return is_valid

    @staticmethod
    def update_form_is_valid(form_data):
        """This method validates the registration form."""

        is_valid = True

        if len(form_data["chore_title"].strip()) == 0:
            flash("Please enter chore_title.", "register")
            is_valid = False
        elif len(form_data["chore_title"].strip()) < 2:
            flash("Chore title must be at least two characters", "register")
            is_valid = False

        # date validator
        if len(form_data["due_date"]) == 0:
            flash("Please enter due_date.")
            is_valid = False
        else:
            try:
                datetime.strptime(form_data["due_date"], "%Y-%m-%d")
            except:
                flash("Invalid release_year.")
                is_valid = False

        if form_data["estimated_time"] == "":
            flash("Please select the number of hours this should take")
            is_valid = False

        # number in range validator
        # if form_data["roommate_points"] not in ["1", "2", "3", "4", "5"]:
        #     flash("Please select a number 1 through 5")
        #     is_valid = False

        # radio button validator
        if "complete" not in form_data:
            flash("Please enter completion status")
            is_valid = False
        elif form_data["complete"] not in ["0", "1"]:
            flash("Please select a completion status")
            is_valid = False
        return is_valid

    @classmethod
    def find_all(cls):
        """Find all chores in the DB"""

        query = "SELECT * FROM chores;"
        list_of_dicts = connectToMySQL(Chore._db).query_db(query)

        print("************** ALL CHORES **************")
        pprint(list_of_dicts)
        print("************** ALL CHORES **************")

        chores = []
        for each_dict in list_of_dicts:
            chore = Chore(each_dict)
            chores.append(chore)
        return chores

    @classmethod
    def find_all_with_users(cls):
        """Finds all chores with users in the database"""

        query = """
        SELECT * FROM chores
        JOIN users
        ON chores.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Chore._db).query_db(query)
        pprint(list_of_dicts)

        chores = []
        for each_dict in list_of_dicts:
            chore = Chore(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "username": each_dict["username"],
                "full_name": each_dict["full_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "favorite_movie": each_dict["favorite_movie"],
                "hobby": each_dict["hobby"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            user = user_data  # TESTING CHANGE
            chore.user = user
            chores.append(chore)
        return chores

    @classmethod
    def find_all_with_users_and_comments(cls):
        """Finds all chores with users in the database"""

        query = """
        with cte1 as (
        SELECT chores.id as 'chore_id', count(comments.user_id) as 'number_of_comments'
        FROM chores
        LEFT JOIN comments
        ON chores.id = comments.chore_id
        GROUP BY chores.id
        )
        SELECT chores.*, users.*, cte1.number_of_comments
        FROM chores
        JOIN users
        ON chores.user_id = users.id
        JOIN cte1
        ON chores.id = cte1.chore_id;
        """
        list_of_dicts = connectToMySQL(Chore._db).query_db(query)
        pprint(list_of_dicts)

        chores = []
        for each_dict in list_of_dicts:
            chore = Chore(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            user = user.User(user_data)  # TESTING CHANGE
            chore.user = user
            if each_dict["number_of_comments"] != None:
                chore.comments.append(each_dict["number_of_comments"])
            chores.append(chore)
        return chores

    @classmethod
    def find_by_id(cls, chore_id):
        """Finds one chore by id in the database"""

        query = "SELECT * FROM chores WHERE id = %(chore_id)s;"
        data = {"chore_id": chore_id}
        list_of_dicts = connectToMySQL(Chore._db).query_db(query, data)

        # error handling
        if len(list_of_dicts) == 0:
            return None

        chore = Chore(list_of_dicts[0])
        return chore

    @classmethod
    def find_by_id_with_user(cls, chore_id):
        """Finds one chore by id and related user in the database."""

        query = """
        SELECT * FROM chores
        JOIN users 
        ON chores.user_id = users.id
        WHERE chores.id = %(chore_id)s;
        """
        data = {"chore_id": chore_id}
        list_of_dicts = connectToMySQL(Chore._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pprint(list_of_dicts)
        chore = Chore(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "username": list_of_dicts[0]["username"],
            "full_name": list_of_dicts[0]["full_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "favorite_movie": list_of_dicts[0]["favorite_movie"],
            "hobby": list_of_dicts[0]["hobby"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        chore.user = User(user_data)  # TESTING CHANGE
        return chore

    @classmethod
    def find_by_id_with_comments(cls, chore_id):
        """Finds one chore by id and related comments in the database."""

        query = """
        SELECT * FROM chores
        JOIN comments 
        ON chores.id = comments.chore_id
        WHERE chores.id = %(chore_id)s;
        """
        data = {"chore_id": chore_id}
        list_of_dicts = connectToMySQL(Chore._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pprint(list_of_dicts[0])
        chore = Chore(list_of_dicts[0])
        for each_dict in list_of_dicts:
            if each_dict["comments.id"] != None:
                comment_data = {
                    "id": each_dict["comments.id"],
                    "comment": each_dict["comment"],
                    "created_at": each_dict["comments.created_at"],
                    "updated_at": each_dict["comments.updated_at"],
                    "chore_id": each_dict["chore_id"],
                    "user_id": each_dict["comments.user_id"],
                }
            comment_obj = comment.Comment(comment_data)
            chore.comments.append(comment_obj)

        return chore

    @classmethod
    def find_by_id_with_user_and_comments(cls, chore_id):
        """Finds one chore by id, the uploader, and the chore's comments in the database."""

        query = """
        SELECT * FROM chores
        LEFT JOIN comments
        ON chores.id = comments.chore_id
        JOIN users 
        ON chores.user_id = users.id
        WHERE chores.id = %(chore_id)s;
        """
        data = {"chore_id": chore_id}
        list_of_dicts = connectToMySQL(Chore._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pprint(list_of_dicts)
        chore = Chore(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "username": list_of_dicts[0]["username"],
            "full_name": list_of_dicts[0]["full_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "favorite_movie": list_of_dicts[0]["favorite_movie"],
            "hobby": list_of_dicts[0]["hobby"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        chore.user = User(user_data)  # TESTING CHANGE

        for each_dict in list_of_dicts:
            if each_dict["comments.user_id"] != None:
                chore.comments.append(each_dict["comments.user_id"])
        return chore

    # END OF READ

    # CREATE
    @classmethod
    def create_chore(cls, form_data):
        """Inserts a new chore from a form"""

        query = """
        INSERT INTO chores
        (chore_title, due_date, complete, chore_description, estimated_time, roommate_points, user_id)
        VALUES
        (%(chore_title)s, %(due_date)s, 0, %(chore_description)s, %(estimated_time)s, %(roommate_points)s, %(user_id)s);
        """
        chore_id = connectToMySQL(Chore._db).query_db(query, form_data)
        return chore_id

    @classmethod
    def update(cls, form_data):
        """Updates a chore by their id."""

        query = """
        UPDATE chores
        SET
        chore_title=%(chore_title)s,
        due_date=%(due_date)s,
        complete=%(complete)s,
        chore_description=%(chore_description)s,
        estimated_time=%(estimated_time)s,
        roommate_points=%(roommate_points)s,
        user_id=%(user_id)s
        WHERE id = %(chore_id)s;
        """
        connectToMySQL(Chore._db).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(clas, chore_id):
        """Deletes a chore from the database"""

        query = "DELETE FROM chores WHERE id=(%(chore_id)s);"
        data = {"chore_id": chore_id}
        connectToMySQL(Chore._db).query_db(query, data)
        return

    def is_commented_by(self, user_id):
        return user_id in self.comments
