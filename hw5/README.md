# Purchase Plotter Program

Carmen Sandiego needs assistance with her taxes.

This project contains a Node.js program designed to aid with the aggregation of provided purchase information.
Documentation for its behavior can be found publicly here: <http://cpl.mwisely.xyz>.
To verify that the code works properly, your code must pass the provided tests.
Sample input and output data has also been provided for your benefit.

**Note: Follow the design specifications EXACTLY.**
Not doing so will cause the existing test suite to fail and hurt your grade.

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

# Then we can start the Node.js REPL!
$ ./bin/node
>
~~~


## Install Prerequisite Packages

~~~ shell
$ ./bin/npm install -d
~~~~

This will have `npm` install the necessary packages listed in the `package.json` file.
You'll have to run this before you run the tests or style checker.

## Run Tests

~~~ shell
$ ./mocha.sh
~~~~

This will run the `Mocha` package which runs the tests in the `test` directory.

**Don't rename or remove the `test` directory, `Mocha` needs this.**

## Check Style

~~~ shell
$ ./jscs.sh *.js
$ ./jscs.sh test/*.js
~~~~

This will run the `JSCS` package to check for compliance with the Google JavaScript Style Guide.
Don't forget to check your files in `test/` as well!

## Run the Program

~~~ shell
$ ./bin/node main.js < purchase_history.csv
~~~

This will use the `main.js` file as the entry point for the program.
It will then feed the data from `purchase_history.csv` to the program over standard input.

<!--  LocalWords:  executables REPL js
 -->
