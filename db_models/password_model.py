from database_config import *
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os

# Initializing our database
db = SQLAlchemy(app)

# the class Password will inherit the db.Model of SQLAlchemy
class PasswordList(db.Model):
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.Text(128))

    def __Init__(self,id,password):
        self.id = id
        self.password = password
        #this method we are defining will convert our output to json

    def add_app_pwd(_id, _password):
        # creating an instance of our password constructor
        new_pwd = PasswordList(id=_id, password=_password)
        db.session.add(new_pwd)  # add new password to database session
        db.session.commit()  # commit changes to session

    def get_all_password():
        '''function to get all pwd in our database'''
        return [PasswordList.json(password) for password in PasswordList.query.all()]