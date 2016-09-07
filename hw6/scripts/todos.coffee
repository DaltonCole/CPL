# Description:
#   Keeps track of todo items
#
# Dependencies:
#   "node-uuid": "1.4.7"
#
# Commands:
#   hubot show my todo list - Lists todo items in no particular order
#   hubot add <item> to my todo list - Adds <item> to the list of todo items
#   hubot <itemID> is done - Removes the item with <itemID> from the todo list
#
# Notes:
#  This script stores todo items as individual text files within a
#  directory named "todos". Each file will be named uniquely with a
#  random UUID (uuid.v4) and no file extension. Because each is a
#  separate file with a random name, the order of the listed todo
#  items may vary.
#
'use strict'

fs = require('fs')
path = require('path')
uuid = require('node-uuid')

# The name of the directory where we're storing our todo files
DATA_DIR = 'todos'

module.exports = (robot) ->

  # Check to see if our chosen DATA_DIR exists. If it doesn't, we'll
  # make it.
  try
    fs.statSync DATA_DIR
  catch err
    fs.mkdirSync DATA_DIR

  # Handler for "hubot show my todo list"
  robot.respond /show my todo list$/i, (msg) ->

    ###

    Uses `fs.readdir` to list the names of the files in the `DATA_DIR`
    directory.

    If the `fs.readdir` callback receives an error (if the error
    exists), then the hubot will reply with the following and exit:

    > Oh no... I couldn't look for todos...

    Otherwise, if the list of todo files is empty, the hubot will
    reply with:

    > The list is empty!

    Otherwise, we loop over the file names, using `fs.readFile` to
    read the contents of each file. We will need to insert a closure
    wrapper in order to ensure that loop variables are closed over.

    Whenever a file is read, its corresponding callback will be
    executed. Each `fs.readFile` callback takes two parameters:
    `error` and `data`.

    If `error` exists, then the hubot will reply with:

    > Uh oh! Had trouble opening a todo...

    Otherwise, the hubot will reply with the ID of the todo item (its
    file name) and the content of the todo file:

    > <itemID>: <item>

    In summary, for each file in the `DATA_DIR` directory, we call
    `fs.readFile` and register a callback, so that when the content of
    a todo file is ready, we can reply to the user.

    We don't necessarily know the order of the files in the directory,
    nor do we know how long it will take to read each file, so the
    hubot may reply with todo items in a totally arbitrary order.

    ###

    # Get ready to read from directory
    fs.readdir DATA_DIR, (err, files) ->
      # If we failed at reading, tell user
      if err?
        msg.reply "Oh no... I couldn't look for todos..."
      else if files.length is 0
        # If no files in directory, tell user
        msg.reply "The list is empty!"
      else
        # For each file in the directory, print file name and its contents
        for file in files
          fs.readFile "#{DATA_DIR}/#{file}", (error, data) ->
            if err?
              # If error occured in reading the file, tell user
              msg.reply "Uh oh! Had trouble opening a todo..."
            else
              msg.reply "#{file}: #{data}"


  # Handler for "hubot add <item> to my todo list"
  robot.respond /add (.*) to my todo list$/i, (msg) ->
    todo = msg.match[1]

    ###

    Uses `fs.writeFile` to save the todo item (with ASCII encoding) to
    a file with a name computed with `uuid.v4`.

    When Node is done writing the data to the specified file, it calls
    our callback. If there's an error, the hubot replies with:

    > Oh no... I couldn't write the todo file...

    Otherwise, the hubot replies with:

    > OK! I added <todo> to the todo list

    Note that file names have no extensions. They are just UUIDs.

    ###

    # Create a random uuid
    uuidv4 = uuid.v4()

    # Create file with the UUID that contains the todo
    fs.writeFile "#{DATA_DIR}/#{uuidv4}", todo, (error) ->
      if error?
        # If error occured, tell user
        msg.reply "Oh no... I couldn't write the todo file..."
      else
        msg.reply "OK! I added #{todo} to the todo list"


  # Handler for "hubot <itemID> is done"
  robot.respond /([0-9a-f\-]{36}) is done$/i, (msg) ->
    id = msg.match[1]

    ###

    Uses `fs.unlink` to delete the todo file from `DATA_DIR` with name
    `id`. If there is an error deleting the file, the hubot replies
    with:

    > Couldn't find <id>

    Otherwise, it replies with

    > OK! Removed <id>

    ###

    # Delete todo
    fs.unlink "#{DATA_DIR}/#{id}", (err) ->
      if err?
        # If error occured, tell user
        msg.reply "Couldn't find #{id}"
      else
        msg.reply "OK! Removed #{id}"

