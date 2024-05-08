from flask import flash
from datetime import datetime
from flask_app.config.mysqlconnection import connectToMySQL
from pprint import pprint
from flask_app.models.user import User


class Event:
    _db = "housemates_db"

    # this constructor accepts a dictionary as input
    def __init__(self, data):
        self.id = data["id"]
        self.setup = data["setup"]
        self.punchline = data["punchline"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None
        self.comments = []

    @staticmethod
    def form_is_valid(form_data):
        """This method validates the registration form."""

        is_valid = True

        if len(form_data["setup"].strip()) == 0:
            flash("Please enter setup.", "register")
            is_valid = False
        elif len(form_data["setup"].strip()) < 2:
            flash("Setup must be at least two characters", "register")
            is_valid = False

        if len(form_data["punchline"].strip()) == 0:
            flash("Please enter punchline.", "register")
            is_valid = False
        elif len(form_data["punchline"].strip()) < 2:
            flash("Punchline must be at least two characters", "register")
            is_valid = False

        # # date validator
        # if len(form_data["release_date"]) == 0:
        #     flash("Please enter release_date.")
        #     is_valid = False
        # else:
        #     try:
        #         datetime.strptime(form_data["release_date"], "%Y-%m-%d")
        #     except:
        #         flash("Invalid release_year.")
        #         is_valid = False

        # # radio button validator
        # if "radio_column" not in form_data:
        #     flash("Please enter radio_column")
        #     is_valid = False
        # elif form_data["radio_column"] not in ["choice1", "choice2"]:
        #     flash("radio_column must be at least three characters.")
        #     is_valid = False

        return is_valid

    @classmethod
    def find_all(cls):
        """Find all events in the DB"""

        query = "SELECT * FROM events;"
        list_of_dicts = connectToMySQL(Event._db).query_db(query)

        print("************** ALL EVENTS **************")
        pprint(list_of_dicts)
        print("************** ALL EVENTS **************")

        events = []
        for each_dict in list_of_dicts:
            event = Event(each_dict)
            events.append(event)
        return events

    @classmethod
    def find_all_with_users(cls):
        """Finds all events with users in the database"""

        query = """
        SELECT * FROM events
        JOIN users
        ON events.user_id = users.id;
        """
        list_of_dicts = connectToMySQL(Event._db).query_db(query)
        pprint(list_of_dicts)

        events = []
        for each_dict in list_of_dicts:
            event = Event(each_dict)
            user_data = {
                "id": each_dict["users.id"],
                "first_name": each_dict["first_name"],
                "last_name": each_dict["last_name"],
                "email": each_dict["email"],
                "password": each_dict["password"],
                "created_at": each_dict["users.created_at"],
                "updated_at": each_dict["users.updated_at"],
            }
            user = User(user_data)
            event.user = user
            events.append(event)
        return events

    @classmethod
    def find_by_id(cls, event_id):
        """Finds one event by id in the database"""

        query = "SELECT * FROM events WHERE id = %(event_id)s;"
        data = {"event_id": event_id}
        list_of_dicts = connectToMySQL(Event._db).query_db(query, data)

        # error handling
        if len(list_of_dicts) == 0:
            return None

        event = Event(list_of_dicts[0])
        return event

    @classmethod
    def find_by_id_with_user(cls, event_id):
        """Finds one event by id and related user in the database."""

        query = """
        SELECT * FROM events
        JOIN users 
        ON events.user_id = users.id
        WHERE events.id = %(event_id)s;
        """
        data = {"event_id": event_id}
        list_of_dicts = connectToMySQL(Event._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pprint(list_of_dicts)
        event = Event(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        event.user = User(user_data)
        return event

    @classmethod
    def find_by_id_with_user_and_comments(cls, event_id):
        """Finds one event by id, the uploader, and the event's comments in the database."""

        query = """
        SELECT * FROM events
        LEFT JOIN comments
        ON events.id = comments.event_id
        JOIN users 
        ON events.user_id = users.id
        WHERE events.id = %(event_id)s;
        """
        data = {"event_id": event_id}
        list_of_dicts = connectToMySQL(Event._db).query_db(query, data)

        if len(list_of_dicts) == 0:
            return None

        pprint(list_of_dicts)
        event = Event(list_of_dicts[0])
        user_data = {
            "id": list_of_dicts[0]["users.id"],
            "first_name": list_of_dicts[0]["first_name"],
            "last_name": list_of_dicts[0]["last_name"],
            "email": list_of_dicts[0]["email"],
            "password": list_of_dicts[0]["password"],
            "created_at": list_of_dicts[0]["users.created_at"],
            "updated_at": list_of_dicts[0]["users.updated_at"],
        }
        event.user = User(user_data)

        for each_dict in list_of_dicts:
            if each_dict["comments.user_id"] != None:
                event.comments.append(each_dict["comments.user_id"])
        return event

    @classmethod
    def create_event(cls, form_data):
        """Inserts a new event from a form"""

        query = """
        INSERT INTO events
        (setup, punchline, user_id)
        VALUES
        (%(setup)s, %(punchline)s, %(user_id)s);
        """
        event_id = connectToMySQL(Event._db).query_db(query, form_data)
        return event_id

    @classmethod
    def update(cls, form_data):
        """Updates a event by their id."""

        query = """
        UPDATE events
        SET
        setup=%(setup)s,
        punchline=%(punchline)s
        WHERE id = %(event_id)s;
        """
        connectToMySQL(Event._db).query_db(query, form_data)
        return

    @classmethod
    def delete_by_id(clas, event_id):
        """Deletes a event from the database"""

        query = "DELETE FROM events WHERE id=(%(event_id)s);"
        data = {"event_id": event_id}
        connectToMySQL(Event._db).query_db(query, data)
        return

    def is_commented_by(self, user_id):
        return user_id in self.comments
