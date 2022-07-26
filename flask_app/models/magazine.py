from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import EMAIL_REGEX, DATABASE
from flask_app.models.user import User


class Magazine:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_magazine(data):
        is_valid = True
        
        if not len(data['name']) >= 2:
            flash("Name must be a minimum of 2 characters!", "error_registration_name")
            is_valid = False

        if not len(data['description']) >= 10:
            flash("Description must be a minimum of 10 characters!", "error_registration_description")
            is_valid = False

        return is_valid

    @classmethod
    def create_magazine(cls, data):
        query = "INSERT INTO magazines (name, description, user_id) VALUES (%(name)s, %(description)s, %(user_id)s);" 

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def get_all_magazines(cls):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id;"

        result = connectToMySQL(DATABASE).query_db(query)
        magazines = []
        for row in result:
            user_data = {
            "id" : row["users.id"],
            "first_name" : row["first_name"],
            "last_name" : row["last_name"],
            "email" : row["email"],
            "password" : row["password"],
            "created_at" : row["users.created_at"],
            "updated_at" : row["users.updated_at"]
        }
            created_by = User(user_data)
            magazine = cls(row)
            magazine.user = created_by
            magazines.append(magazine)
        
        print(magazines)
        return magazines

    
    @classmethod
    def get_single_magazine(cls, data):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE magazines.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        row = result[0]
        #create data table for users table. For matching titles, use dot nation of actual table.
        user_data = {
                    "id" : row["users.id"],
                    "first_name" : row["first_name"],
                    "last_name" : row["last_name"],
                    "email" : row["email"],
                    "password" : row["password"],
                    "created_at" : row["users.created_at"],
                    "updated_at" : row["users.updated_at"]
                }
        created_by = User(user_data)
        magazine = cls(row)
        magazine.user = created_by
        return magazine

    @classmethod
    def delete_magazine(cls, data):

        
        query1 = "DELETE FROM subscription WHERE magazine_id = %(id)s;"
        connectToMySQL(DATABASE).query_db(query1, data)

        query = "DELETE FROM magazines WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_users_magazines(cls, data):
        query = "SELECT * FROM magazines JOIN users ON magazines.user_id = users.id WHERE users.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        magazines = []
        for row in result:
            user_data = {
            "id" : row["users.id"],
            "first_name" : row["first_name"],
            "last_name" : row["last_name"],
            "email" : row["email"],
            "password" : row["password"],
            "created_at" : row["users.created_at"],
            "updated_at" : row["users.updated_at"]
        }
            created_by = User(user_data)
            magazine = cls(row)
            magazine.user = created_by
            magazines.append(magazine)
        return magazines

    @classmethod
    def get_magazine_subscribers(cls, data):

        query = "SELECT first_name, last_name FROM users LEFT JOIN subscription ON users.id = subscription.user_id LEFT JOIN magazines ON subscription.magazine_id = magazines.id WHERE magazines.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        return result
    
    @classmethod
    def subscribe(cls, data):

        query = "INSERT INTO subscription (magazine_id, user_id) VALUES (%(magazine_id)s, %(user_id)s);"

        return connectToMySQL(DATABASE).query_db(query, data)