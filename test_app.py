#Unit test case APP Module
#This test case include following sub test cases
    #Register as a new ADMIN user
    #Login to system using as a ADMIN user
    #Check JWT Token validitiy
    #Update Password complexity(This function require ADMIN access)
    #Force renew password when system admin change the password complexity
#Last Test date : 2020-12-18
#Developer : Rajitha Fernando
import unittest
from json import dumps, loads, load
import os
import requests
import json
from app import app, db
from db_models.pms_models import UserList
from password_module.password import Password

class AppTest(unittest.TestCase):

    def setUp(self):
        self.app  = app.test_client()
        self.app.testing = True
        email = 'test@yahoo.com'
        password = Password.hash_pwd('34D*&%Wgsju!')
        role = 'ADMIN'
        username = 'test'
        pwdcriteastatus = 1
        self.user = UserList.add_new_user(username,password,email,role,pwdcriteastatus)
    
    #Test login function  with correct useremail and password and this generate a token
    def test_login(self):
        response = self.app.post('/login', 
            data = dumps({
                "email":"test@yahoo.com",
                "password": os.getenv("test_admin_pwd"),
            }), content_type='application/json'
        )
        reponse_data = loads(response.data)
        self.token = reponse_data['Token']
        self.assertEqual(response.status_code, 200)

    #Test Complexity update as a ADMIN user without having a proper Token(JWT)
    #This test case generate 401 Error code.(Unauthorized)
    def test_update_complexity_without_JWT_token(self):
        resp_login = self.app.post('/login', 
            data = dumps({
                "email":"test@yahoo.com",
                "password": os.getenv("test_admin_pwd"),
            }),content_type='application/json'
        )
        reponse_data = loads(resp_login.data)
        self.token = reponse_data['Token']

        response = self.app.post('/update_pwd_criteria',
            data = dumps({
                "charaterType": "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?/.<>,{}[]:;|\\`'_-+= ",
                "existLowerCase": True,
                "existNumber": True,
                "existSpecialCharacter": True,
                "existUpperCase": True,
                "maxLength": 16,
                "minLength": 8,
                "specialCharaterList": "!@#$%^&*()?/.<>,{}[]:;|\\`'_-+="
            }),content_type='application/json'
            
        )
        self.assertEqual(response.status_code, 401)    
    
    #Test Complexity update as a ADMIN user with having a proper Token(JWT)
    #This test case generate 401 Error code.(Unauthorized)
    def test_update_complexity(self):
        resp_login = self.app.post('/login', 
            data = dumps({
                "email":"test@yahoo.com",
                "password": os.getenv("test_admin_pwd"),
            }),content_type='application/json'
        )
        reponse_data = loads(resp_login.data)
        self.token = reponse_data['Token']

        response = self.app.post('/update_pwd_criteria',
            data = dumps({
                "charaterType": "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?/.<>,{}[]:;|\\`'_-+= ",
                "existLowerCase": True,
                "existNumber": True,
                "existSpecialCharacter": True,
                "existUpperCase": True,
                "maxLength": 16,
                "minLength": 8,
                "specialCharaterList": "!@#$%^&*()?/.<>,{}[]:;|\\`'_-+="
            }),content_type='application/json',headers={'x-access-tokens': self.token}
            
        )
        self.assertEqual(response.status_code, 200)
    
    #Test case for Force renew password when system admin change the password complexity
    #Once system admin change the password policy, All users will be get an NOTIFICATION when loggin to system
    #At this moment I developed only notification level. Not update module
    #Once user loging to system he or she will see "System adminstartor recently change the password policy. Please update the password!"
    def test_force_renew_password(self):
        response = self.app.post('/login', 
            data = dumps({
                "email":"test@yahoo.com",
                "password": os.getenv("test_admin_pwd"),
            }), content_type='application/json'
        )
        reponse_data = loads(response.data)
        self.assertTrue(reponse_data["Message"], "System adminstartor recently change the password policy. Please update the password!")

    def tearDown(self): 
        db.session.query(UserList).delete()


   
if __name__ == '__main__':
    unittest.main()