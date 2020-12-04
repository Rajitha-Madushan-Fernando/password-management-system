from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import jsonpickle
#Exception lib 
from werkzeug import exceptions
import json
import os
import jwt
import datetime
from functools import wraps

#Import user defined libs
from password_module.password import Password
from db_models.password import PasswordList
from db_models.password import LegacyApp
from db_models.password import UserList

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


#Init ma
ma = Marshmallow(app)

#Access controll module
#Without having a proper JWWT authentication token cannot access to API
app.config['SECRET_KEY'] = 'rajithasecretkey'
def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')
        try:
            jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args, **kwargs)
        except:
            return jsonify({'error': 'Need a valid token to view this page'}), 401
    return wrapper
#Access controll module finished


##User registration module
@app.route('/signin', methods=['POST'])
def register():

    try:
        request_data = request.get_json()
        username = str(request_data['username'])
        password = str(request_data['password'])
        email = request_data['email']
        role = request_data['role']
        
        hibp_result = Password.check_hibp(password)
        is_complexity, complexity_result_msg  = Password.check_complexity(password)
        hash_result = Password.hash_pwd(password)

        if is_complexity is False:
            return jsonify(Process='ERROR!', Process_Message=complexity_result_msg)
    
        elif hibp_result is True:
            return jsonify(Process='ERROR!', Process_Message='This password is already in HIBP Database.')
        
        else:
            #return jsonify(Process='SUCESS!', Process_Message='Good Password!')
            #return jsonify(hash_result)
            response = UserList.add_new_user(username,hash_result,email,role)
            return jsonify({"Message": "Succesfuly saved"}), 201


    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')    
    
@app.route('/all_users', methods=['GET'])
def get_users():
    '''Function to get all the password in the database'''
    response = UserList.get_all_users()
    result = jsonpickle.encode(response)
    return result
##User registration module finished



#Password module start
@app.route('/add_pwd', methods=['POST'])
def check_pwd():
    try:
        req_data = request.get_json()
        user_password = req_data['password']
        user_id = req_data['user_id']
        app_id = req_data['app_id']
        #print(user_password)

        #user defined functions
        hibp_result = Password.check_hibp(user_password)
        is_complexity, complexity_result_msg  = Password.check_complexity(user_password)
        hash_result = Password.hash_pwd(user_password)
        
        #print("--------------------------")
        #print (hash_result)

        if is_complexity is False:
            return jsonify(Process='ERROR!', Process_Message=complexity_result_msg)
    
        elif hibp_result is True:
            return jsonify(Process='ERROR!', Process_Message='This password is already in HIBP Database.')

        else:
            #return jsonify(Process='SUCESS!', Process_Message='Good Password!')
            #return jsonify(hash_result)
            response = PasswordList.add_app_pwd(hash_result,user_id,app_id)
            return jsonify({"Message": "Succesfuly saved"}), 201


    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')

@app.route('/pwd_list', methods=['GET'])
def get_pwd():
    '''Function to get all the password in the database'''
    response = PasswordList.get_all_password()
    result = jsonpickle.encode(response)
    return result
#Password module finished




##Legacy Application module
@app.route('/add_new_app', methods=['POST'])
def add_legacy_app():
    try:
        req_data = request.get_json()
        app_name = req_data['app_name']
        #print(user_password)

        response = LegacyApp.add_new_legacy_app(app_name)
        return jsonify({"Message": "Succesfuly saved"}), 201


    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')

@app.route('/app_list', methods=['GET'])
def get_legacy_app():
    '''Function to get all the app list in the database'''
    response = LegacyApp.get_all_legacy_app()
    result = jsonpickle.encode(response)
    return result
##Legacy Application module finished


#Run server
if __name__ == '__main__':
    app.run(debug=True)  # The user should type the machine ID here
