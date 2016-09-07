from datetime import timedelta


class DataError(Exception):
    """DataError is for a semantic error
    """
    pass


class ObservationTimeline:
    def __init__(self):
        """Constructor for an ObservationTimeline

        initializes an observations list to empty

        :return: None
        """
        self.observations = []

    def add(self, observation):
        """Adds an Observation to the observations list

        :param Observation observation: A single observation

        :return: None
        """
        index = 0
        for x in self.observations:
            # Puts observations in order
            if observation.time < x.time:
                self.observations.insert(index, observation)
                break
            index += 1
        else:
            # Puts observation in the back
            self.observations.append(observation)

    def windows(self, window_size=timedelta(0, 3600)):
        """Yields all observations that happen within
        a specified timeframe from the first observation

        :param timedelta window_size: timeframe

        :yield: A tuple of the observations in timeframe
        from first observation

        :rtype: tuple
        """
        for i in range(len(self.observations)):
            # Add initial observation to tuple
            window = (self.observations[i],)
            # If observation is within timeframe, add it to the tuple
            for j in range(i+1, len(self.observations)):
                if (self.observations[j].time -
                   self.observations[i].time < window_size):
                    window += (self.observations[j],)
            yield window

    def rendezvous(self, window_size=timedelta(0, 3600)):
        """Sees if two agents rendeviwed or not

        :param timedelta window_size: timeframe of observations

        :returns: A tuple with the following items:

                - First observation

                - Second observation

        :rtype: tuple

        :raises ValueError: If there is an issue unpacking the values of a
            row into name, location, time, and item. Note that this is
            thrown when unpacking too few or two many values into a tuple
            of variables.

        :raises DataError: If too many observations happen in timeframe

        """
        for window in self.windows():
            # create tuples without the starting tuple in window
            win = iter(window)
            next(win)
            rend = (window[0],)
            # See if the agents were in the same location at the same time
            for w in win:
                if window[0].location == w.location:
                    rend += (w,)
            # If 3 agents are at the same place at the same time, raise Error
            if len(rend) > 2:
                raise DataError("Can only have one rendezvous in a window")
            # If no two agents were in the same place, skip this iteration
            elif len(rend) == 1:
                continue
            # Returns a tuple of two items of the two observations
            else:
                yield rend
