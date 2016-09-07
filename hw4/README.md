# V.I.L.E. Observation Database

This project contains a Python program designed to aid with the collection and inspection of observations submitted by V.I.L.E. agents.
Documentation for its behavior can be found publicly here: http://cpl.mwisely.xyz
To verify that the code works properly, your code must pass the provided tests.

**Note: Follow the design specifications EXACTLY.**
Not doing so will break our existing, complete test suite and hurt your grade.
Additionally, HTML templates (which you should not edit) may not render properly.

## Running Tests

To run your tests, do the following:

~~~shell
# Activate your virtualenv (which is already setup and named "env")
$ source env/bin/activate
(env) $ py.test
~~~~

**Note: this will work on campus machines. If you use your own machine, you are on your own.**

## Checking Your Style

To check your style with flake8, do the following:

~~~shell
# Activate your virtualenv (which is already setup and named "env")
$ source env/bin/activate
(env) $ flake8 *.py
~~~~

## Running the Program

To run the web application, do the following:

~~~shell
# Activate your virtualenv (which is already setup and named "env")
$ source env/bin/activate
(env) $ python3.4 server.py --port=<portnumber>
~~~

... where `<portnumber>` is a port number of your choosing in the range (8000, 9000].

[1]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
