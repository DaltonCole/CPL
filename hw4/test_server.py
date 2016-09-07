# Python standard library imports
import csv
import io
import json
import os
import pickle
import random
import string

from base64 import b64decode
from datetime import datetime, timedelta
from glob import glob
from urllib.parse import urlsplit

# Other libraries
from webtest import TestApp as HelperApp  # To avoid confusing PyTest

# Our code
import server
import observation


def assert_redirect_to_login(path):
    """A helper function to test that we're redirected if we're not
    logged in.

    """
    app = HelperApp(server.observation_app)

    # Assert that we get redirected
    response = app.get(path)
    assert response.status == "302 Found"

    # Make sure the redirect is going to the right place
    assert urlsplit(response.location).path == "/login/"


def assert_not_redirect_to_login(path):
    """A helper function to test that we're not redirected if we're
    logged in.

    """
    app = HelperApp(server.observation_app)

    # Login as Carmen
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Assert that we're not redirected
    response = app.get(path)
    assert response.status == "200 OK"


def unpack_alerts(cookies):
    return pickle.loads(b64decode(cookies['beaker.session.id'][40:]))['alerts']


def test_load_observations_type():
    """Make sure that load_observations returns the types we want."""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Add a bunch of observations
    time = datetime.fromtimestamp(0)
    for l in string.ascii_lowercase:
        time += timedelta(minutes=random.randint(1, 10))
        app.get('/add/')
        app.post('/add/', {'suspect': l, 'location': l.upper(), 'time': time})

    for o in observation.load_observations():
        # Check that our keys match up
        assert set(o) == {'id', 'reporter', 'suspect', 'location', 'time'}

        # Check all the types
        assert isinstance(o['id'], str)
        assert isinstance(o['reporter'], str)
        assert isinstance(o['suspect'], str)
        assert isinstance(o['location'], str)
        assert isinstance(o['time'], datetime)


def test_load_observations_order():
    """Make sure that load_observations maintains order for us."""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Add a bunch of observations
    time = datetime.fromtimestamp(0)
    for l in string.ascii_lowercase:
        time += timedelta(minutes=random.randint(1, 10))
        app.get('/add/')
        app.post('/add/', {'suspect': l, 'location': l.upper(), 'time': time})

    all_obs = observation.load_observations()
    for prev, current in zip(all_obs, all_obs[1:]):
        assert prev['time'] > current['time']


def test_add_success_alerts():
    """Try adding an observation and check for success messages."""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Clear alerts
    app.get('/')

    # Add an observation
    time = datetime.fromtimestamp(0)
    app.post('/add/', {'suspect': "Frog", 'location': "Place", 'time': time})

    # Unpack the alerts from the session cookie, and assert that we
    # see the right message
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 1, "Expected exactly one alert message"
    assert alerts == [{'kind': 'success',
                       'message': 'New observation added!'}]


def test_add_missing_fields_alerts():
    """Check that we warn for missing fields"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Clear alerts
    app.get('/')

    # Blank fields
    app.post('/add/', {'suspect': "", 'location': "", 'time': ""})

    # Make sure we warn
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 3
    assert alerts == [
        {'kind': 'danger', 'message': 'suspect field cannot be blank!'},
        {'kind': 'danger', 'message': 'location field cannot be blank!'},
        {'kind': 'danger', 'message': 'time field cannot be blank!'},
    ]


def test_add_bad_time_alert():
    """Check that we warn for bad time formatting"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Clear alerts
    app.get('/')

    # Bad time field
    app.post('/add/', {'suspect': "A", 'location': "B", 'time': "nope"})

    # Make sure we warn
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 1
    assert alerts == [{'kind': 'danger',
                       'message': "Bad time format: time data 'nope' does "
                                  "not match format '%Y-%m-%d %H:%M:%S'"}]


