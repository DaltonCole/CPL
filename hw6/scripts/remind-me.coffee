# Description:
#   Reminds you to do something after a specified waiting time
#
# Commands:
#   hubot remind me to <task> in <sec> seconds - Send a reminder in <sec> secs
#
# Notes:
#   If the hubot is shut down, all reminders are cleared.
#
'use strict'

module.exports = (robot) ->

  # Handler for "hubot remind me to <task> in <sec> seconds"
  robot.respond /remind me to (.+) in (\d+) seconds?$/i, (msg) ->
    [taskName, numSeconds] = msg.match[1..2]

    ###

    As soon as the command is issued, the hubot will reply with:

    > OK. I'll remind you to <taskName> in <numSeconds> seconds.

    A timeout is then set, so that the hubot will reply with the
    following after `numSeconds` seconds:

    > Don't forget to <taskName>!

    ###

    # Function that reminds the user to complete a task when ran
    run = () ->
      msg.reply "Don't forget to #{taskName}!"

    # Tell user that we recieved the reminder
    msg.reply "OK. I'll remind you to #{taskName} in #{numSeconds} seconds."

    # Remind user
    setTimeout(run, numSeconds*1000)
