#!/bin/bash

# Variables!
# ----------

# First thing's first: let's define a few variables that we're going
# to need for the rest of the script

# `NODE_DIR` is the name of the directory to use to store the unpacked
# Node.js executables. It starts with a ".", so that it will be
# hidden. That keeps your directory a little less cluttered.
NODE_DIR=.my_nodejs

# `NODE_DOWNLOAD_URL` is the URL from which to download Node.js
NODE_DOWNLOAD_URL=https://nodejs.org/dist/v4.3.1/node-v4.3.1-linux-x64.tar.xz

# `NODE_VERSION` is the version of Node.JS that we're using. If you
# look at the URL for `NODE_DOWNLOAD_URL`, you can see that we can
# obtain the version name by stripping the extension off the
# filename of the downloaded file.
NODE_VERSION=$(basename "$NODE_DOWNLOAD_URL" .tar.xz)

# `NODE_HASH` is the SHA256 hash of the executable. We'll double check
# this as a sanity check to make sure the executable is authentic and
# that the download was successful.
NODE_HASH="1952d92af83b1bd7ffdb4735999f93a91e0d34ba1315ea1210f16f2e411125e4  node-v4.3.1-linux-x64.tar.xz"

# Installing Node.js
# ------------------

# First, check whether the `NODE_DIR` directory exists. If it doesn't,
# we'll go get Node.js and set it up in NODE_DIR. If it does exist,
# we'll just print a message and exit.
if [ ! -d $NODE_DIR ]
then
    # ### If `NODE_DIR` doesn't exist...

    # Then Node.js isn't installed in there!

    # Create and change into the directory where we're keeping nodejs
    mkdir $NODE_DIR
    pushd $NODE_DIR > /dev/null # But be quiet about it.

    # Download Node.js and verify its SHA256 sum for security's sake
    wget $NODE_DOWNLOAD_URL
    echo $NODE_HASH | sha256sum -c -

    # If `sha256sum` detects something fishy, then its exit code will
    # be non-zero. In that case, it's time to exit with great
    # splendor.
    if [ $? -ne 0 ]
    then
        # Show a message explaining the dealio
        echo ""
        echo "GREAT GOOGLY MOOGLY!"
        echo ""
        echo "It looks like something bad happened when we downloaded Node.js!"
        echo "I'm going to stop here and remove what I downloaded."
        echo "This is 2 spooky 4 me."
        echo ""
        echo "It's possible that this was just a network error."
        echo "But I have no way of telling, so I'm outta here."

        # Go back to the directory we were in before (outside of the
        # nodejs dir) and remove the Node.js dir.
        popd > /dev/null
        rm -rf $NODE_DIR

        # Get out of here! Exit with code 1 to indicate that
        # things did NOT work.
        exit 1
    fi

    # Otherwise the download went fine, and the SHA sum was
    # correct. This is the preferred outcome.

    # Unpack the download
    tar xf $NODE_VERSION.tar.xz

    # Get out of the subdir. We're done in here.
    popd > /dev/null

    # Create a link to the bin/ directory, where our executables live
    ln -s $NODE_DIR/$NODE_VERSION/bin bin
else
    # ### If `NODE_DIR` already exists...

    # ... the directory is already there.
    echo "It looks like we've already got a directory named $NODE_DIR."
    echo "If you want to download Node.js again, just delete that "
    echo "directory and run me again."
fi

# Usually bash scripts aren't commented this heavily, but we're
# trying to reduce the amount of magic here.
