from bottle import request, redirect
import json


def requires_login(func):
    '''
    Updates a handler, so that a user is redirected to
    /login/ if they are not currently logged in.

    The wrapped function should be a handler function. When a user
    attempts to visit the path for the wrapped handler,
    this wrapper will check to see if the user is logged in...

    If the “logged_in_as” cookie is missing or blank, then
    the user is not logged in. They are redirected to
    /login/ using bottle.redirect().

    Otherwise, the handler is called as usual.

    :Parameters: func – A handler function to wrap

    :Returns:    The wrapped function
    '''
    def wrapper(*args, **kwargs):
        # See if logged_in_as cookie exists
        if 'logged_in_as' in request.cookies:
            # If empty string, redirect to login page
            if request.get_cookie('logged_in_as') == '':
                redirect("/login/")
        # If it does not, redirect to login page
        else:
            redirect("/login/")
        return func(*args, **kwargs)
    return wrapper


def validate_login_form(form):
    '''
    Validates a login form in the following ways:

    Checks that the form contains a “username” key
    Checks that the form contains a “password” key
    Checks that the value for “username” is not blank
    Checks that the value for “password” is not blank

    Parameters: form (bottle.FormsDict) – A submitted form;
    retrieved from bottle.request

    :Returns:    A list of error messages. Returning the
    empty list indicates that no errors were found.
    '''
    # Create an empty list to contain errors
    errors = []
    # If no username, add error
    if 'username' not in form.keys():
        errors.append('Missing username field!')
    # Else if empty string, add error
    elif form['username'] == '':
        errors.append('username field cannot be blank!')
    # If no password, add error
    if 'password' not in form.keys():
        errors.append('Missing password field!')
    # Else if empty password string, add error
    elif form['password'] == '':
        errors.append('password field cannot be blank!')
    return errors


def check_password(username, password):
    '''
    Checks a user’s password using a plaintext password file.

    Opens a file named “passwords.json”, and loads the
    JSON-formatted data using the built-in Python module json.

    Usernames are case insensitive.

    Note that all usernames in “passwords.json” are stored in lowercase.

    :para: username (str) – The username to check

    :para: password (str) – The password to check

    :Returns:    True if the username/password pair
    was in “passwords.json”, otherwise False
    '''
    # Open password json file
    with open('passwords.json', 'r') as credentials:
        # Read in dictionary of username and passwords
        cred_dict = json.loads(credentials.read())
        try:
            # Check to see if password matches for username
            if cred_dict[username] == password:
                return True
        except:
            pass
    return False
