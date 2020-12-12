import unittest
from json import dumps
from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app  = app.test_client()
        self.app.testing = True

    