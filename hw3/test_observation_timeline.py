"""Tests for observation_timeline module

Feel free to add more tests as you see fit.

"""
import random

from datetime import datetime, timedelta

from observation import Observation
from observation_timeline import ObservationTimeline


def random_timed_observations(count=100):
    """A helper function that returns Observations with random times

    Note that the names and locations will all be the same.

    :param int count: The number of Observations to return

    :return: a list of Observation instances in a random order.
    """
    # Generate a list of random, unique Observations
    observations = []
    time = datetime.fromtimestamp(0)
    for _ in range(count):
        time += timedelta(minutes=random.randint(1, 59))
        observations.append(Observation("Skeletor", "Starbucks", str(time)))

    # Shuffle up the Observations
    random.shuffle(observations)

    return observations


def random_timed_observation_timeline(count=100):
    """A helper function that returns an ObservationTimeline that contains
    Observations with random times.

    Note that the names and locations will all be the same.

    :param int count: The number of Observations in the ObservationTimeline

    :return: An ObservationTimeline with ``count`` Observations with
        random times.

    """
    # Generate some observations
    observations = random_timed_observations(count)

    # Add the observations to our timeline
    timeline = ObservationTimeline()
    for t in observations:
        timeline.add(t)

    return timeline


def test_add():
    """Test that adding more Observations keeps them in order."""
    # Generate observations with random times
    timeline = random_timed_observation_timeline()

    # Check that our observations are in order
    # (Go look up zip())
    for prev, current in zip(timeline.observations, timeline.observations[1:]):
        assert prev.time < current.time


def test_window():
    """Test that our window generator respects window_size."""
    # Generate observations with random times
    timeline = random_timed_observation_timeline()

    # Defaults to one hour
    for window in timeline.windows():
        # Gotta be a tuple, though we don't know the length
        assert isinstance(window, tuple)
        assert len(window) > 0

        # Check the types
        for o in window:
            assert isinstance(o, Observation)

        # Double check that Observations in the window are sorted (for fun)
        for o1, o2 in zip(window, window[1:]):
            assert o1 < o2

        # Make sure each member is within an hour of the first.
        # We know they're sorted, so just check first and last.
        assert (window[0].time + timedelta(hours=1)) > window[-1].time


def test_rendezvous():
    """Test our rendezvous generator"""
    timeline = ObservationTimeline()
    'timeline.add(Observation("Skeletor", "Starbucks", "1970-01-02 02:53:00"))'
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 03:52:00"))

    for i, suspect_pair in enumerate(timeline.rendezvous()):
        # Gotta be a tuple of length 2
        assert isinstance(suspect_pair, tuple)
        assert len(suspect_pair) == 2

        # Unpack 'em
        s1, s2 = suspect_pair

        # Check the types
        assert isinstance(s1, Observation)
        assert isinstance(s2, Observation)

        # Check that we've got our suspects
        assert "Skeletor" in (s1.name, s2.name)
        assert "Doc Oc" in (s1.name, s2.name)

    # We only looped one time, so 'i' was set to zero, and that's it.
    assert i == 0


def test_my_add():
    """Test that adding more Observations keeps them in order."""
    # Generate observations with random times
    timeline = ObservationTimeline()
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 03:49:00"))
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 02:51:00"))
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 03:52:00"))
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 04:52:00"))
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 05:52:00"))
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 03:50:00"))

    # Check that our observations are in order
    # (Go look up zip())
    for prev, current in zip(timeline.observations, timeline.observations[1:]):
        assert prev.time < current.time


def test_my_rendezvous():
    """Test our rendezvous generator"""
    timeline = ObservationTimeline()
    timeline.add(Observation("Skeletor", "Starbucks", "1970-01-02 02:53:00"))
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 03:05:00"))
    timeline.add(Observation("Ham", "Starbucks", "1970-01-02 03:55:00"))

    for i, suspect_pair in enumerate(timeline.rendezvous()):
        # Gotta be a tuple of length 2
        print("boo")
        assert isinstance(suspect_pair, tuple)
        assert len(suspect_pair) == 2

        # Unpack 'em
        s1, s2 = suspect_pair

        # Check the types
        assert isinstance(s1, Observation)
        assert isinstance(s2, Observation)

    # We only looped one time, so 'i' was set to zero, and that's it.
    assert i == 1


def test_my_rendezvous_more():
    """Test our rendezvous generator"""
    timeline = ObservationTimeline()
    timeline.add(Observation("Skeletor", "Starbucks", "1970-01-02 02:53:00"))
    timeline.add(Observation("Doc Oc", "Starbucks", "1970-01-02 03:05:00"))
    timeline.add(Observation("D", "Starbucks", "1970-01-02 03:55:00"))
    timeline.add(Observation("E", "Starbucks", "1970-01-02 04:50:00"))
    timeline.add(Observation("F", "Starbucks", "1970-01-02 05:40:00"))
    timeline.add(Observation("G", "Starbucks", "1970-01-02 06:30:00"))

    for i, suspect_pair in enumerate(timeline.rendezvous()):
        # Gotta be a tuple of length 2
        print("boo")
        assert isinstance(suspect_pair, tuple)
        assert len(suspect_pair) == 2

        # Unpack 'em
        s1, s2 = suspect_pair

        # Check the types
        assert isinstance(s1, Observation)
        assert isinstance(s2, Observation)

    # We only looped one time, so 'i' was set to zero, and that's it.
    assert i == 4


def test_window_enumeration():
    """Test that our window generator respects window_size."""
    # Generate observations with random times
    timeline = random_timed_observation_timeline()

    # Defaults to one hour
    for i, window in enumerate(timeline.windows()):
        # Gotta be a tuple, though we don't know the length
        assert isinstance(window, tuple)
        assert len(window) > 0
        for x in window:
                print(x)
        print("")
        # Check the types
        for o in window:
            assert isinstance(o, Observation)

        # Double check that Observations in the window are sorted (for fun)
        for o1, o2 in zip(window, window[1:]):
            assert o1 < o2

        # Make sure each member is within an hour of the first.
        # We know they're sorted, so just check first and last.
        assert (window[0].time + timedelta(hours=1)) > window[-1].time
    assert i == len(timeline.observations) - 1
