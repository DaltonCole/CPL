# Import all of our testable functions from main.
from main import press_button, which_to_press, dial_to, should_flip


def test_press_button():
    """Test that we'll know when to press the Button Layer button

    Tests press_button function.
    """
    # Create a list of 135 elements to test
    test_cases = []

    for i in range(135):
        test_cases.append(i)

    # If number is divisible by 13, return False, True otherwise
    for i in test_cases:
        if i % 13 == 0:
            assert not press_button(i)
        else:
            assert press_button(i)


def test_which_to_press():
    """Test that we'll know how to respond to the History Layer

    Tests which_to_press function.
    """
    history = []

    for display, expected in [(4, 2), (1, 4), (3, 1), (1, 4), (2, 2)]:
        actual = which_to_press(history, display)
        assert actual == expected
        history.append((display, expected))


def test_dial_to():
    """Test that we'll know how to respond to the Code Layer

    Tests dial_to function.
    """
    vault_state = {
        'serial number': 'XX7e3652',
        'suspicion level': 0,
        'indicators': {
            'maintenance required': False,
            'check engine': True
        },
        'switch count': 6
    }

    assert dial_to(vault_state, 'elephant') == 'a'
    assert dial_to(vault_state, 'daltoncole') == 'n'
    assert dial_to(vault_state, 'thisisatest') == 'i'
    assert dial_to(vault_state, 'moretests') == 'e'
    assert dial_to(vault_state, 'ilikepi') == 'e'
    assert dial_to(vault_state, 'thatwasalie') == 'a'
    assert dial_to(vault_state, 'idontlikepi') == 'l'
    assert dial_to(vault_state, 'circuit') == 'c'


def test_should_flip():
    """Test that we'll know how to respond to the Switches Layer

    Tests should_flip function.
    """
    vault_state = {
        'serial number': 'FFGXRK89999',
        'suspicion level': 0,
        'indicators': {
            'check engine': True,
            'maintenance required': False
        },
        'switch count': 6
    }

    assert not should_flip(vault_state, 0, 0, 0)
    assert should_flip(vault_state, 0, 1, 0)
    assert not should_flip(vault_state, 1, 0, 0)
    assert not should_flip(vault_state, 0, 0, 1)
    assert should_flip(vault_state, 1, 1, 0)
    assert should_flip(vault_state, 0, 1, 1)
    assert not should_flip(vault_state, 1, 0, 1)
    assert not should_flip(vault_state, 1, 1, 1)
