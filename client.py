###################################
#
# Client for SmartSpend, our budgeting app.
#
# Authors:
#   - Nicholas Qiu
#   - Stephi Lyou
#   - Serena Lyou

import sys
import pathlib
import requests
from functions.auth import signup, login
from functions.appfuncs import *

from configparser import ConfigParser
class Client:
    def __init__(self,username,firstname,lastname):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        
def prompts():
    print("1. Add a budget")
    print("2. Edit a budget")
    print("2. View budgets summary")
    print("3. Add a transaction")
    print("4. Save transaction")
    print("6. Log out and Exit")
    s = input("Enter 1-6> ")
    return s        

def main():
    
    config_file = 'smartspend-client-config.ini'
    
    if not pathlib.Path(config_file).is_file():
        print("**ERROR: config file '", config_file, "' does not exist, exiting")
        sys.exit(0)
    
    # setup base URL to web service:
    configur = ConfigParser()
    configur.read(config_file)
    baseurl = configur.get('client', 'webservice')
    
    if len(baseurl) < 16:
        print("**ERROR: baseurl '", baseurl, "' is not nearly long enough...")
        sys.exit(0)

    if baseurl == "https://YOUR_GATEWAY_API.amazonaws.com":
        print("**ERROR: update config file with your gateway endpoint")
        sys.exit(0)

    if baseurl.startswith("http:"):
        print("**ERROR: your URL starts with 'http', it should start with 'https'")
        sys.exit(0)

    lastchar = baseurl[len(baseurl) - 1]
    if lastchar == "/":
        baseurl = baseurl[:-1]
    
    print("------SmartSpend!------")
    print()
    
    # eliminate traceback so we just get error message:
    sys.tracebacklimit = 0

    print("Sign up or log in?")
    print("1. Sign up")
    print("2. Log in")
    s = input("Enter 1 or 2> ")
    
    client = None
    
    if s != "1" and s != "2":
        return
    elif s == "1":
        username, first_name, last_name = signup(baseurl)
        
    elif s == "2":
        username, first_name, last_name = login(baseurl)
    
    client = Client(username, first_name, last_name)
        
    print("Welcome, ", client.firstname, " ", client.lastname, "!")
    
    s = 0
    while s != 6:
        s = prompts()
        
        match s:
            case "1":
                print("-----Add a Budget------")
                # TODO: add_budget()
                
            case "2":
                print("------Edit Budget------")
                # TODO: edit_budget()
            case "3":
                print("----Budget Summary-----")
                # TODO: view_budgets_summary()
            case "4":
                print("----New Transaction----")
                # TODO: add_transaction()
            case "5":
                print("---Save Transaction----")
                # TODO: save_transaction()
            case _:
                print("---Exited SmartSpend---")
        
if __name__ == "__main__":
    main()