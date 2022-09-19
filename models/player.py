from proj_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class Player:
   db_name = "rink_rat_ronins"
   def __init__(self,data):
       self.id = data['id']
       self.first_name = data['first_name']
       self.last_name = data['last_name']
       self.email = data['email']
       self.password = data['password']
       self.created_at = data['created_at']
       self.updated_at = data['updated_at']
       
   @classmethod
   def save(cls,data):
       query = "INSERT INTO players (first_name, last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
       return connectToMySQL('rink_rat_ronins').query_db(query,data) 
     
   @classmethod 
   def get_all(cls):
       query = "SELECT * FROM players;"
       results = connectToMySQL(cls.db_name).query_db(query)
       players = []
       for row in results:
           players.append( cls(row))
       return players
   
   @classmethod
   def get_by_email(cls,data):
       query = "SELECT * FROM players WHERE email = %(email)s;"
       results = connectToMySQL(cls.db_name).query_db(query,data)
       if len(results) < 1:
           return False
       return cls(results[0])
     
   @classmethod
   def get_one(cls,data):
       query = "SELECT * FROM players WHERE id = %(id)s;"
       results = connectToMySQL(cls.db_name).query_db(query,data)
       return cls( results[0] )

   
     
     
   @staticmethod
   def validate_register(player):
       is_valid = True
       query = "SELECT * FROM players WHERE email = %(email)s;"
       results = connectToMySQL('rink_rat_ronins').query_db(query,player)
       if len(results) >= 1:
           flash("Email already taken.","register")
           is_valid=False
       if not EMAIL_REGEX.match(player['email']):
           flash("Invalid Email!!!", "register")
           is_valid=False
       if len(player['first_name']) < 3:
           flash("First name must be at least 3 characters", "register")
           is_valid=False
       if len(player['last_name']) < 3:
           flash("Last name must be at least 3 characters", "register")
           is_valid=False
       if len(player['password']) < 8:
           flash("Password must be at least 8 characters", "register")
           is_valid=False
       if player['password'] != player['confirm_pw']:
            flash("Passwords don't match","register")
       return is_valid
