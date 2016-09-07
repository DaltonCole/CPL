"""Tests for observation module

Feel free to add more tests as you see fit.

"""
import datetime
import pytest

from observation import Observation


def test_lt():
    """Test < operator"""
    o1 = Observation("Scratch", "Starbucks", "2016-01-11 12:00:00")
    o2 = Observation("Grounder", "Starbucks", "2016-01-11 12:30:00")
    assert o1 < o2
    assert not (o2 < o1)


def test_gt():
    """Test > operator"""
    o1 = Observation("Scratch", "Starbucks", "2016-01-11 12:00:00")
    o2 = Observation("Grounder", "Starbucks", "2016-01-11 12:30:00")
    assert not (o1 > o2)
    assert o2 > o1


def test_le():
    """Test <= operator"""
    o1 = Observation("Scratch", "Starbucks", "2016-01-11 12:00:00")
    o2 = Observation("Grounder", "Starbucks", "2016-01-11 12:30:00")
    assert o1 <= o2
    assert o1 <= o1
    assert o2 <= o2
    assert not (o2 <= o1)


def test_ge():
    """Test >= operator"""
    o1 = Observation("Scratch", "Starbucks", "2016-01-11 12:00:00")
    o2 = Observation("Grounder", "Starbucks", "2016-01-11 12:30:00")
    assert not (o1 >= o2)
    assert o1 >= o1
    assert o2 >= o2
    assert o2 >= o1


def test_datetime():
    """Test loading the :class:`datetime.datetime` from a string"""
    # Check the type
    o = Observation("Scratch", "Starbucks", "2016-01-11 12:04:02")
    assert isinstance(o.time, datetime.datetime)

    # Bad time
    with pytest.raises(ValueError):
        Observation("Scratch", "Starbucks", "2016-01-11 12:00:")

    # Bad date
    with pytest.raises(ValueError):
        Observation("Scratch", "Starbucks", "2016-01- 12:00:00")

    # Good date/time
    o = Observation("Scratch", "Starbucks", "2016-01-11 12:04:02")

    # Check that fields are assigned properly
    assert o.time.day == 11
    assert o.time.month == 1
    assert o.time.year == 2016
    assert o.time.hour == 12
    assert o.time.minute == 4
    assert o.time.second == 2
    assert o.time.microsecond == 0


def test_str():
    """Test str construction"""
    o = Observation("Dr. Robotnik", "Starbucks", "2016-01-11 12:04:02")
    assert str(o) == "Dr. Robotnik at Starbucks (2016-01-11 12:04:02)"
