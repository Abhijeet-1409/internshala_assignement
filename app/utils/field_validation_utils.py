import re
from bson import ObjectId

def check_username_validity(username: str) -> str:
    # Check if the username starts with a letter or an underscore
    if username:
        if not re.match(r'^[A-Za-z_]', username):  # Starts with a letter or underscore
            raise ValueError('Username must start with a letter or an underscore.')
        if not re.match(r'^[A-Za-z0-9_]*$', username):  # Contains only letters, numbers, or underscores
            raise ValueError('Username can only contain letters, numbers, or underscores.')
    return username


def check_password_validity(password: str) -> str:
        # Check if the password starts with a letter and contains at least one digit and one special character
        if password:
            if not re.match(r'^[A-Za-z]', password):  # Starts with a letter
                raise ValueError('Password must start with a letter.')
            if not re.search(r'\d', password):  # Contains at least one digit
                raise ValueError('Password must contain at least one number.')
            if not re.search(r'[\W_]', password):  # Contains at least one special character
                raise ValueError('Password must contain at least one special character.')
        return password


def objectid_to_str(id: ObjectId) -> str:
    # Helper function to convert ObjectId to string for Pydantic model
    return str(id)