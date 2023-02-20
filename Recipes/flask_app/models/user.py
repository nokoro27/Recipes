

from flask_app.models.recipe import Recipe
from flask.helpers import flash
from flask_app.config.mysqlconnection import MySQLConnection
import bcrypt
import re

db = 'mydb'
class User: 
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.recipes = []

    @classmethod
    def insertNewUser(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        data['password'] = cls.encryptPassword(data['password'])

        id = MySQLConnection(db).query_db(query, data)
        
        return id

    @staticmethod
    def validateLogin(data): #returns user if found, else returns False
        user = User.getUserbyEmail(data)

        if not user:
            flash('Did not recognize user email!', 'login')
            return False

        print("USER BEFORE PW CHECK: ", user.password, "DATA FROM FORM: ", data)
        
        #checks the password given to the hashed password stored in database
        pw_check = bcrypt.checkpw(bytes(data["password"], "utf8"), bytes(user.password, 'utf8'))
        print("hashed pw check: ", pw_check )
        if not pw_check:
            flash('Incorrect Password', 'login')
            return False
        
        return user 
    
    @staticmethod
    def validateRegistration(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash('First Name needs more than two characters', 'first_name')
            is_valid = False
        if len(data['last_name']) < 3:
            flash('Last name needs more than two characters', 'last_name')
            is_valid = False

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        if( not EMAIL_REGEX.match(data['email'])):
            flash("Must enter valid email", 'email')
            is_valid = False
        
        #Validates Password:
        if(len(data['confirm_password']) < 8):
            flash("Password must be at least 8 characters", 'password')
            is_valid = False
            
        numberandchar = re.compile(r'^.*[0-9].*')
        if(not numberandchar.match(data['confirm_password'])):
            flash("Password must contain at least 1 number", 'password')
            is_valid = False
        

        return is_valid

    @classmethod
    def getUserbyEmail(cls, data):
        query = "SELECT * from users WHERE email = %(email)s"

        user_fromDB = MySQLConnection(db).query_db(query, data)
        #if is a success, puts the user in an instance instead of list
        if user_fromDB:
            user = cls(user_fromDB[0])

        return user
    
    @classmethod
    def getUserbyId(cls, id):
        query = "SELECT * from users LEFT JOIN recipes On users.id = recipes.user_id WHERE users.id = %(id)s "

        data = {
            'id': id
        }

        user_fromDB = MySQLConnection(db).query_db(query, data)

        #if is a success, puts the user in an instance instead of list
        if user_fromDB:
            user = cls(user_fromDB[0])

            for row in user_fromDB:
                info = {
                    'id' : row['recipes.id'],
                    'name': row['name'],
                    'description': row['description'],
                    'instructions': row['instructions'],
                    'date_made' : row['date_made'],
                    'under_30': row['under_30'],
                    'user_id': row['user_id'],
                    'created_at': row['recipes.created_at'],
                    'updated_at': row['recipes.updated_at']
                    }
                user.recipes.append(Recipe(info))

                print("USER DATA RETURNED: ", user.recipes)
            return user
        else:
            print("Failed to retrieve user from database by Id")
            return False
    
    @classmethod
    def encryptPassword(cls, password):
        #Will return encrypted password via bcrypt
        hashed =bcrypt.hashpw(bytes(password, "utf8"), bcrypt.gensalt(14))
        return hashed