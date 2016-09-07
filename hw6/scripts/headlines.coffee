# Description:
#   Fetches headlines from a remote site
#
# Dependencies:
#   "request": "2.69.0"
#
# Configuration:
#   HEADLINE_URL: The URL to use for fetching newline-delimited
#       headlines. Defaults to http://cpl.mwisely.xyz/hw/6/headlines.txt
#
# Commands:
#   hubot show me a headline - Go fetch a random headline
#
# Notes:
#   This script pulls headlines from HEADLINE_URL. That means that
#   this script will need access to the Internet.
#
'use strict'

request = require('request')

HEADLINE_URL = process.env.HEADLINE_URL
HEADLINE_URL ?= 'http://cpl.mwisely.xyz/hw/6/headlines.txt'

module.exports = (robot) ->

  # Handler for "hubot show me a headline"
  robot.respond /show me a headline$/i, (msg) ->

    ###

    Use the `request` library (which is already installed by NPM) to
    send a request to HEADLINE_URL. When the request is complete, the
    provided callback will receive three parameters: `error`,
    `response`, and `body`.

    If an error **exists** (hint, hint) or if the response's status
    code is not 200 (`HTTP OK`), then the hubot should reply with:

    > I couldn't get any headlines...

    Otherwise, the request must have succeeded. In that case, the
    hubot should reply with a random headline from the
    newline-delimited response body. Note that the headline should
    never be blank, since the headline website will always have at
    least one headline to choose.

    ###

    # Tell user we are getting a random headline
    msg.reply "Okey doke. I'll go fetch a headline!"

    # Reguest a headline from the specified URL
    request.get {uri:HEADLINE_URL, json : true}, (err, r, body) ->
      # If error occured, tell user
      if err?
        console.log "I couldn't get any headlines..."
      else
        # Otherwise, print a random header
        lines = body.split('\n')
        msg.reply lines[Math.floor(Math.random()*lines.length)]









