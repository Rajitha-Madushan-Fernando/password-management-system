# Password-management-system
A PMS(Password Management System) is an API that helps individuals securely store and manage all of their login credentials. This api is used to create strong, unique, complex passwords for web applications. 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Setup the environment

------------


-  ##### Check python version `$ python --version`
- ##### Check pip version `$ pip --version`
- ##### Clone the project `$ git clone https://github.com/Rajitha-Madushan-Fernando/password-management-system.git`
-  ##### Install python virtual environment `pip install pipenv`
- #####  Install required packages  `pip install -r requirements.txt` 
- #####  Activate Python environment `pipenv shell` 


### Now you ready to run the application

------------
This  password management system contain two environment variables. Test and Development.To check main functionalities, We need to run the system under **development** environment and if we want to test the system we need to run the system under **test** environment.

#### Run the system under Test environment | Run the unit test cases
##### Windows 
	$env:FLASK_ENV = 'test'
	python -m unittest
##### Linux
	export FLASK_ENV=test
	python -m unittest

#### Run the system under Development environment
##### Windows 
	$env:FLASK_ENV = 'development'
	python app.py
##### Linux
	export FLASK_ENV=development
	python app.py

##### Note : Depends on your requirement you need to change the environment. Otherwise system will generate errors. Ex: If you want to use the system and check the functionalities, Then you cannot use Test environment. You need to change it to **Development environment**.
------------
### PMS Functionalities
This system functions mainly devided to two categories. **ADMIN** and **USER**.  Some task can be perform by Admin only. In the first section list down all  function which required Admin access.

##### Note : After having the  successfully login,The system generate a Json web token. For all other tasks we need to give this token as a authentication mechanisam. To do that you have to pass the token in the postman header field. 
`x-access-tokens :  "your token goes here"`

### Admin  Tasks
##### Login to system using master password - Admin[POST]
`http://127.0.0.1:5000/login`
<br/>
`{
	"email": "admin@admin.com",
	"password": "123DEs!678"
}`

##### Add new legacy application to system - Admin[Token Required][POST]
`http://127.0.0.1:5000/add_new_legacy_app`
<br/>
 `{
    "app_name":"HRM",
    "url":"www.sample.com",
    "description":"Sample data"
}`
##### View all registered User list - Admin[Token Required][GET]
`http://127.0.0.1:5000/all_users`

##### Update Password complexity - Admin[Token Required][POST]
`http://127.0.0.1:5000/update_pwd_criteria`
<br/>
`{
    "charaterType": "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?/.<>,{}[]:;|\\`'`_-+= ",  
    "existLowerCase": true,  
    "existNumber": true,  
    "existSpecialCharacter": true,  
    "existUpperCase": true,  
    "lastUpdatedDate": "2020-12-09",  
    "maxLength": 16,  
    "minLength": 8,  
    "specialCharaterList": "!@#$%^&*()?/.<>,{}[]:;|\\`'`_-+="  
}`
 

------------

### Normal User Tasks
##### View the password complexity[Token Not Required][GET] 
 `http://127.0.0.1:5000/get_pwd_criteria`

##### Signup/Create new User profile[POST]
 `http://127.0.0.1:5000/signup`
 <br/>
 `{
	"username":"sam",
	"password":"Ab@#123sJK7",
	"email":"sam@gmail.com"
}`
##### Login to system using master password[POST]
`http://127.0.0.1:5000/login`
<br/>
`{
	"email": "sam@gmail.com",
	"password": "Ab@#123sJK7"
}`
##### View System Legacy application list[Token Required][GET]
 `http://127.0.0.1:5000/app_list`

##### Create new Password [Token Required][POST] - Main task of the PMS
`http://127.0.0.1:5000/add_pwd`
<br/>
 `{
	"password":"1@##D$D5fAcbA!",
	"app_id":1
}`
##### Update the exsiting password [Token Required][PUT]
`http://127.0.0.1:5000/update_pwd`
<br/>
 `{
	"id":1,
	"password":"1@##D$D5f!cbA!"
}`


##### Get all passwords list for current logged user [Token Required][GET]
`http://127.0.0.1:5000/pwd_list`
