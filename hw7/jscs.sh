#!/bin/bash

# Determine the directory where this bash script lives
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check that node is actually installed SOMEWHERE.  We don't really
# care what version of Node.js we're using, as long as it lets us
# install and run the right version of JSCS.
which node > /dev/null
if [ "$?" != "0" ]
then
    echo ""
    echo "Looks like Node.js isn't installed anywhere!"
    echo ""
    echo "Either run this script on a campus Linux box, or install Node.js yourself."
    echo ""

    exit 1
fi

# Check if jscs is already installed...
if [ ! -e $DIR/node_modules/.bin/jscs ]
then

    echo ""
    echo "I don't see JSCS anywhere. I'm going to go get it."
    echo ""
    echo "/me runs to the store"
    echo ""

    sleep 1

    npm install -d jscs@2.11.0 jscs-jsdoc@1.3.2
fi

# npm installs the jscs executable within node_modules/.bin, so let's
# add it to our PATH. That way we can run it like....
PATH=$DIR/node_modules/.bin:$PATH

# ... this. Then, we pass all command line arguments received by this
# script to jscs.
jscs "$@"
