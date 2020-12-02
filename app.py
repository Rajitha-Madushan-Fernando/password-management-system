from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
#Exception lib 
from werkzeug import exceptions
import os


#Import user defined libs
from password_module.password import Password

#init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#Init db
db = SQLAlchemy(app)
#Init ma
ma = Marshmallow(app)


#Password module
@app.route('/add_pwd', methods=['POST'])
def check_pwd():
    try:
        req_data = request.get_json()
        user_password = req_data['password']
        print(user_password)

        hibp_result = Password.check_hibp(user_password)
        complexity_result = Password.check_complexity(user_password)
        
        if complexity_result is True:
            return jsonify(Process='ERROR!', Process_Message='This password does not meet security policies.')
    
        elif hibp_result is True:
            return jsonify(Process='ERROR!', Process_Message='This password is already in HIBP Database.')

        else:
            return jsonify(Process='SUCESS!', Process_Message='Good Password!')


    except (KeyError, exceptions.BadRequest):
        return jsonify(Process='ERROR!', Process_Message='Missing information, wrong keys or invalid JSON.')



#Run server
if __name__ == '__main__':
    app.run(debug=True)  # The user should type the machine ID here
