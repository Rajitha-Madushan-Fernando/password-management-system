from database_config import *
from json import load
import pyhibp
from pyhibp import pwnedpasswords as pw
import bcrypt
import os
import string
from cryptography.fernet import Fernet
basedir = os.path.abspath(os.path.dirname(__file__))
#This key is use to decrypt the password
genrated_key = os.environ[current_env+'_encryptkey'].encode('utf-8')
complexity_file = os.environ[current_env+'_COMPLEX']

class Password:
    @staticmethod
    def check_hibp(password):
        # Required: A descriptive user agent must be set describing the application consuming
        #   the HIBP API
        pyhibp.set_user_agent(ua="PMS-User")

        # Check a password to see if it has been disclosed in a public breach corpus
        resp = pw.is_password_breached(password=password)
        if resp:
            #print("Password breached!")
            #print("This password was used {0} time(s) before.".format(resp))
            return True
        # Get data classes in the HIBP system
        resp = pyhibp.get_data_classes()

        # Get all breach information
        resp = pyhibp.get_all_breaches()

        # Get a single breach
        resp = pyhibp.get_single_breach(breach_name="Adobe")

        # An API key is required for calls which search by email address
        #   (so get_pastes/get_account_breaches)
        # See <https://haveibeenpwned.com/API/Key>
        HIBP_API_KEY = None

        if HIBP_API_KEY:
            # Set the API key prior to using the functions which require it.
            pyhibp.set_api_key(key=HIBP_API_KEY)

            # Get pastes affecting a given email address
            resp = pyhibp.get_pastes(email_address="test@example.com")

            # Get breaches that affect a given account
            resp = pyhibp.get_account_breaches(account="test@example.com", truncate_response=True)
    
    @staticmethod
    def check_complexity(password):
        with open(basedir +'/'+complexity_file, 'r') as file:
            criteria = load(file)
            spCharater = criteria['existSpecialCharacter']
            upperCase = criteria['existUpperCase']
            lowerCase = criteria['existLowerCase']
            number = criteria['existNumber']
            spCharaterList = criteria['specialCharaterList']
            maxLen = criteria['maxLength']
            minLen = criteria['minLength']
            charaterType = criteria['charaterType']
            
            #print (spCharater)
            
            if len(password) < minLen:
                return False, "Make sure your password is at least " + str(minLen) + " letters"

            if len(password) > maxLen:
                return False, "Make sure your password is at max " + str(maxLen) + " letters"
            
            if number is True: 
                if any(str.isdigit(password) for password in password) != number:
                    return False, "Make sure your password contain one number"
                else:
                    pass
                    
            if upperCase is True: 
                if any(password.isupper() for password in password) != upperCase:
                    return False, "Make sure your password contain one uppercase letter"
                else:
                    pass

            if lowerCase is True:
                if  any(password.islower() for password in password) != lowerCase:
                        return False, "Make sure your password contain one lowercase letter"
                else:
                    pass
                
            if spCharater  is True:
                if any(cha in spCharaterList for cha in password) != True:
                    return False, "Make sure your password contain one special charater"
                else:
                    pass
            
            if any(cha not in charaterType for cha in password):
                return False, "Make sure to enter allowed charaters"
                
            else:
                return True, "Password suceess"

    @staticmethod
    def hash_pwd(password):
        updated_password = password.encode("utf-8")
        password_hash = bcrypt.hashpw(updated_password, bcrypt.gensalt())
        #print (password_hash)
        return password_hash

    @staticmethod
    def verify_password(hash_password,password):
        #print (password)
        #print (hash_password)
        hash_pwd=hash_password.encode("utf-8")
        passsword_status =  bcrypt.checkpw(hash_pwd, password)
        return passsword_status

    @staticmethod
    def encrypt_password(password):
        BLOCK_SIZE = 32 
        key = genrated_key
        plain_text = password
        data = plain_text.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        ciphered_text = cipher.encrypt(pad(data,BLOCK_SIZE))
        return ciphered_text


    def decrypt_pwd(cipher_text):
        cipher = AES.new(genrated_key, AES.MODE_ECB)
        deciphered_bytes = cipher.decrypt(cipher_text)
        decrypted_data = deciphered_bytes.decode('utf-8')
        return ''.join(x for x in decrypted_data if x in string.printable)
    """
    def sample_encrypt(password):
        print(genrated_key)
        cipher_suite = Fernet(genrated_key)
        print(genrated_key)
        answer = bytes(password, encoding='utf-8')
        cipher_text = cipher_suite.encrypt(answer)
        plain_text = cipher_suite.decrypt(cipher_text)
        print(cipher_text)
        print(plain_text)
    """