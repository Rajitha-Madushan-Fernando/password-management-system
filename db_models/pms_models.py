from database_config import *
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json
import os


# Initializing our database
db = SQLAlchemy(app)

# the class Password will inherit the db.Model of SQLAlchemy
class PasswordList(db.Model):
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128))
    user_id = db.Column(db.Integer())
    app_id = db.Column(db.Integer())

   
   
    def add_app_pwd(_password,_app_id,_user_id):

        # creating an instance of our password constructor
        new_pwd = PasswordList(password=_password, app_id=_app_id, user_id=_user_id)
        db.session.add(new_pwd)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_pwd

    def get_all_password(_user_id):
        #function to get all pwd in our database to related particular user
        return [PasswordList.json(password) for password in PasswordList.query.filter(PasswordList.user_id==_user_id).all()]

    def json(self):
        return {
            #'id': self.id,
            'password': "Hide",
            'app_id': self.app_id,
            #'user_id': self.user_id
        }

# the class legacy app will inherit the db.Model of SQLAlchemy
class LegacyApp(db.Model):
    __tablename__ = 'tbl_legacy_application_list'
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(128))
    

    def add_new_legacy_app(_app_name):
        # creating an instance of our password constructor
        new_legacy_app = LegacyApp(app_name=_app_name)
        db.session.add(new_legacy_app)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_legacy_app

    def get_all_legacy_app():
        #function to get all pwd in our database to related particular user
        return [LegacyApp.json(legacyApp) for legacyApp in LegacyApp.query.all()]

    def json(self):
        return {
            'id': self.id,
            'app_name': self.app_name
        }

# the class User app will inherit the db.Model of SQLAlchemy
class UserList(db.Model):
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(20))
    
    

    
    def add_new_user(_username,_password,_email,_role):
        # creating an instance of our password constructor
        new_user = UserList(role=_role,username=_username,password=_password,email=_email)
        db.session.add(new_user)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_user
    
    def get_all_users():
        #function to get all pwd in our database to related particular user
        #selected_list = ['id','username','email','role']
        #user_list =UserList.query.with_entities(UserList.id, UserList.username).all()
        user_list= [UserList.json(userApp) for userApp in UserList.query.all()]
        return user_list
    
    def check_login(_email,):
        user = UserList.query.filter_by(email=_email).first()
        if user is None:
            print("-------")
            return False
        else:
            return user

  
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': "Hide",
            'email': self.email,
            'role': self.role
        }

   