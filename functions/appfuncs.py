###################################
#
# Functions for the main features
# in our SmartSpend application.
#   - add_budget
#   - edit_budget
#   - view_budgets_summary
#   - add_transaction
#   - save_transaction
#
# Authors:
#   - Nicholas Qiu
#   - Stephi Lyou
#   - Serena Lyou
import requests
import uuid
import json

def add_budget(baseurl, username):
    
    #basically going to be entirely like project03 - just upload a budget to the database, no s3 here
        
    pass

def edit_budget(baseurl, username):
    
    #get a budget, update the max amount, and upload the updated budget to the database
    
    pass

def view_budgets_summary(baseurl, username):
    
    # same thing as project03 basically, filter by user and display all budgets
        # get the sum of all budgets and the sum of all transactions
        # display the sum of all budgets and the sum of all transactions
        # display the remaining budget as a percentage of the total budget
        
    pass

def add_transaction(baseurl, username):
    
    #basically going to be entirely like project03 - upload the image to s3, upload the transaction to the database
        #maybe compress the image on upload? depends
    pass

def view_transaction(baseurl, username):
    
    #download an image from s3 and save to a file + write other contents transaction contents to another file
    
    pass
