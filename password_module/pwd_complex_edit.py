from flask import Flask, request, jsonify
from json import load, dumps
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class PasswordComplexityEdit:


    @staticmethod
    def getComplexity():
        with open(basedir + '/password_complexity.json', 'r') as file:
            criteria = load(file)
            return criteria


    def updateComplexity(data):
        with open(basedir + '/password_complexity.json', 'r+') as file:
            #System admin can update the password complexity
            #criteria = load(file)

            update_data = dumps(data, indent=2)
            file.write(update_data)  # Writing the new password policies in the file
            return "Successfully updated!"
