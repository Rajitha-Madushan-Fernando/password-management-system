#Password management system database model.
#This file contain all database classes {User, Password, Legacy App}
#Import all required libraries
from database_config import *
from datetime import datetime


# Import user defined libs
#This Password module is use to decrypt the password and send to frontend
from password_module.password import Password

#Create Legacy application model, database table and fields
class LegacyApp(db.Model):
    #Create a table
    __tablename__ = 'tbl_legacy_application_list'
    id = db.Column(db.Integer, nullable=False, primary_key=True, unique=True)
    url = db.Column(db.String(128), nullable=False )
    description = db.Column(db.String(128), nullable=False )
    app_name = db.Column(db.String(128), nullable=False )
    pwd = db.relationship('PasswordList', back_populates="parent" , lazy='joined')

    
    #Add new legacy application to PMS    
    def add_new_legacy_app(_app_name,_url,_description):
        new_legacy_app = LegacyApp(app_name=_app_name,description=_description,url=_url)
        db.session.add(new_legacy_app)  # create a new record
        db.session.commit()  # commit changes to session
        return new_legacy_app

    #Get all legacy applications
    def get_all_legacy_app():
        return [LegacyApp.json(legacyApp) for legacyApp in LegacyApp.query.all()]

    #Before add new legacy application to system, check the entered application is already in the database or not
    def check_app_id(app_id):
        exists = LegacyApp.query.filter_by(id=app_id).scalar()
        if exists is None:
            return False
        else:
            return True
        
    #Convert to json object and render to front end | In this case
    def json(self):
        return {
            'id': self.id,
            'app_name': self.app_name
        }

#Create Password  model, database table and fields
class PasswordList(db.Model):
    #Create a table
    __tablename__ = 'tbl_app_password_list'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    password = db.Column(db.String(128))
    user_id = db.Column(db.Integer())
    #created_date = db.Column(db.DateTime(), default=datetime.utcnow)
    app_id = db.Column(db.Integer(), db.ForeignKey('tbl_legacy_application_list.id'))
    parent = db.relationship("LegacyApp", back_populates="pwd")

    #Add New Password for Legacy application
    def add_app_pwd(_password,_user_id,_app_id):
        new_pwd = PasswordList(password=_password, user_id=_user_id, app_id=_app_id)
        db.session.add(new_pwd)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_pwd

    #Get all password list for current logged user. 
    #Pass current logged user id as a parameter
    def get_all_password(_user_id):
        result = [PasswordList.json(record) for record in PasswordList.query.filter(PasswordList.user_id==_user_id).all()]
        return result

    
    #Convert to json object and render to front end | In this case
    def json(self):
        return {
            'id': self.id,
            'password':Password.decrypt_pwd(self.password),
            'app_name': self.parent.app_name,
            'url': self.parent.url,
            'description': self.parent.description
            #'created_date': self.created_date
            #'user_id': self.user_id
        }

#Create User  model, databaUserListse table and fields
class UserList(db.Model):
    #Create a table
    __tablename__ = 'tbl_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(128))
    email = db.Column(db.String(128))
    role = db.Column(db.String(20))
    passwordCriteraStatus = db.Column(db.Integer())
    
    #Create dummy admin User
    def add_new_admin_user(_username,_password,_email,_role,_passwordCriteraStatus):
        new_user = UserList(role=_role,username=_username,password=_password,email=_email,passwordCriteraStatus=_passwordCriteraStatus)
        db.session.add(new_user)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_user

    #Create new user and save in database
    def add_new_user(_username,_password,_email,_role,_passwordCriteraStatus):
        new_user = UserList(role=_role,username=_username,password=_password,email=_email,passwordCriteraStatus=_passwordCriteraStatus)
        db.session.add(new_user)  # add new password to database session
        db.session.commit()  # commit changes to session
        return new_user
    
    #Get all registered users list
    def get_all_users():
        user_list= [UserList.json(userApp) for userApp in UserList.query.all()]
        return user_list
    
    #Filter user by ADMIN role
    def get_user_by_id(_id):
        userIsExist = UserList.query.filter_by(id=_id, role="ADMIN").first()
        if userIsExist is None:
            return False
        else:
            return True

    #Check the email address in the database when your trying to login to system
    def check_login(_email):
        user = UserList.query.filter_by(email=_email).first()
        if user is None:
            return False
        else:
            return user

    #When system admin change the password complexity update user pasword criteria status= 0
    def update_user_satus():
        update = db.session.query(UserList).filter(UserList.passwordCriteraStatus == 1).update({UserList.passwordCriteraStatus:0}, synchronize_session = False)
        db.session.commit()  # commit changes to session
        return True

    #Convert to json object and render to front end | In this case   
    def json(self):
        return {
            'id': self.id,
            'username': self.username,
            #'password': "************",
            'email': self.email,
            'role': self.role
        }


class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.String(required=True)

class PasswordSchema(Schema):
    app_id = fields.Integer(required=True)
    password = fields.String(required=True)


class LegacyAppSchema(Schema):
    url = fields.String(required=True)
    description = fields.String(required=True)
    app_name = fields.String(required=True)

db.create_all()
