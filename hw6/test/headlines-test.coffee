'use strict'

Helper = require('hubot-test-helper')
should = require('chai').should()

# Delay execution of a function
#
# With the 'headline' script, our hubot might require a little time to
# perform asynchronous web requests. This function helps us wait a
# little bit for the hubot to respond before we make any test
# assertions.
#
# @param [Function] The function to call when time is up
#
delay = (callback) ->
  setTimeout callback, 1000

describe 'headline script', ->

  # Configure Mocha to use longer timeout periods... since we have to
  # wait for the Hubot to respond to messages.
  @slow 2000
  @timeout 40000

  beforeEach ->
    @helper = new Helper('../scripts/headlines.coffee')
    @room = @helper.createRoom()

  afterEach ->
    do @room.destroy

  it 'gets a headline', (done) ->
    @room.user.say('carmen', 'hubot show me a headline').then =>
      delay =>
        # Three messages in total, the first two are the request and
        # acknowledgement.
        @room.messages.length.should.equal 3
        @room.messages[0..1].should.deep.equal [
          ['carmen', 'hubot show me a headline']
          ['hubot', '@carmen Okey doke. I\'ll go fetch a headline!']
        ]

        # The headline shouldn't be blank.
        @room.messages[2].should.not.deep.equal ['hubot', '@carmen ']

        do done

  it 'doesn\'t return a blank headline', (done) ->
    # Ask for 20 headlines
    promises = for i in [1..20]
      @room.user.say('carmen', 'hubot show me a headline')

    # Once all 20 headlines have been requested...
    Promise.all(promises).then =>
      delay =>
        # Check that we've got the right number of responses
        # (request, acknowledgement, headline) * 20 == 60
        @room.messages.length.should.equal 60

        # Make sure none of them are blank!
        for msg in @room.messages
          [name, content] = msg
          content.trim().should.not.equal '@carmen'

        do done
