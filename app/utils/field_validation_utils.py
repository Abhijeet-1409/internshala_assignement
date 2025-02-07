import re
from bson import ObjectId
from email_validator import EmailNotValidError
from pydantic import EmailStr, validate_email

def check_username_validity(username: str) -> str:
 
    if not re.match(r'^[A-Za-z_]', username): 
        raise ValueError('Username must start with a letter or an underscore.')
    if not re.search(r'\d', username): 
        raise ValueError('username must contain at least one number.')
    if not re.search(r'[@_$]', username):  
        raise ValueError("Username must contain at least one special character ('@', '_', or '$').")

    return username


def check_password_validity(password: str) -> str:
    
    if not re.match(r'^[A-Za-z]', password):  
        raise ValueError('Password must start with a letter.')
    if not re.search(r'\d', password): 
        raise ValueError('Password must contain at least one number.')
    if not re.search(r'[@%$]', password):  
        raise ValueError("Password must contain at least one special character ('@', '%', or '$').")
    
    return password


def check_email_validity(email:EmailStr ):
    try:
        validate_email(value=email)
    except EmailNotValidError as email_exe:
        raise ValueError("Invalid email address. Please enter a valid email.")
    except Exception as exe:
        raise exe

    return email


def objectid_to_str(id: ObjectId) -> str:
    # Helper function to convert ObjectId to string for Pydantic model
    return str(id)