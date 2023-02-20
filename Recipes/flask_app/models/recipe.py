from flask_app.config.mysqlconnection import MySQLConnection
from flask import flash

db = 'mydb'
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description= data['description']
        self.instructions = data['instructions']
        self.date = data['date_made']
        self.under_30= data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    def update(self, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date)s, under_30 = %(under_30)s, updated_at = NOW() WHERE id = %(id)s"
        if(data['under_30'] == 'False'):
            data['under_30'] = 0
        else:
            data['under_30'] = 1
            

        MySQLConnection(db).query_db(query, data)

        return self
    def delete(self):
        query = f"DELETE FROM recipes WHERE id = {self.id}"

        MySQLConnection(db).query_db(query)
        
    @classmethod
    def addRecipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30, created_at, updated_at, user_id) Values(%(name)s, %(description)s, %(instructions)s, %(date)s, %(under_30)s, NOW(), NOW(), %(user_id)s)"

        id = MySQLConnection(db).query_db(query, data)
        
        if(id):
            print('successfully added recipe to database')
            return id
        else:
            print("Didn't add to database")
            return False

    @staticmethod
    def validateRecipe(data):
        is_valid = True
        # Validates name
        if len(data['name']) < 3:
            flash('Name has to be longer than 2 characters', 'name')
            is_valid = False
        
        # Validates description
        if len(data['description']) < 1:
            flash('Must have description', 'description')
            is_valid = False
        
        # Validates instructions
        if len(data['instructions']) < 1:
            flash('Must have instructions', 'instruction')
            is_valid = False

        # Validates date_made
        if not data["date"]:
            flash('Must set Date', 'date')
            is_valid = False

        return is_valid

    @classmethod
    def getRecipe(cls, id):
        query = "SELECT * from recipes WHERE id = %(id)s"

        data = {
            'id': id
        }

        results = MySQLConnection(db).query_db(query, data)

        if(results):
            recipe = cls(results[0])
            return recipe
        else:
            return False

    @classmethod
    def getAllRecipes(cls):
        query = "Select * from recipes"
        
        results = MySQLConnection(db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        
        return recipes