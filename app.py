from database_config import *
from flask import Flask, request, Response, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json
import os
import jwt
import datetime
import uuid
from functools import wraps
from flask import session as login_session
# Exception lib
from werkzeug import exceptions


# Import user defined libs
from password_module.password import Password
from password_module.pwd_complex_edit import PasswordComplexityEdit
from db_models.pms_models import PasswordList
from db_models.pms_models import LegacyApp
from db_models.pms_models import UserList


# Access controll module
# Without having a proper JWWT authentication token cannot access to API
app.config['SECRET_KEY'] = 'rajithasecretkey!@#^&*!)KDJ'


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({
                'Error Meesage': "A Valid token is missing!"
            }), 401
        try:

            data = jwt.decode(token, app.config['SECRET_KEY'])
            return f(*args,  **kwargs)
        except:
            return jsonify({
                'Error Meesage': "Your token is expired! Please login in again"
            }), 401

    return decorator
# Access controll module end

# User registration module


@app.route('/signin', methods=['POST'])
def register():

    try:
        request_data = request.get_json()
        username = str(request_data['username'])
        password = str(request_data['password'])
        email = request_data['email']
        role = request_data['role']
        pwdcriteastatus = 1
        #Check this email address is already exist or not
        user = UserList.check_login(email)
        if user:
            error_message = "This email address is already registered!"
            return jsonify({
                'Error Meesage': error_message
            }), 401
        else:
            hibp_result = Password.check_hibp(password)
            is_complexity, complexity_result_msg = Password.check_complexity(
                password)
            hash_result = Password.hash_pwd(password)

            if is_complexity is False:
                return jsonify(Process='ERROR!', Process_Message=complexity_result_msg)

            elif hibp_result is True:
                return jsonify(Process='ERROR!', Process_Message='This password is already in HIBP Database.')

            else:
                # return jsonify(Process='SUCESS!', Process_Message='Good Password!')
                # return jsonify(hash_result)
                response = UserList.add_new_user(
                    username, hash_result, email, role, pwdcriteastatus)
                return jsonify({"Message": "Succesfuly saved"}), 201


    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')
# User registration module end

# User list retrive module start


@app.route('/all_users', methods=['GET'])
@token_required
def get_users():
    try:
        # Check this user role is ADMIN or USER
        roleStatus = UserList.get_user_by_id(login_session['id'])
        # Function to get all the password in the database
        if roleStatus:
            result = UserList.get_all_users()
            print(result)
            result = make_response(jsonify({"status": result}))
            return result
        else:
            return jsonify({"Message": "Only Admin can see all users"}), 401
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')
# User list retrive module end


# User login module Start
@app.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    email = request_data['email']
    entered_password = request_data['password']
    # Do password verification

    user = UserList.check_login(email)
    try:
        if user:
            current_pwd = user.password
            user_password_status = user.passwordCriteraStatus
            if user_password_status == 0:
                Message = "System adminstartor recently change the password policy. Please update the password!"
            else:
                Message = "Your password meet complexity."

            if Password.verify_password(entered_password, current_pwd):
                login_session['id'] = user.id
                expiration_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
                token = jwt.encode({'exp': expiration_date},app.config['SECRET_KEY'], algorithm='HS256')
                login_session['logged_in'] = True
                return jsonify({
                    'token': token.decode('utf-8'),
                    'user-id': user.id,
                    'email': user.email,
                    'Message': Message

                }), 200
            else:
                error_message = "Your username or password is invalid"
                return jsonify({
                    'Error Meesage': error_message
                }), 401

        else:
            error_message = "Your username or password is invalid"
            return jsonify({
                'Error Meesage': error_message
            }), 401
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Something went wrong! Please login in again')
# User login module end

#User logout module start
#@app.route('/logout',  methods=['POST'])
#@token_required
#def logout():
#    session.pop(login_session['logged_in'], None)
#    return jsonify({
#        'Error Meesage': 'You were logged out.'
#   }), 200
#User logout module end


# Password module start
@app.route('/add_pwd', methods=['POST'])
@token_required
def check_pwd():
    try:
        req_data = request.get_json()
        user_password = req_data['password']
        user_id = login_session['id']
        app_id = req_data['app_id']

        # user defined functions
        hibp_result = Password.check_hibp(user_password)
        is_complexity, complexity_result_msg = Password.check_complexity(user_password)
        encry_result = Password.encrypt_password(user_password)
        #return encry_result
        if is_complexity is False:
            return jsonify(Process='ERROR!', Process_Message=complexity_result_msg)

        elif hibp_result is True:
            return jsonify(Process='ERROR!', Process_Message='This password is already in HIBP Database.')

        else:
            response = PasswordList.add_app_pwd(encry_result, user_id, app_id)
            return jsonify({"Message": "Succesfuly saved"}), 201

    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')

@app.route('/pwd_list', methods=['GET'])
@token_required
def get_pwd():
    #Function to get all the password in the database
    try:
        result = PasswordList.get_all_password(login_session['id'])
        response = make_response(jsonify({"status": result}))
        return response
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')
# Password module end


# Legacy Application module
@app.route('/add_new_legacy_app', methods=['POST'])
@token_required
def add_legacy_app():
    try:
        req_data = request.get_json()
        app_name = req_data['app_name']
        url = req_data['url']
        description = req_data['description']
        roleStatus = UserList.get_user_by_id(login_session['id'])
        if roleStatus:
            result = LegacyApp.add_new_legacy_app(app_name, url, description)
            return jsonify({"Message": "Succesfuly saved"}), 201
        else:
            return jsonify({"Message": "Only Admin can create new applications"}), 401

    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again')


@app.route('/app_list', methods=['GET'])
@token_required
def get_legacy_app():
    # Function to get all the app list in the database
    try:
        result = LegacyApp.get_all_legacy_app()
        response = make_response(jsonify({"status": result}))
        return response
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')
# Legacy Application module finished


# Password complexity renew process
@app.route('/get_pwd_criteria', methods=['POST', 'GET'])
def get_complexity():
    try:
        response = PasswordComplexityEdit.getComplexity()
        return response
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')


@app.route('/update_pwd_criteria', methods=['POST'])
@token_required
def update_complexity():
    request_data = request.get_json()
    charaterType = request_data['charaterType']
    existLowerCase = request_data['existLowerCase']
    existNumber = request_data['existNumber']
    existSpecialCharacter = request_data['existSpecialCharacter']
    existUpperCase = request_data['existUpperCase']
    maxLength = request_data['maxLength']
    minLength = request_data['minLength']
    specialCharaterList = request_data['specialCharaterList']
    try:
        data = {
            "charaterType": charaterType,
            "existLowerCase": existLowerCase,
            "existNumber": existNumber,
            "existSpecialCharacter": existSpecialCharacter,
            "existUpperCase": existUpperCase,
            "maxLength": maxLength,
            "minLength": minLength,
            "specialCharaterList": specialCharaterList
        }
        result = PasswordComplexityEdit.updateComplexity(data)
        roleStatus = UserList.get_user_by_id(login_session['id'])
        if roleStatus:
            if result is True:
                response = UserList.update_user_satus()
                # return response
                if response is True:
                    return jsonify({"Message": "Password complexity succesfully updated!"}), 200

            else:
                return jsonify({"Message": "Missing information, wrong keys or invalid JSON."}), 401
        else:
            return jsonify({"Message": "Only Admin can update password complexity"}), 401
    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Your token is expired! Please login in again.')

# Run server
if __name__ == '__main__':
    app.run(debug=True)  # The user should type the machine ID here
