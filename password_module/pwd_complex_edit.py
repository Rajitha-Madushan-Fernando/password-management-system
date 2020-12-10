from flask import Flask, request, jsonify
from json import load, dumps, dump
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class PasswordComplexityEdit:


    @staticmethod
    def getComplexity():
        with open(basedir + '/password_complexity.json', 'r') as file:
            criteria = load(file)
            return criteria


    def updateComplexity(data):
        with open(basedir + '/password_complexity.json', 'w') as file:
            json_object = data
            #a_file = open(basedir + "/password_complexity.json", "w")
            dump(json_object, file)
            file.close()  
            return True