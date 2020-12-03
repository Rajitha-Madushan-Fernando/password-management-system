from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#Exception lib 
from werkzeug import exceptions
import os


#Import user defined libs
from password_module.password import Password
from db_models.password_model import PasswordList

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
        print(user_password)

        #user defined functions
        hibp_result = Password.check_hibp(user_password)
        complexity_result = Password.check_complexity(user_password)
        hash_result = Password.hash_pwd(user_password)
        
        print("--------------------------")
        print (hash_result)

        if complexity_result is True:
            return jsonify(Process='ERROR!', Process_Message='This password does not meet security policies.')
    
        elif hibp_result is True:
            return jsonify(Process='ERROR!', Process_Message='This password is already in HIBP Database.')

        else:
            print("xxxxxxxxxxxxxxxxxxxxxxxxx")
            ##return jsonify(Process='SUCESS!', Process_Message='Good Password!')
            #return jsonify(hash_result)
            PasswordList.add_app_pwd(id, hibp_result)
            response = Response("Your password successfully added", 201, mimetype='application/json')
            return response
            #Save password and other data in the database!


    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')

@app.route('/pwd_list', methods=['GET'])
def get_pwd():
    '''Function to get all the movies in the database'''
    return jsonify({'Passwords': PasswordList.get_all_password()})

#Run server
if __name__ == '__main__':
    app.run(debug=True)  # The user should type the machine ID here
