"""XY77 Battering Ram

A tool for manipulating the backdoor in the XY77 Series Quad-layer Vault.
"""


def read_int():
    """A helper function for reading an integer from stdin

    :return: The integer that was read
    :rtype: int
    """
    return int(input('>> '))


def read_bool():
    """A helper function for reading a bool from stdin.

    Requires that the user type "1" or "0".

    :return: The bool that was read
    :rtype: int
    """
    val = input('>> ')
    while val not in ('1', '0'):
        print("Answer Yes (1) or No (0)")
        val = input('>> ')
    return bool(int(val))


def press_button(display):
    """Returns True if the display value indicates that the button should
    be pressed.

    :param int display: The current value on the Button Layer display

    :return: True if the button should be pressed
    :rtype: bool
    """
    # If display value is evently divisable by 13,
    # then the button should not be depressed
    if display % 13 == 0:
        return False
    else:
        return True


def button_layer(vault_state):
    """Interact with the user to override the Button Layer

    :param vault_state: The current state of the vault

    :return: None
    """
    # Loop until the display value is evenly divisable by 13
    # The suspicion level should increase by 1 every time the button is pressed
    while(True):
        print('What number is displayed?')
        display = read_int()

        if press_button(display):
            vault_state['suspicion level'] += 1
            print('Press the button!')
        else:
            break

    print('Leave the button alone now.')
    print('Button layer is complete.')

    return


def which_to_press(history, displayed):
    """Returns the integer value of the button to press in response to the
    button press history and currently displayed value.

    :param list history: A list of pairs (tuples) that represents the
        history of values displayed and buttons pressed. Each tuple
        looks like: (value_displayed, button_pressed)

    :param int displayed: The value that is currently displayed.

    :return: The label of the button to press.
    :rtype: int
    """
    # If displayed is 1, then the fourth button should be pressed
    if displayed == 1:
        history.append((1, 4))
        return 4
    # If displayed is 2, then the button pressed
    # in the first round should be pressed
    elif displayed == 2:
        first_display, first_button = history[0]
        history.append((2, first_button))
        return first_button
    # If displayed is 3, then the the button with the same value as
    # the display in the previous round should be pressed
    elif displayed == 3:
        previous_display, previous_button = history[-1]
        history.append((3, previous_display))
        return previous_display
    # If displayed is 4, then the second button should be pressed
    elif displayed == 4:
        history.append((4, 2))
        return 2


def history_layer(vault_state):
    """Interact with the user to override the History Layer

    :param vault_state: The current state of the vault.

    :return: None
    """
    # Create an empty history to be passed into the which_to_press function
    history = []

    for i in range(5):
        print('What number is displayed right now?')
        displayed = read_int()

        press = which_to_press(history, displayed)

        print('Press the button labeled', press)

        # Increase the suspicion level by 1 each time
        # an even numbere labled button is pressed
        if press % 2 == 0:
            vault_state['suspicion level'] += 1

    print('History layer complete.')
    return


def dial_to(vault_state, code):
    """Determines which letter to dial to, based on the vault's serial
    number and code word.

    :param vault_state: The current state of the vault.
    :param str code: The code word that is displayed in the Code Layer

    :return: The letter to turn the dial to
    :rtype: str
    """
    # First index is the fourth to last character of code
    first_index = int((vault_state['serial number'])[-4])
    # The last index is the second to last character of code
    last_index = int((vault_state['serial number'])[-2])

    # The substring is the string from the first to last index of code
    sub_string = code[first_index:(last_index+1)]

    # The desired character to return is the
    # lowest valued char in the substring
    # return sorted(sub_string[0])
    return (sorted(sub_string))[0]


def code_layer(vault_state):
    """Interact with the user to override the Code Layer

    :param vault_state: The current state of the vault.

    :return: None
    """
    # Get user code input
    print('What is the displayed code?')
    code = input('>> ')

    # Find the desired letter to turn the dial to
    letter = dial_to(vault_state, code)

    print('Turn the dial to', letter)
    print('Code layer complete.')
    return


