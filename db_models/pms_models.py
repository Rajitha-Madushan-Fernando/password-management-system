from database_config import *
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_json import FlaskJSON, JsonError, json_response, as_json
import os
from flask_restless import APIManager
from sqlalchemy.engine import Engine
from sqlalchemy import event



# Initializing our database
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)


# the class legacy app will inherit the db.Model of SQLAlchemy
class LegacyApp(db.Model):
    __tablename__ = 'tbl_legacy_application_list'
    id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True, unique=True)
    app_name = db.Column(db.String(128), nullable=False )
    

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

# the class Password will inherit the db.Model of SQLAlchemy
class PasswordList(db.Model):
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    password = db.Column(db.String(128))
    user_id = db.Column(db.Integer())
    app_id = db.Column(db.Integer())
    # define relationship
    #tbl_legacy_application_list = db.relationship('LegacyApp')
    #legacyapp = db.relationship('LegacyApp', backref="passwords", uselist=False)

    def add_app_pwd(_password,_user_id,_app_id):

        # creating an instance of our password constructor
        new_pwd = PasswordList(password=_password,user_id=_user_id,app_id=_app_id)
        db.session.add(new_pwd)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_pwd

    def get_all_password(_user_id):
        #function to get all pwd in our database to related particular user
        result = [PasswordList.json(password) for password in PasswordList.query.filter(PasswordList.user_id==_user_id).all()]
        #result =  [PasswordList.json(passwordlist) for passwordlist in PasswordList.query.all()]
        #print (result)
        return result

  
    def json(self):
        return {
            #'id': self.id,
            'password': "Hide",
            'app_name': self.app_id,
            #'user_id': self.user_id
        }


# the class User app will inherit the db.Model of SQLAlchemy
