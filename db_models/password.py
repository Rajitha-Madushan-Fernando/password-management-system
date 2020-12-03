from database_config import *
import json
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

# Initializing our database
db = SQLAlchemy(app)

# the class Password will inherit the db.Model of SQLAlchemy
class PasswordList(db.Model):
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(128))
    app_id = db.Column(db.String(11))
    user_id = db.Column(db.String(11))
    
    
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
        