def test_add_form_validation():
    """Check that we warn for bad forms"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Clear alerts
    app.get('/')

    # Missing fields
    app.post('/add/', {'suspec': "A", 'locatio': "B", 'tim': "nope"})

    # Make sure we warn
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 3
    assert alerts == [
        {'kind': 'danger', 'message': "Missing suspect field!"},
        {'kind': 'danger', 'message': "Missing location field!"},
        {'kind': 'danger', 'message': "Missing time field!"}
    ]


def test_add_files():
    """Try adding a bunch of observations, ensuring that files are created
    on disk.

    """
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    time = datetime.fromtimestamp(0)
    for l in string.ascii_lowercase:
        time += timedelta(minutes=random.randint(1, 10))
        app.get('/add/')
        app.post('/add/', {'suspect': l, 'location': l.upper(), 'time': time})

    obs_filenames = glob("observations/*.json")
    assert len(obs_filenames) == 26

    letters = set()
    for obs_name in obs_filenames:
        with open(obs_name) as obs_file:
            obs_data = json.load(obs_file)

        # Assert that the set of keys is what we want
        assert set(obs_data) == {"reporter", "suspect", "location", "time"}

        # Since we're logged in as Carmen
        assert obs_data['reporter'] == 'carmen'

        # Check that we saved the suspect and location correctly
        # (location is the uppercase version of suspect)
        assert ord(obs_data['suspect']) == ord(obs_data['location']) + 32

        # Remember all the letters we've seen so far
        letters.add(obs_data['suspect'])

        # Make sure we can load the time correctly -- shouldn't throw
        # an exception
        datetime.strptime(obs_data['time'], "%Y-%m-%d %H:%M:%S")

    assert letters == set(string.ascii_lowercase)


def test_remove_success_alert():
    """Try removing an observation, ensuring there's a success message"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Add a an observation
    time = datetime.fromtimestamp(0)
    app.post('/add/', {'suspect': 'a', 'location': 'b', 'time': time})
    app.get('/')        # Clears alerts

    # Remove something real
    obs_file, = glob("observations/*.json")
    obs_id = os.path.basename(obs_file).rstrip('.json')
    app.post('/remove/{}/'.format(obs_id))

    # Make sure we display a success message
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 1
    assert alerts == [{'kind': 'success',
                       'message': 'Removed {}.'.format(obs_id)}]


def test_remove_bogus_alert():
    """Try removing a bogus observation, ensuring there's a warning"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Add a an observation
    time = datetime.fromtimestamp(0)
    app.post('/add/', {'suspect': 'a', 'location': 'b', 'time': time})
    app.get('/')        # Clears alerts

    # Remove something bogus
    # Pick some arbitrary UUID. Collision is improbable.
    bogus_uuid = "b58cba44-da39-11e5-9342-56f85ff10656"
    app.post('/remove/{}/'.format(bogus_uuid))

    # Make sure we warn the user about it
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 1
    assert alerts == [{'kind': 'danger',
                       'message': 'No such observation {}'.format(bogus_uuid)}]


def test_remove():
    """Try adding a bunch of observations, and delete a couple items"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    time = datetime.fromtimestamp(0)
    for l in string.ascii_lowercase:
        time += timedelta(minutes=random.randint(1, 10))
        app.post('/add/', {'suspect': l, 'location': l.upper(), 'time': time})

    # We should have all 26
    assert len(glob("observations/*.json")) == 26

    for obs_name in glob("observations/*.json"):
        obs_id = os.path.basename(obs_name).rstrip('.json')

        # The file should be in there
        assert obs_name in glob("observations/*.json")

        # Get the form (to make sure it doesn't change anything on disk)
        app.get('/remove/{}/'.format(obs_id))

        # The file should still be in there
        assert obs_name in glob("observations/*.json")

        # Try to delete it
        app.post('/remove/{}/'.format(obs_id))

        # The file should be gone
        assert obs_name not in glob("observations/*.json")

    # Ain't nothin' left, I'll tell ya what.
    assert len(glob("observations/*.json")) == 0


def test_clear_success_alert():
    """Try clearing observations, ensuring there's a success message"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    # Add a an observation
    time = datetime.fromtimestamp(0)
    app.post('/add/', {'suspect': 'a', 'location': 'b', 'time': time})
    app.get('/')        # Clears alerts

    # Remove something bogus
    app.post('/clear/')

    # Make sure we warn the user about it
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 1
    assert alerts == [{'kind': 'success',
                       'message': 'Cleared all observations.'}]


def test_clear():
    """Try adding a bunch of observations, and clear them out"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    time = datetime.fromtimestamp(0)
    for l in string.ascii_lowercase:
        time += timedelta(minutes=random.randint(1, 10))
        app.post('/add/', {'suspect': l, 'location': l.upper(), 'time': time})

    # We should have all 26
    assert len(glob("observations/*.json")) == 26

    # This shouldn't change the files
    app.get('/clear/')

    # We should still have all 26
    assert len(glob("observations/*.json")) == 26

    # Delete all the observation files
    app.post('/clear/')

    # OK, now they're gone.
    assert len(glob("observations/*.json")) == 0


