def password_validation(password):
    """Checking password requirements for validation when registering account"""
    special_symbols = ["!", '$', '@', '#', '%', "^", "&", "*", "(", ")", "-", "=", "+", "_", "/", "<", ">", ":", ","] # some symbols to check whether the password contain symbols or not
    # symbols to use for checking whether a password contain symbols or not.
    status = True # boolean variable used for checking

    if len(password) < 7: # password length should be greater than 7
        status = False

    if len(password) > 15: # password length should be lower than 15
        status = False

    if not any(char.isdigit() for char in password): # checking each char in the password if there's a number or not
        status = False

    if not any(char.isupper() for char in password): # checking each char in the password if there's an uppercase letter or not
        status = False

    if not any(char.islower() for char in password): # checking each char in the password if there's an lowercase letter or not
        status = False

    if not any(char in special_symbols for char in password): # checking each char in the password if there's a symbol or not
        status = False

    if status: # if all requirements exist:
        return status # returning True