"""Tests for main module
"""
from observation_timeline import ObservationTimeline
from observation import Observation
from main import load_timeline


def test_load_timeline():
    """Tests the return values of load_timeline
    """
    # Call load_timeline
    time_tuple = load_timeline('test.csv')

    # Create as dictionary as to what time_tuple[0] should be
    diction = {"Bob": "shoes", "Jane": "Mits", "Dalton": "One Billion Dollars"}

    # Create a ObservationTimeline as to what time_tuple[1] should be
    timeline = ObservationTimeline()
    timeline.add(Observation("Bob", "Starbucks", "1970-01-02 02:53:00"))
    timeline.add(Observation("Jane", "Starbucks", "1970-01-02 03:53:00"))
    timeline.add(Observation("Dalton", "Starbucks", "1970-01-02 04:53:00"))
    timeline.add(Observation("Aaron", "My house", "1970-01-02 05:53:00"))
    timeline.add(Observation("Mike", "His House", "1970-01-02 06:53:00"))

    # Check to see if the two are equal
    assert diction == time_tuple[0]
    for x in range(len(timeline.observations)):
        assert (timeline.observations[x].name ==
                time_tuple[1].observations[x].name)
        assert (timeline.observations[x].location ==
                time_tuple[1].observations[x].location)
        assert (timeline.observations[x].time ==
                time_tuple[1].observations[x].time)
