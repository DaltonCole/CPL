'use strict'

Helper = require('hubot-test-helper')
expect = require('chai').expect

helper = new Helper('../scripts/hello.coffee')

describe 'hello script', ->
  beforeEach ->
    @room = helper.createRoom()

  afterEach ->
    @room.destroy()

  it 'says hi in response to "hubot hi"', ->
    @room.user.say('alice', 'hubot hi').then =>
      expect(@room.messages).to.eql [
        ['alice', 'hubot hi']
        ['hubot', '@alice hey there']
      ]

  it 'says hi in response to "Hubot hi"', ->
    @room.user.say('alice', 'Hubot hi').then =>
      expect(@room.messages).to.eql [
        ['alice', 'Hubot hi']
        ['hubot', '@alice hey there']
      ]

  it 'says hi in response to "hi hubot"', ->
    @room.user.say('alice', 'hi hubot').then =>
      expect(@room.messages).to.eql [
        ['alice', 'hi hubot']
        ['hubot', '@alice hey there']
      ]

  it 'says hi in response to "hi Hubot"', ->
    @room.user.say('alice', 'hi Hubot').then =>
      expect(@room.messages).to.eql [
        ['alice', 'hi Hubot']
        ['hubot', '@alice hey there']
      ]
