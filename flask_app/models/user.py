from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app import EMAIL_REGEX, DATABASE

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PW_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters", "error_message_first_name")
            is_valid = False

        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters", "error_message_last_name")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "error_message_email")
            is_valid = False

        if User.get_user_by_email(data):
            flash("Email is already in use!", "error_message_email")
            is_valid = False

        if len(data['password']) < 8:
            flash('Password must be at least 8 characters', "error_message_password")
            is_valid = False

        if data['confirm_password'] != data['password']:
            flash('Confirm your password', "error_message_confirm_password")
            is_valid = False

        return is_valid


    @staticmethod
    def validate_user_edits(data):
        is_valid = True

        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters", "error_message_first_name")
            is_valid = False

        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters", "error_message_last_name")
            is_valid = False

        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "error_message_email")
            is_valid = False

        return is_valid

    @classmethod
    def create_user(cls, data):

        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        
        result = connectToMySQL(DATABASE).query_db(query, data)

        return result
    
    @classmethod
    def get_user_by_email(cls, data):

        query = "SELECT * FROM users WHERE users.email  = %(email)s"

        result = connectToMySQL(DATABASE).query_db(query, data)

        if not result:
            return False

        return cls(result[0])

    @classmethod
    def get_user_to_edit(cls, data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        
        print(result[0])
        return result[0]
    
    @classmethod
    def update_user(cls, data):

        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def users_magazines_count(cls, data):
        query = "SELECT COUNT(subscription.user_id) AS 'subscription', magazines.name, magazines.id FROM magazines LEFT JOIN users ON users.id = magazines.user_id LEFT JOIN subscription ON subscription.magazine_id = magazines.id WHERE magazines.user_id = %(id)s GROUP BY magazines.name;"

        result = connectToMySQL(DATABASE).query_db(query, data)
        print(result)
        return result