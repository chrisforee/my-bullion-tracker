from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models.user_model import User

class Bullion:
    def __init__(self, data):
        self.id = data['id']
        self.description = data['description']
        self.amount = data['amount']
        self.type = data['type']
        self.weight = data['weight']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.date_purchased = data['date_purchased']
        self.purchased_from = data['purchased_from']
        self.location_held = data['location_held']

 #Class method to create a query to retireve all sightings with users
    @classmethod
    def get_all_with_users(cls): #<============== not retreiving anything from routes so no 'data' needed
        query = "SELECT * "
        query += "FROM bullion "
        query += "JOIN users ON bullion.user_id = users.id;"
        # This code snippet will create an instance for each recipe and inside each recipe will be an instance of the user to be displayed on the template
        results = connectToMySQL(DATABASE).query_db(query) #<=========== Results will provide data from db
        list_bullions = [] #<========= create list to provide instances of sightings
        for row in results: #<============== iterate through the rows in the data returned 
            current_bullion = cls(row) #<========= create the recipe instance
            user_data = { #<====== create the user data from the above query
                **row, 
                "created_at" : row['users.created_at'],
                "updated_at" : row['users.updated_at'],
                "id" : row['users.id']
            }
            current_user = User(user_data) #<======instance of user is created from User class
            current_bullion.user = current_user #<=======combining both instances from recipe and user
            list_bullions.append(current_sighting) #<======= append list of sightings 
        return list_bullions #<===== list to be sent back to controller

    #Class method to create an INSERT query to place a sighting into the database
    @classmethod
    def create(cls, data):
        query = "INSERT INTO bullion( description, amount, type, weight, date_purchased, purchased_from, location_held, user_id )"
        query += "VALUES ( %(description)s, %(amount)s, %(type)s, %(weight)s, %(date_purchased)s, %(purchased_from)s, %(location_held)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data) #<=========================== Will send back id of the created/inserted recipe

    # Class method to create a query to retireve one sighting by id with user
    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * "
        query += "FROM bullion "
        query += "JOIN users ON bullion.user_id = users.id "
        query += "WHERE bullion.id = %(id)s;"
        
        result = connectToMySQL(DATABASE).query_db(query, data)
        if len(result) > 0: #<=====validating a result was returned
            current_bullion = cls(result[0]) #<====== creating the current sighting instance from query to be sent to controller then to be sent to template
            user_data = {
                **result[0], 
                "created_at" : result[0]['users.created_at'],
                "updated_at" : result[0]['users.updated_at'],
                "id" : result[0]['users.id']
            }
            current_bullion.user = User(user_data) #<========== created instance of user object to display on template
            return current_bullion
        else:
            return None

    # Class method to create an UPDATE query to update sightings
    @classmethod
    def update_one(cls, data):
        query = "UPDATE bullion "
        query += "SET description = %(description)s, amount = %(amount)s, type = %(type)s, weight = %(weight)s, date_purchased = %(date_purchased)s, location_held = %(location_held)s "
        query += "WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one(cls, data):
        query = "DELETE FROM bullion "
        query += "WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Static method to validate for empty inputs in html form
    @staticmethod
    def validate_bullion(data):
        is_valid = True
        # First set of validations for empty fields
        if data['description'] == "":
            flash("Description required", "error_bullion_description")
            is_valid = False
        if data['amount'] == "":
            flash("Amount required", "error_bullion_amount")
            is_valid = False
        if data['type'] == "":
            flash("Type required", "error_bullion_type")
            is_valid = False
        if data['weight'] == "":
            flash("Weight required", "error_bullion_weight")
            is_valid = False
        if data['date_purchased'] == "":
            flash("Date purchased required", "error_bullion_date_purchased")
            is_valid = False
        if data['purchased_from'] == "":
            flash("Purchased from required", "error_bullion_purchased_from")
            is_valid = False
        if data['location_held'] == "":
            flash("Location held required", "error_bullion_location_held")
            is_valid = False                        
        return is_valid            