def test_download():
    """Try adding a bunch of observations, and clear them out"""
    app = HelperApp(server.observation_app)
    app.post('/login/', {'username': 'carmen', 'password': 'frog'})

    time = datetime.fromtimestamp(0)
    for l in string.ascii_lowercase:
        time += timedelta(minutes=random.randint(1, 10))
        app.post('/add/', {'suspect': l, 'location': l.upper(), 'time': time})

    # We should have all 26
    assert len(glob("observations/*.json")) == 26

    # This shouldn't change the files
    response = app.get('/download/')

    # We should have all 26 as rows in the CSV file
    assert len(response.text.splitlines()) == 26

    # We know they'll be in reversed alphabetical order, since we
    # increased the time as we added them and they're sorted most
    # recent to least recent.
    reader = csv.reader(io.StringIO(response.text))
    for letter, row in zip(reversed(string.ascii_lowercase), reader):
        suspect, location, time = row
        assert suspect == letter
        assert location == letter.upper()


def test_list_login():
    """Make sure we get redirected as expected for /"""
    assert_redirect_to_login('/')
    assert_not_redirect_to_login('/')


def test_add_login():
    """Make sure we get redirected as expected for /add/"""
    assert_redirect_to_login('/add/')
    assert_not_redirect_to_login('/add/')


def test_remove_login():
    """Make sure we get redirected as expected for /remove/"""
    # Pick some arbitrary UUID.
    uuid = "b58cba44-da39-11e5-9342-56f85ff10656"
    assert_redirect_to_login('/remove/{}/'.format(uuid))
    assert_not_redirect_to_login('/remove/{}/'.format(uuid))


def test_clear_login():
    """Make sure we get redirected as expected for /clear/"""
    assert_redirect_to_login('/clear/')
    assert_not_redirect_to_login('/clear/')


def test_download_login():
    """Make sure we get redirected as expected for /download/"""
    assert_redirect_to_login('/download/')
    assert_not_redirect_to_login('/download/')


def test_login_form_alerts():
    """Make sure login forms are validated"""
    app = HelperApp(server.observation_app)

    # Use bad field names
    response = app.post('/login/', {'usernam': 'carmon', 'passwor': 'frog'})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/login/"

    # Check for alerts
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 2
    assert alerts == [
        {'kind': 'danger', 'message': 'Missing username field!'},
        {'kind': 'danger', 'message': 'Missing password field!'}
    ]

    # Clear EVERYTHING (including alerts)
    app.reset()

    # Use blank field names
    response = app.post('/login/', {'username': '', 'password': ''})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/login/"

    # Check for alerts
    alerts = unpack_alerts(app.cookies)
    assert len(alerts) == 2
    assert alerts == [
        {'kind': 'danger', 'message': 'username field cannot be blank!'},
        {'kind': 'danger', 'message': 'password field cannot be blank!'}
    ]


def test_login():
    """Make sure login works as we expect"""
    app = HelperApp(server.observation_app)

    # The page loads up
    response = app.get('/login/')
    assert response.status == "200 OK"

    # Doesn't work with a bad username
    response = app.post('/login/', {'username': 'carmon', 'password': 'frog'})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/login/"
    assert app.cookies.get('logged_in_as') is None

    # Doesn't work with a bad password
    response = app.post('/login/', {'username': 'carmen', 'password': 'fwog'})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/login/"
    assert app.cookies.get('logged_in_as') is None

    # Doesn't work with arbitrary password capitalization
    response = app.post('/login/', {'username': 'carmen', 'password': 'FROG'})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/login/"
    assert app.cookies.get('logged_in_as') is None

    # Works with a good password
    response = app.post('/login/', {'username': 'carmen', 'password': 'frog'})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/"
    assert app.cookies['logged_in_as'] == "carmen"

    # Works with various username capitalization
    response = app.post('/login/', {'username': 'CaRmEn', 'password': 'frog'})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/"
    assert app.cookies['logged_in_as'] == "carmen"


def test_logout():
    """Make sure logout works as we expect"""
    app = HelperApp(server.observation_app)
    response = app.post('/login/', {'username': 'carmen', 'password': 'frog'})
    assert response.status == "302 Found"
    assert urlsplit(response.location).path == "/"
    assert app.cookies['logged_in_as'] == "carmen"

    response = app.get('/logout/')
    assert response.status == "200 OK"
    assert app.cookies['logged_in_as'] == ""
