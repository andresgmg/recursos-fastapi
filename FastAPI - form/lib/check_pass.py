from model.handle_db import Handle_DB
from werkzeug.security import check_password_hash

# Define a function that takes in a username and password as parameters
def check_user(username, passw):
    # Create an instance of the Handle_DB class to interact with the database
    user = Handle_DB()
    # Retrieve a user record from the database based on the provided username
    filter_user = user.get_only(username)
    # If a user record is found
    if filter_user:
        # Check if the provided password matches the hashed password stored in the user record
        same_passw = check_password_hash(filter_user[4], passw)
        # If the passwords match
        if same_passw:
            # Return the user record
            return filter_user
    # If no user record is found or the password does not match
    # Return None to indicate that the login attempt was unsuccessful
    return None