def should_flip(vault_state, has_red, has_blue, has_green):
    """Determine whether a single switch should be flipped (toggled).

    :param vault_state: The current state of the vault.
    :param bool has_red: True if the red light is on for this switch,
        otherwise False.
    :param bool has_blue: True if the blue light is on for this switch,
        otherwise False.
    :param bool has_green: True if the green light is on for this switch,
        otherwise False.

    :return: True if the user should flip (toggle) this switch, otherwise False
    :rtype: bool
    """
    # Returns False if all three colors are off.
    # This if is not needed but included for clairity
    if not has_red and not has_blue and not has_green:
        return False
    # Returns True if only the Blue light is on
    # and the check engine light is also on
    elif (not has_red and has_blue and not has_green and
          vault_state['indicators']['check engine']):
        return True
    # Returns False if only the Red light is on.
    # This is not needed but included for clairity
    elif has_red and not has_blue and not has_green:
        return False
    # Returns True if only the Green light is on
    # and the maintenance required light is also on
    elif (not has_red and not has_blue and has_green and
          vault_state['indicators']['maintenance required']):
        return True
    # Returns True if only the Red and Blue lights are on
    # and the serial number contains 'K'
    elif (has_red and has_blue and not has_green and
          'K' in vault_state['serial number']):
        return True
    # Returns True if only the Blue and Green lights are on
    # and the serial number contains 'R'
    elif (not has_red and has_blue and has_green and
          'R' in vault_state['serial number']):
        return True
    # Returns True if only the Red and Green lights are on
    # and the serial number contains 'B'
    elif (has_red and not has_blue and has_green and
          'B' in vault_state['serial number']):
        return True
    # Returns True if all three lights are on.
    # This is not needed but included for clairity
    elif has_red and has_blue and has_green:
        return False
    # Otherwise the flip should not be flipped
    else:
        return False


def switches_layer(vault_state):
    """Interact with the user to override the Switches Layer

    :param vault_state: The current state of the vault.

    :return: None
    """
    # Repeat switch test for the number of switches on valut
    for i in range(vault_state['switch count']):
        print('Does switch', i, 'have a red light?')
        has_red = read_bool()
        print('Does switch', i, 'have a blue light?')
        has_blue = read_bool()
        print('Does switch', i, 'have a green light?')
        has_green = read_bool()

        if should_flip(vault_state, has_red, has_blue, has_green):
            print('Flip that switch\n')
            # Increase suspicion level by 2 each time flip is switched
            vault_state['suspicion level'] += 2
        else:
            print('DO NOT flip that switch\n')

    print('Switches layer is complete.')
    return


def get_vault_state():
    """Interact with the user to create an initial vault state.

    The vault state has several keys:

    * "suspicion level": The vault's current suspicion level (starts at 0).
    * "serial number": The vault's serial number (requires user input).
    * "switch count": The number of switches in the Switches Layer
        (requires user input)
    * "indicators": A dictionary with the following keys:
        * "check engine": True if the vault's Check Engine light is on
            (requires user input)
        * "maintenance required": True if the vault's Maintenance Required
            light is on (requires user input)

    :return: The initial vault state
    :rtype: dict
    """
    state = {
        'suspicion level': 0,
        'indicators': {},
    }

    print("What is the vault's serial number?")
    state['serial number'] = input('>> ')

    print('Is the "check engine" light on?')
    state['indicators']['check engine'] = read_bool()

    print('Is the "maintenance required" light on?')
    state['indicators']['maintenance required'] = read_bool()

    print('How many switches are on the vault?')
    state['switch count'] = read_int()
    return state


def main():
    """Program entry point.

    Greets the user and begins interactive layer override
    guide. Prior to exit, the program warns the user to wait a certain
    amount of time before opening the vault.

    :return: None

    """
    print("Welcome to the XY77 Battering Ram")

    state = get_vault_state()
    print("State acquired. Let's start.")

    print("\n**History Layer**")
    history_layer(state)

    print("\n**Code Layer**")
    code_layer(state)

    print("\n**Switches Layer**")
    switches_layer(state)

    print("\n**Button Layer**")
    button_layer(state)

    print("Layers bypassed.")
    print("Wait", state['suspicion level'],
          "seconds or more to allow suspicion level to dissipate.")


if __name__ == '__main__':
    #  Start it
    main()
