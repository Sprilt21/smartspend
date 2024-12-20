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
from configparser import ConfigParser
import requests
from pathlib import Path
import base64

def add_budget(baseurl, username):
    print("Enter the budget name:")
    budget_name = input("> ")
    print("Enter the budget amount:")
    budget_amt = input("> ")
    if budget_amt.isdigit():
        budget_amt = int(budget_amt)
    else:
        print("Error: Budget amount must be a number")
        return None
    
    #print(budget_amt)
    if not budget_name or not budget_amt:
        print("Error: Budget name and amount are required")
        return None
    
    if budget_amt < 0:
        print("Error: budget must be positive")
        return None
    data = {
        "username": username,
        "budget_name": budget_name,
        "budget_amt": float(budget_amt)
    }
    
    api = '/add-budget'
    url = baseurl + api
        
    res = requests.post(url, json=data)
        
    if res.status_code == 200:
        budget_id = res.json()
        print(f"Budget '{budget_name}' successfully added!")
        return {
            "budget_id": budget_id,
            "budget_name": budget_name,
            "budget_amt": budget_amt
        }
    else:
        print(f"Error: {res.text}")
        return None

def edit_budget(baseurl, username):
    print("Enter the name of the budget you want to edit")
    budget_name = input("> ")
    print("Enter the new budget amount")
    budget_amt = input("> ")

    if budget_amt.isdigit():
        budget_amt = int(budget_amt)
    else:
        print("Error: Budget amount must be a number")
        return None
    if not budget_name or not budget_amt:
        print("Error: Budget name and amount are required")
        return None

    if budget_amt < 0:
        print("Error: budget must be positive")
        return None

    data = {
        "username": username,
        "budget_name": budget_name,
        "budget_amt": budget_amt,
    }

    api = '/edit-budget'
    url = baseurl + api
        
    res = requests.patch(url, json=data)
    
    if res.status_code == 200:
        print("Budget updated successfully!")
        return True
    else:
        print(f"Error updating budget: {res.text}")
        return None

def view_budgets_summary(baseurl, username):
    
    # same thing as project03 basically, filter by user and display all budgets
        # get the sum of all budgets and the sum of all transactions
        # display the sum of all budgets and the sum of all transactions
        # display the remaining budget as a percentage of the total budget

    data = {
        "username": username,
    }
    
    api = '/budgets'
    url = baseurl + api
        
    res = requests.get(url, json=data)
        
    if res.status_code == 200:
        budgets = res.json()
            
        if not budgets:
            print("No budgets found.")
            return None
                
        print("\nYour current budgets:")
        print("------------------------")
        budgeted_total = 0
        current_total = 0
        for budget in budgets:
            budget_name, budget_amt, current_amt = budget
            budgeted_total += budget_amt
            current_total += current_amt
            print(f"Budget: {budget_name}")
            print(f"Amount: ${budget_amt:.2f}")
            print(f"Current Amount: ${current_amt:.2f}")
            print(f"Remaining: ${budget_amt - current_amt:.2f}")
            print("------------------------")
        
        print(f"Total Budgeted: ${budgeted_total:.2f}")
        print(f"Total Current: ${current_total:.2f}")
        print(f"Percent of budget used: {(current_total / budgeted_total) * 100:.2f}%")
        return budgets
            
    else:
        print(f"Error retrieving budgets: {res.text}")
        return None

def add_transaction(baseurl, username):
    
    #basically going to be entirely like project03 - upload the image to s3, upload the transaction to the database
        #maybe compress the image on upload? depends
        
    print("Enter the budget name:")
    budget_name = input("> ")
    print("Enter the receipt image filename:")
    receipt_img = input("> ")
    print("Enter a transaction description:")
    description = input("> ")
    
    if not budget_name or not receipt_img or not description:
        print("Error: budget name, receipt image, and description are required")
        return None
    
    if not Path(receipt_img).is_file():
        print("Error: file not found")
        return None
    
    infile = open(receipt_img, "rb")
    bytes = infile.read()
    infile.close()
    
    encoded = base64.b64encode(bytes)
    datastr = encoded.decode()
    
    data = {
        "budget_name": budget_name,
        "filename": receipt_img,
        "datastr": datastr,
        "desc": description
    }
    
    api = '/add_transaction/' + username
    url = baseurl + api
    #print(api)
    res = requests.post(url, json=data)
    
    if res.status_code == 200:
        transaction_id = res.json()
        print(f"Transaction with ID '{transaction_id}' successfully added!")
        return {
            "transaction_id": transaction_id,
            "budget_name": budget_name,
            "filename": receipt_img,
            "description": description
        }
    else:
        print(f"{res.status_code}")
        print(f"Error: {res.text}")
        return None

    
def view_transaction(baseurl, username):
    
    #download an image from s3 and save to a file + write other contents transaction contents to another file
    #
    # setup AWS based on config file:
    #
    try: 
        print("Enter the transaction id:")
        transaction_id = input("> ")

        if not transaction_id:
            print("Error: transaction id is required")
            return None

        api = '/view_transaction/' + transaction_id
        url = baseurl + api
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            image = data[0]
            details = data[1]
            if not image or not details:
                print("Error: transaction not found")
                return None

            decoded_details = base64.b64decode(details).decode("utf-8")

            transaction_username = None
            for line in decoded_details.split("\n"):
                if "User Name:" in line:
                    transaction_username = line.split(":")[1].strip()

            if not transaction_username:
                print("Error: Could not extract username from transaction details")
                return None

            if transaction_username != username:
                print("Error: not authorized to view this transaction")
                return None
            
            image_file = f"{transaction_id}_receipt.jpg"
            with open(image_file, "wb") as img_file:
                img_file.write(base64.b64decode(image))

            details_file = f"{transaction_id}_details.txt"
            with open(details_file, "w") as det_file:
                det_file.write(base64.b64decode(details).decode("utf-8"))
            
            print(f"Transaction details saved to {details_file}")
            print(f"Receipt image saved to {image_file}")
            return {
                "image": image_file,
                "details": details_file
            }
        else:
            print("**ERROR: view_transaction failed")
            print(f"Error: {res.json()}")
            return None    
    except Exception as e:
        print("**ERROR: view_transaction failed")
        print(f"Error: {e}")
        return None    