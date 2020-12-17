import unittest
from .password import Password as Password
class PasswordTest(unittest.TestCase):

    def setUp(self):
        self.password1 = 'password'
        self.password2 = '12345678'
        self.password3 = 'ABC123456'
        self.password4 = '!@#$AD'
        self.password5 = '34D*&%Wgsju!'
        self.password6 = '34D*&%Wgsju!34D*&%Wgsju!34D*&%Wgsju!'

    def test_complexity(self):
        #Using password complexity json file and check whether password meets the requirement.
        self.assertEqual(Password.check_complexity(self.password1), (False, 'Make sure your password contain one number'),'Failed Password Test : Make sure your password contain one number')
        self.assertEqual(Password.check_complexity(self.password2), (False, 'Make sure your password contain one uppercase letter'),  'Failed Password Test : Make sure your password contain one uppercase letter')
        self.assertEqual(Password.check_complexity(self.password3), (False, 'Make sure your password contain one lowercase letter'),  'Failed Password Test : Make sure your password contain one lowercase letter')
        self.assertEqual(Password.check_complexity(self.password4), (False, 'Make sure your password is at least 8 letters'),  'Failed Password Test : Make sure your password is at least 8 letters')
        self.assertEqual(Password.check_complexity(self.password5), (True, 'Password suceess'), 'Password suceess')
        self.assertEqual(Password.check_complexity(self.password6), (False, 'Make sure your password is at max 16 letters'),  'Failed Password Test : Make sure your password is at max 16 letters')
    
    def test_hibp(self):
        #Using the PyHIBP  API check the inserted password is leaked password or not
        #Last test data : 14/12/2020
        #This is externel API process. Processing time is depend by the internet connection, computer processing power, etc
        #If the password is in this leaked list system return True
        self.assertTrue(Password.check_hibp(self.password1))
        self.assertTrue(Password.check_hibp(self.password2))
        self.assertTrue(Password.check_hibp(self.password3))
        self.assertFalse(Password.check_hibp(self.password5))

        
    def test_password_validity(self):
        #Using python Bcrypt (verify_password)  function check user entered password and hashed password status
        self.assertTrue(Password.verify_password(self.password1, Password.hash_pwd(self.password1)))#Both use same passwords  
        self.assertTrue(Password.verify_password(self.password2, Password.hash_pwd(self.password2)))#Both user same passwords  
        self.assertFalse(Password.verify_password(self.password1, Password.hash_pwd(self.password4)))#Use Different passwords  
        self.assertFalse(Password.verify_password(self.password3, Password.hash_pwd(self.password5)))#Use Different passwords  

    

    def tearDown(self):
        pass   


   
if __name__ == '__main__':
    unittest.main()