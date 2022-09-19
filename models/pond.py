from proj_app import app
from proj_app.config.mysqlconnection import connectToMySQL
from flask import flash
from ..models import player
from flask_sqlalchemy import SQLAlchemy






class Pond:
   db_name = "rink_rat_ronins"
   
   def __init__(self, db_data):
       self.id = db_data['id']
       self.location = db_data['location']
       self.occur = db_data['occur']
       self.description = db_data['description']
       self.photo_upload = db_data ['photo_upload']
       self.player_id = db_data['player_id']
       self.created_at = db_data['created_at']
       self.updated_at = db_data['updated_at']
       self.player = []
       self.creator = None

       
   @classmethod
   def save(cls,data):
        query = "INSERT INTO ponds (location, occur, description, photo_upload, player_id) VALUES (%(location)s,%(occur)s,%(description)s,%(photo_upload)s,%(player_id)s);"
        return connectToMySQL("rink_rat_ronins").query_db(query, data)
    
    
   @classmethod
   def get_all(cls):
       query = "SELECT * FROM ponds LEFT JOIN players ON ponds.player_id= players.id;"
       results = connectToMySQL("rink_rat_ronins").query_db(query)
       if len(results) < 1:
         return []
       ponds = []
       print(results)
       for row in results:
           one_pond = cls(row)
           get_one= {
              "id": row['players.id'],
              "first_name":row['first_name'],
              "last_name":row['last_name'],
              "email":row['email'],
              "password":row['password'],
              "created_at":row['players.created_at'],
              "updated_at":row['players.updated_at'],
              }
           this_pond=player.Player(get_one)
           one_pond.creator=this_pond
           ponds.append(one_pond)
       return ponds

   
   @classmethod
   def get_one_with_players(cls,data):
       query = "SELECT * FROM ponds LEFT JOIN players ON ponds.player_id = players.id WHERE ponds.id = %(id)s;"
       results = connectToMySQL("rink_rat_ronins").query_db(query,data)
       print(results)
       ponds = cls(results[0])
       for row in results:
           p = {
              'id': results[0]['players.id'],
              'first_name': results[0]['first_name'],
              'last_name': results[0]['last_name'],
              'email': results[0]['email'],
              'password': results[0]['password'],
              'created_at': results[0]['players.created_at'],
              'updated_at': results[0]['players.updated_at']
            }
       add_pond=player.Player(p)
       ponds.creator=add_pond
       ponds.player.append( player.Player(p) )
       return ponds

   @classmethod
   def update(cls,data):
       query= "UPDATE ponds SET location=%(location)s,occur=%(occur)s,description=%(description)s,photo_upload=%(photo_upload)s,player_id=%(player_id)s, updated_at=NOW() WHERE id = %(id)s;"
       return connectToMySQL("rink_rat_ronins").query_db(query,data)
     
   @classmethod
   def destroy(cls,data):
       query = "DELETE FROM ponds WHERE id = %(id)s;"
       return connectToMySQL("rink_rat_ronins").query_db(query,data)
   

   @staticmethod
   def validate_pond(pond):
        is_valid = True
        if len(pond['location']) < 3:
            is_valid = False
            flash("Location must be at least 3 characters","pond")
        if len(pond['occur']) == "":
            is_valid = False
            flash("You must add a date","pond")
        if len(pond['description']) < 8:
            is_valid = False
            flash("Add more details to your description","pond")
        return is_valid
