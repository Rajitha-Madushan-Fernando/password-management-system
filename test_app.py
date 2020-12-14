import unittest
from json import dumps, loads, load
import requests
import json
from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app  = app.test_client()
        self.app.testing = True
        self.app.token = ""

    #Test user registration module
    def test_resgister(self):
        response = self.app.post('/signin', 
            data = dumps({
                'username':'test',
                'password': '34D*&%Wgsju!',
                'email': 'test@yahoo.com',
                'role': 'USER',
                'pwdcriteastatus':1 #This is either 1 or 0 
            }), content_type='application/json'
        )
        self.assertEqual(response.status_code, 201), "This response should success(201)"
    
    #Test Login module using  test@yahoo.com and  password = "34D*&%Wgsju!" 
    def test_login_by_correct_data(self):
        response = self.app.post('/login', 
            data = dumps({
                "email":"test@yahoo.com",
                "password": "34D*&%Wgsju!",
            }), content_type='application/json'
        )
        #print (response.data)
        reponse_data = loads((response.data))
        self.assertEqual(reponse_data["email"], "test@yahoo.com")
        self.assertEqual(reponse_data["user-id"], 4)
        self.assertEqual(response.status_code, 200)
       
    #Test Login module using  sample@yahoo.com and  password = "342123&%Wgsju!" 
    def test_login_by_incorrect_data(self):
        response = self.app.post('/login', 
            data = dumps({
                "email":"sample@yahoo.com",
                "password": "342123&%Wgsju!",
            }), content_type='application/json'
        )
        #print (response.data)
        reponse_data = loads((response.data))
        self.assertEqual(response.status_code, 401)
    
    def test_get_pwd_list_without_valid_token(self):
        response = self.app.get('/pwd_list',
             data = dumps({}), content_type='application/json'
        )
        #print(response.data)
        reponse_data = loads((response.data))
        self.assertEqual(reponse_data["Error Meesage"], "A Valid token is missing!")
        self.assertEqual(response.status_code, 401)
    

    def test_get_pwd_list_with_valid_token(self):
        resp_login = self.app.post('/login', data = dumps({"email":"test@yahoo.com","password": "34D*&%Wgsju!"}), content_type='application/json')
        token = loads((resp_login.data))   
        response = self.app.get('/pwd_list', headers={ 'x-access-tokens': token["token"]})
        self.assertEqual(response.status_code, 200)


    


    def tearDown(self):
        pass   


   
if __name__ == '__main__':
    unittest.main()