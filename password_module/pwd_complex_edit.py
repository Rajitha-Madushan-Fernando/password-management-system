from database_config import *
from flask import Flask, request, jsonify
from json import load, dumps, dump
import os
basedir = os.path.abspath(os.path.dirname(__file__))
complexity_file = os.environ[current_env+'_COMPLEX']

class PasswordComplexityEdit:


    @staticmethod
    def getComplexity():
        with open(basedir +'/'+complexity_file, 'r') as file:
            criteria = load(file)
            return criteria


    def updateComplexity(data):
        with open(basedir +'/'+complexity_file, 'w') as file:
            json_object = data
            dump(json_object, file)
            file.close()  
            return True