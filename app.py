from flask import Flask, request, Response, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import jsonpickle
import json
import os
import jwt
import datetime
import uuid
from functools import wraps
from flask import session as login_session
#Exception lib 
from werkzeug import exceptions


#Import user defined libs
from password_module.password import Password
from db_models.pms_models import PasswordList
from db_models.pms_models import LegacyApp
from db_models.pms_models import UserList


#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


#Init ma
ma = Marshmallow(app)

#Access controll module
#Without having a proper JWWT authentication token cannot access to API
app.config['SECRET_KEY'] = 'rajithasecret'
def token_required(f):
    @wraps(f)  
    def decorator(*args, **kwargs):
        token = None 
        #print (request.headers)
        if 'x-access-tokens' in request.headers:  
            token = request.headers['x-access-tokens'] 
        if not token:  
             return jsonify({
                'Error Meesage': "A Valid token is missing!"
            }), 401      
        try:   
            
            data = jwt.decode(token, app.config['SECRET_KEY']) 
            return f( *args,  **kwargs) 
        except:  
            return jsonify({
                'Error Meesage': "Token is invalid"
            }), 401   
            
             
    return decorator
#Access controll module end

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
@token_required
def get_users():
    '''Function to get all the password in the database'''
    result = UserList.get_all_users()
    #print (result)
    result =  make_response(jsonify({"status": result}))
    return result
##User registration module end


##User login module Start
@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data['email']
    entered_password = request_data['password']
    #Do password verification
    
    user = UserList.check_login(email)
    #return jsonpickle.encode(user)
    
    #print(current_pwd)
    if user:
        current_pwd = user.password
        if  Password.verify_password(current_pwd,entered_password):
            login_session['id'] = user.id
            #print(login_session['id'])
            expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'])
            return jsonify({
                'token': token.decode('utf-8'),
                'user-id':user.id,
                'email': user.email
            }), 200
    else:
        error_message="Your username or password is invalid"
        return jsonify({
                'Error Meesage': error_message
        }), 401     
##User login module end



#Password module start
@app.route('/add_pwd', methods=['POST'])
@token_required
def check_pwd():
    try:
        req_data = request.get_json()
        user_password = req_data['password']
        user_id = login_session['id']
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
@token_required
def get_pwd():
    '''Function to get all the password in the database'''
    #print(login_session['id'])
    result = PasswordList.get_all_password(login_session['id'])
    response =  make_response(jsonify({"status": result}))
    return response
#Password module end


##Legacy Application module
@app.route('/add_new_app', methods=['POST'])
@token_required
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
@token_required
def get_legacy_app():
    '''Function to get all the app list in the database'''
    result = LegacyApp.get_all_legacy_app()
    response =  make_response(jsonify({"status": result}))
    return response
##Legacy Application module finished


#Run server
if __name__ == '__main__':
    app.run(debug=True)  # The user should type the machine ID here
