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





# the class legacy app will inherit the db.Model of SQLAlchemy
class LegacyApp(db.Model):
    __tablename__ = 'tbl_legacy_application_list'
    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    app_name = db.Column(db.String(128), nullable=False )
    legacyapp = db.relationship(
        "PasswordList", backref="LegacyApp", lazy="select", uselist=False
    )

    

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

# the class Password will inherit the db.Model of SQLAlchemy
class PasswordList(db.Model):
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    password = db.Column(db.String(128))
    user_id = db.Column(db.Integer())
    #created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    app_id = db.Column(db.Integer(), db.ForeignKey('tbl_legacy_application_list.id'))

    #db.create_all()
    
    
    def add_app_pwd(_password,_user_id,_app_id):
        #print(_created_date)
        # creating an instance of our password constructor
        new_pwd = PasswordList(password=_password, user_id=_user_id, app_id=_app_id)
        print("--------")
        db.session.add(new_pwd)  # add new password to database session
        print("--------")
        db.session.commit()  # commit changes to session
        print("--------")
        return new_pwd

    def get_all_password(_user_id):
        #function to get all pwd in our database to related particular user
        result = [PasswordList.json(password) for password in PasswordList.query.filter(PasswordList.user_id==_user_id).all()]
        #print (result)
        return result

  
    def json(self):
        return {
            #'id': self.id,
            'password': "*************",
            'app_name': self.app_id,
            #'created_date': self.created_date
            #'user_id': self.user_id
        }

#the class UserList will inherit the db.Model of SQLAlchemy
class UserList(db.Model):
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(20))
    passwordCriteraStatus = db.Column(db.Integer())
    
    

    
    def add_new_user(_username,_password,_email,_role,_passwordCriteraStatus):
        # creating an instance of our password constructor
        new_user = UserList(role=_role,username=_username,password=_password,email=_email,passwordCriteraStatus=_passwordCriteraStatus)
        db.session.add(new_user)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_user
    
    def get_all_users():
        user_list= [UserList.json(userApp) for userApp in UserList.query.all()]
        return user_list
    
    def get_user_by_id(_id):
        userIsExist = UserList.query.filter_by(id=_id, role="ADMIN").first()
        if userIsExist is None:
            return False
        else:
            return True

    def check_login(_email):
        user = UserList.query.filter_by(email=_email).first()
        if user is None:
            return False
        else:
            return user

    def update_user_satus():
        update = db.session.query(UserList).filter(UserList.passwordCriteraStatus == 1).update({UserList.passwordCriteraStatus:0}, synchronize_session = False)
        db.session.commit()  # commit changes to session
        return True
        
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': "Hide",
            'email': self.email,
            'role': self.role
        }



# the class User app will inherit the db.Model of SQLAlchemy
