# -*- mode: python -*-
##
#
# A simple Python script to automatically run the XY77 override guide.
#
# **NOTE**: Campus machines have the `pexpect` library installed. You
# should be able to run this script with no issues on those
# boxes. Simply run it the same way you run a regular Python program:
#
#     python3.4 check_expectations.py
#
# The 'child.expect' lines tell `pexpect` to wait for your program to
# output that line. The 'child.sendline' lines tell `pexpect` to send
# that information to the program.
#
# With these two combined, we can simulate typing really quickly! It
# makes it **much** easier that trying to type in input values
# again... and again... and again...
#
# You aren't required to use this file. It's just here to make testing
# a little easier, if you want to give it a try.
#
##
import pexpect
import sys


# Start the XY77 program
child = pexpect.spawnu('python3.4 main.py')

# Keep track of output from the attached program.
child.logfile_read = sys.stdout

##
# Setup
#

# Serial number
child.expect(">> ")             # Wait for a >>
child.sendline("KRXX7e3652")    # When we see a >>, send the serial number

# Check Engine light
child.expect(">> ")
child.sendline("0")

# Maintenance Required light
child.expect(">> ")
child.sendline("1")

# How many switches?
child.expect(">> ")
child.sendline("4")

##
# History Layer
##

# First number
child.expect(">> ")
child.sendline("4")

# Second number
child.expect(">> ")
child.sendline("1")

# Third number
child.expect(">> ")
child.sendline("3")

# Fourth number
child.expect(">> ")
child.sendline("1")

# Fifth number
child.expect(">> ")
child.sendline("2")

##
# Code Layer
##

# Code word
child.expect(">> ")
child.sendline("circuit")

##
# Switches Layer
##

# Switch 1 red
child.expect(">> ")
child.sendline("1")

# Switch 1 blue
child.expect(">> ")
child.sendline("0")

# Switch 1 green
child.expect(">> ")
child.sendline("1")

# Switch 2 red
child.expect(">> ")
child.sendline("0")

# Switch 2 blue
child.expect(">> ")
child.sendline("0")

# Switch 2 green
child.expect(">> ")
child.sendline("1")

# Switch 3 red
child.expect(">> ")
child.sendline("1")

# Switch 3 blue
child.expect(">> ")
child.sendline("1")

# Switch 3 green
child.expect(">> ")
child.sendline("1")

# Switch 4 red
child.expect(">> ")
child.sendline("1")

# Switch 4 blue
child.expect(">> ")
child.sendline("0")

# Switch 4 green
child.expect(">> ")
child.sendline("0")

##
# Button Layer
##

# Shows 44
child.expect(">> ")
child.sendline("44")

# Shows 83
child.expect(">> ")
child.sendline("83")

# Shows 52
child.expect(">> ")
child.sendline("52")

# Wait for the program to end.
child.expect(pexpect.EOF)
