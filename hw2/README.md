# V.I.L.E. XY77 Battering Ram

This project contains a Python program designed to aid in the bypassing of security layers on a XY77 Series Quad-layer Vault.
Documentation for its behavior can be found publicly here: http://cpl.mwisely.xyz
To verify that the code works properly, you must complete any partial test functions that are given.

**Note: Do NOT change any function names or argument lists in `main.py`.**
Doing so will break our existing, complete test suite.

## Regarding Tests

The unit tests have been partially implemented.
The `test_which_to_press` test is sufficiently implemented, while the others still need attention.
Use the `vault_state` variables given to you.

It is going to be difficult to test any function that uses the `input` function, so do not worry about those functions.
If you wish to create more tests to better verify the behavior of the program, simply add more test functions to `test_main.py`.

## Running Your Tests

Tests for this program have been written using [pytest](http://pytest.org).
In order to run these tests, you must have access to a pytest executable.
We understand some of our agents do not have access to machines with pytest installed.
Thus, a script has been included to install (if necessary) and run pytest automatically.
This script creates a [virtual environment][1] within the project so that no system files are affected.

To run the tests, use the script as shown below:

~~~shell
# Assuming that you are at the top directory of your project
./py.test
~~~

**Note: this will work on campus machines. If you use your own machine, you are on your own.**

## Checking Your Style

Carmen Sandiego loves PEP 0008.

Again, we realize that not everyone has access to a PEP 0008 checker.
Thus, a script has been included to install (if necessary) and run flake8 automatically.
flake8 is a PEP 0008 checker and Python linter.

To check your style with flake8, do the following:

~~~shell
# Assuming that you are at the top directory of your project
./flake8
~~~~

## Running the Program

To run the battering ram program interactively, do the following:

~~~shell
# Assuming that you are at the top directory of your project
python3.4 main.py
~~~

To run the battering ram program with predefined inputs, do the following:

~~~shell
# Assuming that you are at the top directory of your project
python3.4 check_expectations.py
~~~

You are welcome to modify the `check_expectations.py` program as you wish.
This is a very useful tool for speeding up the development process.
No need to type the same input over and over and over and over again.
Let the computer do it for you.
It is 2016 for pete's sake.

[1]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
