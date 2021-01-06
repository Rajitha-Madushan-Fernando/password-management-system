#Unit test case Password Module
#This test case include following sub test cases
    #Test Password complexity using different parameters
    #Test the password is Leaked password or Not( Using Thrid Party API - HIBP)
    #Verifies that a password matches a hash using (password_verify) function
    #Test Encrypt and Decrypt functions (Cannot store password as a plain text.PMS successfully encrypt the password) 
#Last Test date : 2020-12-18
#Developer : Rajitha Fernando
import unittest
import os
from .password import Password as Password


class PasswordTest(unittest.TestCase):
    
    def setUp(self):
        self.password1 = os.getenv("password1")
        self.password2 = os.getenv("password2")
        self.password3 = os.getenv("password3")
        self.password4 = os.getenv("password4")
        self.password5 = os.getenv("password5")
        self.password6 = os.getenv("password6")

    def test_complexity(self):
        self.assertEqual(Password.check_complexity(self.password1), (False, 'Make sure your password contain one number'))
        self.assertEqual(Password.check_complexity(self.password1+'1A#ß'), (False, 'Make sure to enter allowed charaters'))
        self.assertEqual(Password.check_complexity(self.password1+'1'), (False, 'Make sure your password contain one uppercase letter'))
        self.assertEqual(Password.check_complexity(self.password1+'1A'), (False, 'Make sure your password contain one special charater'))
        self.assertEqual(Password.check_complexity(self.password1+'1A#'), (True, 'Password suceess'))
        self.assertEqual(Password.check_complexity(self.password2+'A'), (False, 'Make sure your password contain one lowercase letter'))
        self.assertEqual(Password.check_complexity(self.password4), (False, 'Make sure your password is at least 8 letters'))
        self.assertEqual(Password.check_complexity(self.password6), (False, 'Make sure your password is at max 16 letters'))
        

    def test_hibp(self):
        #Using the PyHIBP  API check the inserted password is leaked password or not
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

    
    def test_encrypt_decrypt_pwd(self):
        #Using python cryptodome encrypt and decrypt functions to store password securely.
        cipher_text = Password.encrypt_password(self.password5)
        self.assertTrue(type(cipher_text) == bytes ) 
        decrypt_text = Password.decrypt_pwd(cipher_text)
        #Test same password with encrypt and decrypt functions
        self.assertTrue(decrypt_text == self.password5)
        #Test different password with encrypt and decrypt functions
        self.assertFalse(decrypt_text == self.password4)

    

    def tearDown(self):
        pass   

    
   
if __name__ == '__main__':
    unittest.main()