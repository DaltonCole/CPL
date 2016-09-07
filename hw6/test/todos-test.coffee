'use strict'

fs = require('fs')
Helper = require('hubot-test-helper')
path = require('path')
rm = require('rimraf').sync
should = require('chai').should()
tmp = require('tmp')

# Delay execution of a function
#
# With the 'todo' script, our hubot might require a little time to
# perform asynchronous file I/O. This function helps us wait a little
# bit for the hubot to respond before we make any test assertions.
#
# @param [Function] The function to call when time is up
#
delay = (callback) ->
  setTimeout callback, 250

describe 'todo script', ->

  # Configure Mocha to use longer timeout periods... since we have to
  # wait for the Hubot to respond to messages.
  @slow 1000
  @timeout 2000

  beforeEach ->
    # Create and `cd` to a temporary directory for testing's sake.
    @dataDir = tmp.dirSync().name
    process.chdir @dataDir

    @helper = new Helper('../scripts/todos.coffee')
    @room = @helper.createRoom()

  afterEach ->
    do @room.destroy
    rm @dataDir, disableGlob: false

  it 'creates a "todos" directory for todo items', (done) ->
    fs.stat 'todos', (err, stat) ->
      should.not.exist err
      stat.isDirectory().should.be.true
      do done

  it 'shows a message when the data file is empty', (done) ->
    @room.user.say('carmen', 'hubot show my todo list').then =>
      delay =>
        @room.messages.should.deep.equal [
          ['carmen', 'hubot show my todo list']
          ['hubot', '@carmen The list is empty!']
        ]
        do done

  it 'shows a message when the data file isn\'t there', (done) ->
    fs.rmdirSync path.join @dataDir, "todos"
    fs.rmdirSync path.join @dataDir
    @room.user.say('carmen', 'hubot show my todo list').then =>
      delay =>
        @room.messages.should.deep.equal [
          ['carmen', 'hubot show my todo list']
          ['hubot', '@carmen Oh no... I couldn\'t look for todos...']
        ]
        do done

  it 'lets us add an item', (done) ->
    @room.user.say('carmen', 'hubot add potato to my todo list').then =>
      delay =>
        @room.messages.should.deep.equal [
          ['carmen', 'hubot add potato to my todo list']
          ['hubot', '@carmen OK! I added potato to the todo list']
        ]
        do done

  it 'lets us add a couple of items', (done) ->
    @room.user.say('carmen', 'hubot add frog to my todo list').then =>
      delay =>
        @room.user.say('carmen', 'hubot add submarine to my todo list').then =>
          delay =>
            @room.messages.should.deep.equal [
              ['carmen', 'hubot add frog to my todo list']
              ['hubot', '@carmen OK! I added frog to the todo list']
              ['carmen', 'hubot add submarine to my todo list']
              ['hubot', '@carmen OK! I added submarine to the todo list']
            ]

            # Note that for this test, all the file-related code is
            # syncronous. Your scripts should be *asynchronous*.
            todoDir = path.join @dataDir, "todos"
            files = fs.readdirSync todoDir

            # Read data from the listed files
            data = for f in files
              fs.readFileSync path.join(todoDir, f), 'ascii'

            data.should.have.members ['frog', 'submarine']

            # Make sure that we see our items when we ask for the
            # whole todo list
            @room.user.say('carmen', 'hubot show my todo list').then =>
              delay =>
                @room.messages[4].should.deep.equal [
                  'carmen', 'hubot show my todo list'
                ]

                # We start at message 5, since the first 4 were
                # already checked earlier in this test.
                todos = []
                for [name, msg] in @room.messages[5..]
                  name.should.equal "hubot"
                  msg.should.match /@carmen [0-9a-f\-]{36}: .*/i

                  match = (/@carmen [0-9a-f\-]{36}: (.*)/i).exec msg
                  todos.push match[1]

                todos.should.have.members ['frog', 'submarine']

                do done

  it 'lets us remove items', (done) ->
    @room.user.say('carmen', 'hubot add frog to my todo list').then =>
      @room.user.say('carmen', 'hubot add submarine to my todo list').then =>
        delay =>
          # Check the files on disk, as a sanity check
          todoDir = path.join @dataDir, "todos"
          files = fs.readdirSync todoDir
          files.length.should.equal 2
          [f1, f2] = files

          # Try to delete a todo, then make sure the correct file has
          # has been deleted
          @room.user.say('carmen', "hubot #{f1} is done").then =>
            delay =>
              @room.messages[4..].should.deep.equal [
                ['carmen', "hubot #{f1} is done"]
                ['hubot', "@carmen OK! Removed #{f1}"]
              ]
              [f3] = fs.readdirSync todoDir
              f2.should.equal f3

              files = fs.readdirSync todoDir
              files.length.should.equal 1

              do done
