from dotenv import load_dotenv
from flask import Flask, request, Response, jsonify, make_response,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, ValidationError
from flask_json_schema import JsonSchema
import os
import json
import jwt
import datetime
import uuid
from functools import wraps
from flask import session as login_session

# Exception lib
from werkzeug import exceptions

#Cryto libs
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Cipher import AES


#Load envirement variables
load_dotenv()
current_env = os.environ['FLASK_ENV']


#print(current_env)


#init app
app = Flask(__name__)
schema = JsonSchema(app)
basedir = os.path.abspath(os.path.dirname(__file__))


#Database
#app.config['PROPAGATE_EXCEPTIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, os.environ[current_env+'_DB'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initializing our database
db = SQLAlchemy(app)