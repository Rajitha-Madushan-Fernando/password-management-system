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
    
    

    def tearDown(self):
        pass   


   
if __name__ == '__main__':
    unittest.main()