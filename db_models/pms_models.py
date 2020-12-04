from database_config import *
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship



# Initializing our database
db = SQLAlchemy(app)

# the class Password will inherit the db.Model of SQLAlchemy
class PasswordList(db.Model):
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128))
    user_id = db.Column(db.String(11))
    app_id = db.Column(db.Integer(), db.ForeignKey('tbl_legacy_application_list.id'))

    def json(self):
        return {
            'id': self.id,
            'password': self.password,
            'app_id': self.app_id,
            'user_id': self.user_id
        }
   
    def add_app_pwd(_password,_app_id,_user_id):

        # creating an instance of our password constructor
        new_pwd = PasswordList(password=_password, app_id=_app_id, user_id=_user_id)
        db.session.add(new_pwd)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_pwd

    def get_all_password():
        #function to get all pwd in our database to related particular user
        return [PasswordList.json(passwordList) for passwordList in PasswordList.query.all()]


# the class legacy app will inherit the db.Model of SQLAlchemy
class LegacyApp(db.Model):
    __tablename__ = 'tbl_legacy_application_list'
    id = db.Column(db.Integer, primary_key=True)
    app_name = db.Column(db.String(128))
    


    def json(self):
        return {
            'id': self.id,
            'name': self.app_name
        }

    def add_new_legacy_app(_app_name):
        # creating an instance of our password constructor
        new_legacy_app = LegacyApp(app_name=_app_name)
        db.session.add(new_legacy_app)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_legacy_app

    def get_all_legacy_app():
        #function to get all pwd in our database to related particular user
        return [LegacyApp.json(legacyApp) for legacyApp in LegacyApp.query.all()]


# the class User app will inherit the db.Model of SQLAlchemy
class UserList(db.Model):
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(20))
    
    

    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'role': self.role
        }

    def add_new_user(_username,_password,_email,_role):
        # creating an instance of our password constructor
        new_user = UserList(role=_role,username=_username,password=_password,email=_email)
        db.session.add(new_user)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_user
    
    def get_all_users():
        #function to get all pwd in our database to related particular user
        return [UserList.json(userApp) for userApp in UserList.query.all()]

   