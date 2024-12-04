###################################
#
# Client for our budgeting app.
#
# Authors:
#   - Nicholas Qiu
#   - Stephi Lyou
#   - Serena Lyou
import sys

def main():
    print("-----SmartSpend!-----")
    
    print()
    
    
    # eliminate traceback so we just get error message:
    sys.tracebacklimit = 0

    print("Sign up or log in?")
    print("1. Sign up")
    print("2. Log in")
    s = input("Enter 1 or 2> ")
    
    if s != "1" and s != "2":
        return
    elif s == "1":
        print("-------Sign Up-------")
        print("Enter your username:")
        username = input("> ")
        print("Enter your password:")
        password = input("> ")
        print("Enter your email:")
        email = input("> ")
        print("Enter first name:")
        first_name = input("> ")
        print("Enter last name:")
        last_name = input("> ")
        
        # send to server
        # TODO
    elif s == "2":
        print("-------Log In-------")
        print("Enter your username:")
        username = input("> ")
        print("Enter your password:")
        password = input("> ")
        
        # send to server
        # TODO
        
if __name__ == "__main__":
    main()