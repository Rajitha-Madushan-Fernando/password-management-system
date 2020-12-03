from flask import Flask, request, Response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import jsonpickle
#Exception lib 
from werkzeug import exceptions
import os
from datetime import date

#Import user defined libs
from password_module.password import Password
from db_models.password import PasswordList

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


#Init ma
ma = Marshmallow(app)


#Password module
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
    print("0000000")
    response = PasswordList.get_all_password()
    result = jsonpickle.encode(response)
    return result

#Run server
if __name__ == '__main__':
    app.run(debug=True)  # The user should type the machine ID here
