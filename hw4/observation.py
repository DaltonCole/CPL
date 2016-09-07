import datetime
import uuid
import json
from glob import glob

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
"""The format to use for observation times"""


def validate_observation_form(form):
    '''
    Checks that the form contains a “suspect” key

    Checks that the form contains a “location” key

    Checks that the form contains a “time” key

    Checks that the value of “suspect” is not blank

    Checks that the value of “location” is not blank

    Checks that the value of “time” is not blank

    If “time” was provided, checks that it can be loaded
    according to the observation.DATE_FORMAT format

    :Parameters: form (bottle.FormsDict) – A submitted form;
    retrieved from bottle.request

    :Returns:    A list of error messages. Returning the
    empty list indicates that no errors were found.
    '''
    errors = []
    # Check to see if suscpect is a key
    if 'suspect' in form.keys():
        # If suspect value is blank, add error
        if form['suspect'] == '':
            errors.append("suspect field cannot be blank!")
    # If not, add error to list
    else:
        errors.append('Missing suspect field!')
    # Check to see if location is a key
    if 'location' in form.keys():
        # If suspect value is blank, add error
        if form['location'] == '':
            errors.append("location field cannot be blank!")
    # If not, add error to list
    else:
        errors.append('Missing location field!')
    # Check to see if time is a key
    if 'time' in form.keys():
        # If time value is blank, add error
        if form['time'] == '':
            errors.append("time field cannot be blank!")
        # If time is in the wrong format, add error
        else:
            try:
                datetime.datetime.strptime(form['time'], DATE_FORMAT)
            except ValueError:
                errors.append("Bad time format: time data '{}' does "
                              "not match format "
                              "'%Y-%m-%d %H:%M:%S'".format(form['time']))
    # If not, add error to list
    else:
        errors.append('Missing time field!')
    return errors


def load_observation(o_filename):
    '''
    Observations are returned as dictionaries with the following attributes:
        id (str) - The ID of the observation. The same as its filename.
            Note that we do not store the id in the file. It is simply
            added to the loaded observation before we return it.
        suspect (str) - The name of the observed suspect
        reporter (str) - The name of the V.I.L.E. agent who
            submitted the observation report
        location (str) - The location where the suspect was observed
        time (datetime.datetime) - The time when the observation occurred

    Parameters: o_filename (str) – The name of the file that stores the
    observation data. The name should have the form observations/<uuid>.json,
    where <uuid> is a unique ID:

    Returns:    A loaded observation dict as described above
    '''
    # Open file to read observation from
    with open(o_filename, 'r') as obsdata:
        # Get file contents using json.loads
        obs = json.loads(obsdata.read())
        # Creat ID filed with file name minus extention
        obs['id'] = o_filename[:-5]
    # Convert time string to datetime format
    obs['time'] = datetime.datetime.strptime(obs['time'], DATE_FORMAT)
    return obs


def load_observations():
    '''
    Loads observations from the observations/ directory.

    Uses observation.load_observation() and glob.glob to create a
    new list of loaded observations. Observations are sorted
    according to their timestamp, so that the returned list
    starts with the most recent observation and ends with the least recent.

    :Returns:    A list of loaded observations ordered by
    timestamp from most to least recent.
    '''
    # Get list of every .json file in observations
    all_obs = glob("observations/*.json")
    # Create a list of observation dictionaries using load_observations
    # ---NOTE: Only Comprhention list, only place where I felt it was useful---
    loaded_obs_list = [load_observation(i) for i in all_obs]
    # Sort them in chronilogical order
    loaded_obs_list = sorted(loaded_obs_list, key=lambda time: time['time'])
    # Reverse chronicolize them
    loaded_obs_list.reverse()
    return loaded_obs_list


def save_observation(observation_dict):
    '''
    Saves an observation to disk.

    The observation disk contains the following fields:

    reporter (str) - The name of the V.I.L.E. agent who submitted
        the observation.
    suspect (str) - The name of the observed suspect
    location (str) - The location where the suspect was observed
    time (str) - The time the observation occurred
    The saved file is named uniquely by generating a UUID with Python’s
    built-in uuid.uuid4() function.

    The saved file has a .json extension and is stored in the
    observations/ directory.

    :Parameters: observation_dict (dict) – A dictionary
    containing observation information as described above.

    :Returns:    None
    '''
    # Create a random filename
    file_name = uuid.uuid4()
    # Add path and extention
    file_name = 'observations/' + str(file_name) + '.json'
    # Write file to disk
    with open(file_name, 'w') as outfile:
        json.dump(observation_dict, outfile)
