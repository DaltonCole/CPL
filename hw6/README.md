# Turnip - A 21st Century Personal Assistant

Turnip is a [Hubot](http://hubot.github.com) designed to assist Carmen Sandiego with some simple tasks.

This project contains several scripts (within the `scripts/` directory) that will enable a Hubot to perform several useful actions.
Documentation for its behavior can be found publicly here: <http://cpl.mwisely.xyz>.
To verify that the code works properly, your code must pass the provided tests.
A sample conversation has been included for comparison.

**Note: Follow the documentation in the source code.**
Failure to do so may cause the existing test suite to fail and hurt your grade.

**Note: the following procedure will work on campus machines.**
**If you use your own machine for development, you are on your own.**

## A note on Git

**Do not** commit any of the following:

- The `bin` link made by `setup.sh`
- The `.my_nodejs` directory, which contains the downloaded and unpacked copes of Node.js
- The `node_modules` directory, which contains downloaded third-party libraries

They should be ignored automatically by Git, but still.
Don't commit them.

## Install a local copy of Node.js

`setup.sh` will download, verify, and unpack a copy of Node.js v4.3.1 in a hidden directory in your repository.
Then it'll create a link named `bin`, which you can use to access the `node` and `npm` executables that were installed.

~~~ shell
$ bash setup.sh

# ... a bunch of output
~~~

## Install Prerequisite Packages

~~~ shell
$ ./bin/npm install -d
~~~~

This will have `npm` install the necessary packages listed in the `package.json` file.
You'll have to run this before you run the tests or style checker.

## Run Tests

~~~ shell
$ ./mocha.sh --compilers "coffee:coffee-script/register" test/*.coffee
~~~~

This will run the `Mocha` package which runs the tests in the `test` directory.
The additional flag tells `Mocha` to compile the CoffeeScript files into JavaScript prior to executing them.

**Don't rename or remove the `test` directory, `Mocha` needs this.**

## Check Style

~~~ shell
$ ./coffeelint.sh scripts/*.coffee test/*.coffee
~~~~

This will run the `CoffeeLint` package to check for possible style and logic errors in `scripts/` and `test/`.

## Run the Program

~~~ shell
$ ./hubot.sh
Hubot>
~~~

This will invoke Hubot.
Hubot will then look in `scripts/` for Turnip's custom scripts and compile them as required.

## Trying out CoffeeScript

~~~ shell
$ ./coffee.sh
coffee>
~~~

This will start the CoffeeScript REPL.
You don't have to compile any CoffeeScript files in `test/` or `script/`.
That's taken care of automatically.

We simply included `coffee.sh`, so that you can play around with the CoffeeScript interpreter and compiler.

<!--  LocalWords:  executables REPL js Hubot Sandiego CoffeeScript
 -->
<!--  LocalWords:  CoffeeLint hubot
 -->
