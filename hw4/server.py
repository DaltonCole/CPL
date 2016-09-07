# Python standard library imports
import argparse
import csv
import io
import os
import socket
import sys
from datetime import datetime
from glob import glob

# Third party library imports (installed with pip)
from bottle import (app, get, post, response, request, run,
                    jinja2_view, redirect, static_file)
from beaker.middleware import SessionMiddleware

# Local imports
from alerts import load_alerts, save_danger, save_success
from authentication import requires_login, validate_login_form, check_password
from observation import (validate_observation_form, load_observations,
                         save_observation)


@get('/')
@jinja2_view("templates/list_observations.html")
@requires_login
@load_alerts
def list_observations():
    """
    This handler returns a context dictionary with the following fields:

    observations: A list of loaded observations (dictionaries) in reverse
    chronological order (from most recent to least recent)

    :Returns:    a context dictionary (as described above) to be
    used by @jinja2_view to render a template.

    :Return type:    dict
    """
    return {'observations': load_observations()}


@get('/add/')
@jinja2_view("templates/add_observation.html")
@requires_login
@load_alerts
def show_observation_form():
    '''
    This handler returns an empty context dictionary.

    :Returns:    a context dictionary (as described above) to
    be used by @jinja2_view to render a template.
    :Return type:    dict
    '''
    return {}


@post('/add/')
def process_observation_form():
    '''
    Validates the submitted form

    If the form is has errors, saves the errors as danger alerts
    and redirects the user back to /add/

    Saves a new observation file to disk

    Save a success alert message

    Redirects the user to /

    Requires users to be logged in

    :Returns:    None.
    '''
    # Create a blank dict to store the form in
    form = {}
    # See if forms contains suspect
    try:
        form['suspect'] = request.forms['suspect']
    except:
        pass
    # See if forms contains location
    try:
        form['location'] = request.forms['location']
    except:
        pass
    # See if forms contains time
    try:
        form['time'] = request.forms['time']
    except:
        pass
    # Find possible errors from form
    errors = validate_observation_form(form)
    # Save errors and redirect
    if errors:
        for alerts in errors:
            save_danger(alerts)
        redirect('/add/')
    # Add reporter field to form
    form['reporter'] = request.get_cookie('logged_in_as')
    # Save form, save success alert, and redirect
    save_observation(form)
    save_success("New observation added!")
    redirect("/")


# For this route, observation_id must be 36 characters in length, all
# hexadecimal and dashes.
@get('/remove/<observation_id:re:[0-9a-f\-]{36}>/')
@jinja2_view("templates/remove_observation.html")
@requires_login
@load_alerts
def show_removal_confirmation_form(observation_id):
    '''
    Shows a form that can be used to delete an existing observation.

    Requires users to be logged in

    Loads alerts for display

    Uses “templates/remove_observation.html” as its template
    This handler returns a context dictionary with the following fields:
        observation_id: The ID (UUID) of the observation to remove, as a string

    :param: uuid to be removed

    :Returns:    a context dictionary to be used by
    @jinja2_view to render a template.

    :Return type:    dict
    '''
    return {'observation_id': observation_id}


@post('/remove/<observation_id:re:[0-9a-f\-]{36}>/')
def remove_observation(observation_id):
    '''
    Attempts to remove the observation with id observation_id

    If the file could not be removed (OSError), then a danger alert is saved.

    If the file was removed successfully, a success alert is saved.

    In either case, the user is redirected to /

    Requires users to be logged in

    :param: uuid to be removed (no json extention)

    :Returns:    None.
    '''
    # Try to the specified json file from observations directory
    try:
        rmfile = "observations/" + observation_id + '.json'
        os.remove(rmfile)
    # If error, log danger error
    except:
        save_danger('No such observation {}'.format(observation_id))
    # Otherwise log success
    else:
        save_success('Removed {}.'.format(observation_id))
    # Then redirect to main page
    finally:
        redirect("/")


@get('/clear/')
@jinja2_view("templates/clear_observations.html")
@requires_login
@load_alerts
def show_clear_confirmation_form():
    # This function doesn't need to pass any data to the template.
    # Simply return {}
    return {}


@post('/clear/')
def clear_observations():
    '''
    Attempts to remove all saved observation files

    If the files could not be removed (an exception of some sort),
    then a danger alert is saved.

    If the files were removed successfully, a success alert is saved.

    In either case, the user is redirected to /

    Requires users to be logged in

    Returns:    None.
    '''
    # Try to remove all json files from observations directory
    try:
        filelist = glob("observations/*.json")
        for f in filelist:
            os.remove(f)
    # If error, log danger error
    except:
        save_danger("Clear Observations failed")
    # Otherwise log success
    else:
        save_success("Cleared all observations.")
    # Then redirect to main page
    finally:
        redirect("/")


