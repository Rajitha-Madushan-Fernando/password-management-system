# Password-management-system
A PMS(Password Management System) is an API that helps individuals securely store and manage all of their login credentials. This api is used to create strong, unique, complex passwords for web applications. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Want to use this project
##### Basics
1. Fork/Clone
2. Activate a virtualenv
3. Install all dependencies from a pipfile
`$ pipenv install --dev`

##### Select the environment to run the application
This password management system  contain **Test** and **Development** environments

##### To run this API under Development environment

    $ export FLASK_ENV=development 

    $ python app.py 

##### To run this API under Testing environment / To run all unit test cases and remove all Deprecation Warning 

    $ export FLASK_ENV=test

    $ pytest . -W ignore::DeprecationWarning

### System main functions

#### Signup / Register to system as a new user
`Method = POST`     `http://127.0.0.1:5000/signin`


    {
    	"username":"Jack",
    	"password":"123DEs!678",
    	"email":"jack@gmail.com",
    	"role":"ADMIN"
    }
