###################################
#
# Functions for user authentication
# in our SmartSpend application.
#
# Authors:
#   - Nicholas Qiu
#   - Stephi Lyou
#   - Serena Lyou

import requests
from cryptography.fernet import Fernet

def signup(baseurl):
    
    print("-------Sign Up-------")
    print("Enter your username:")
    username = input("> ")
    print("Enter your password:")
    password = input("> ")
    print("Enter first name:")
    first_name = input("> ")
    print("Enter last name:")
    last_name = input("> ")
    
    key = Fernet.generate_key()
    
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    
    data = {
        "username": username,
        "password": encrypted_password,
        "first_name": first_name,
        "last_name": last_name,
        "key": key.decode()
    }
    
    #send to lambda_function to write to sql
    api = '/sign-up'
    url = baseurl + api
    
    res = requests.post(url, json=data)
    print(res)
    print(res.text)
    
    if res.status_code == 200:
        print("Sign up successful!")
        print(res.json())
        return [username, first_name, last_name]
        
def login(baseurl):
    
    logged_in = False
    
    print("-------Log In-------")
    
    api = '/log-in'
    url = baseurl + api
    
    while not logged_in:
        print("Enter your username:")
        username = input("> ")
        print("Enter your password:")
        password = input("> ")
        
        data = {
            "username": username, 
            "password": password
        }
        
        print(url)
        res = requests.post(url, json=data)
        
        print(res.text)
        
        print(res.status_code)
        if res.status_code == 200:
            print("Log-in successful!")
            body = res.json()
            print(body)
            logged_in = True
            
            return [username, body["first_name"], body["last_name"]]
        elif res.status_code == 400:
            print("Invalid username or password.")