@get('/download/')
@requires_login
def download_csv():
    '''
    Lists observations by formatting them as CSV

    Requires users to be logged in

    :Returns:    The loaded observations (in reverse chronological order) in
    CSV format. The three columns should correspond to
    suspect, location, and time, respectively.

    :Return type:    str
    '''
    # Load observations
    obs = load_observations()
    # Set HTTP response's Content-Type header
    response.content_type = 'text/plain; charset=ascii;'
    # Write to io.StringIO to prevent using a temporary file
    with io.StringIO() as d:
        # set fieldnames (header of csv file)
        fieldnames = ['suspect', 'location', 'time']
        writer = csv.DictWriter(d, fieldnames=fieldnames)
        # Write every dict in obs to csv file
        for i in obs:
            writer.writerow({'suspect': i['suspect'], 'location':
                            i['location'], 'time': i['time']})
        # Get string of StringIO, so we can close first
        contents = d.getvalue()
    # Return contents of obs in csv formated string
    return contents


@get('/login/')
@jinja2_view("templates/login.html")
@load_alerts
def show_login_form():
    """Handler for GET Requests to /login/ path.

    * Shows a form that can be used to submit login credentials
    * Loads alerts for display
    * Uses "templates/login.html" as its template
    """
    # This function doesn't need to pass any data to the template.
    # Simply return {}
    return {}


@post('/login/')
def process_login_form():
    """Handler for POST Requests to /login/ path.

    * Processes the login form

        1. Validates the submitted form

            * If the form is has errors, saves the errors as
              danger alerts and redirects the user back to /login/

        2. Checks that the user's username/password combo is good

            * Usernames are case insensitive

        3. Redirects the user

            - If their credentials were good, set their
              ``logged_in_as`` cookie to their username, save a
              success alert, and redirect them to "/"
            - If their credentials were bad, save a danger alert, and
              redirect them to "/login/"

    * Requires users to be logged in

    """
    errors = validate_login_form(request.forms)
    if errors:
        save_danger(*errors)
        redirect('/login/')

    username = request.forms['username'].lower()
    password = request.forms['password']

    # TODO some kind of actual authentication
    if check_password(username, password):
        response.set_cookie("logged_in_as", username, path='/')
        save_success("Successfully logged in as {}.".format(username))
        redirect("/")
    else:
        save_danger("Incorrect username/password information.")
        redirect("/login/")


@get('/logout/')
@jinja2_view("templates/logged_out.html")
@load_alerts
def logout():
    """Handler for GET Requests to /logout/ path.

    * Logs a user out by setting their "logged_in_as" cookie to ""
    * Loads alerts for display
    * Uses "templates/logged_out.html" as its template
    """
    response.set_cookie("logged_in_as", "", path="/")
    return {}


@get('/assets/<path:path>')
def get_style_file(path):
    """Handler for GET requests to /assets/<path>/ path.

    * Returns file contents of site assets. CSS, JavaScript, images,
      fonts, etc.

    **This function doesn't need to be changed.**

    """
    return static_file(path, root="assets")


# Configuration options for sessions.
# Used by alerts module
session_options = {
    'session.type': 'cookie',
    'session.validate_key': 'super-secret'
}

# Configures the app to use sessions middleware
observation_app = app()
observation_app = SessionMiddleware(observation_app, session_options)

if __name__ == '__main__':
    # Set up a command line argument parser
    parser = argparse.ArgumentParser(
        description='Run the V.I.L.E. Observation Reporting Web Application'
    )

    # A required --port argument, so that the user knows which port
    # they're binding to.
    parser.add_argument('--port', type=int, required=True,
                        help='The port number to listen on.')

    # Allow the user to specify a hostname, defaulting to 0.0.0.0
    # (i.e., "Bind to all network interfaces")
    parser.add_argument('--host', type=str, default="0.0.0.0",
                        help='The hostname to listen on.')

    # Parse CLI args
    args = parser.parse_args()

    # Make sure it's in the range we want
    if args.port < 8000 or args.port >= 9000:
        print("Please use a port in the range [8000, 9000).", file=sys.stderr)
        sys.exit(1)

    try:
        # Attempt to bind to the port, just to make sure that it's free
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((args.host, args.port))
        s.close()
    except OSError:
        # If it's NOT free, then it's time to bail. The user needs to
        # specify a different port number to bind to.
        fmt = "Looks like port {} is taken! Choose a different one."
        print(fmt.format(args.port), file=sys.stderr)
        sys.exit(1)

    # Run the app!
    run(
        app=observation_app,             # Use the bottle application
                                         # we made

        host=args.host, port=args.port,  # Bind to the provided
                                         # host/port

        debug=True,                      # Use debug mode (shows
                                         # helpful error pages
                                         # whenever there's a problem
                                         # with the code)

        reloader=True                    # Reload the web app whenever
                                         # a module changes
    )
