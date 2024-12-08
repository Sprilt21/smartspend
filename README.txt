The python packages "requests" and "cryptography" are needed to run our client.

requests and cryptography may need to be installed via pip:

to do this, run "pip install requests cryptography" or "python -m pip install requests cryptography"

To run our client, run "python client.py", or "python3 client.py".

Most of the functions are done in AWS, so our client just needs to be run,
and the rest of the functions will be handled by AWS.

Files:
    client.py - handles user input, calls functions based on prompts
    functions:
        auth.py - handles sign in and log in of user, functions are called by client.py
        appfuncs.py - handles main app functions (add/edit budgets and transactions, view and download of budgets and transactions)