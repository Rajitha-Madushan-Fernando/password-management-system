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
- #####  Activate Python environment `pipenv shell` 
- #####  Install required packages  `pip install -r requirements.txt` 

### Now you ready to run the application

------------
This  password management system contain two environment variables. Test and Development.To check main functionalities, We need to run the system under **development** environment and if we want to test the system we need to run the system under **test** environment.

#### Run the system under Test environment | Run the unit test cases
##### Windows 
	$env:FLASK_ENV = test
	python -m unittest
##### Linux
	export FLASK_ENV=test
	python -m unittest

#### Run the system under Development environment
##### Windows 
	$env:FLASK_ENV = development
	python -m unittest
##### Linux
	export FLASK_ENV=development
	python -m unittest

##### Note : Depends on your requirement you need to change the environment. Otherwise system will generate errors. Ex: If you want to use the system and check the functionalities, Then you cannot use Test environment. You need to change it to **Development environment**.
------------
### PMS Functionalities
This system functions mainly devided to two categories. **ADMIN** and **USER**.  Some task can be perform by Admin only. In the first section list down all  function which required Admin access.





