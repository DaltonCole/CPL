from datetime import datetime


class Observation:
    def __init__(self, name, location, time):
        """Constructor for an observation

        Raises a ValueError if time is in the
        incorrect format

        :param str name: name of the agent

        :param str location: location of target

        :param str time: arival time at location

        :return: None
        """
        self.name = name
        self.location = location
        self.timeString = time
        # Change inputed time to timedate format
        self.time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

    def __lt__(self, other):
        """Less than. Determins if self arrival time was sooner
        than other's arrival time

        :param Observation other: Who we are comparing this to

        :return: Bool, True if self arrived eariler, False otherise

        :rtype: Bool
        """
        if self.time < other.time:
            return True
        else:
            return False

    def __gt__(self, other):
        """Greater than. Determins if self arrival time was
        later than other's arrival time

        :param Observation other: Who we are comparing this to

        :return: Bool, True if self arrived later, False otherise

        :rtype: Bool
        """
        if self.time > other.time:
            return True
        else:
            return False

    def __le__(self, other):
        """Less than or equal to. Determins if self arrival
        time was sooner or equal to other's arrival time

        :param Observation other: Who we are comparing this to

        :return: Bool, True if self arrived eariler or same time
        as other, False otherise

        :rtype: Bool
        """
        if self.time <= other.time:
            return True
        else:
            return False

    def __ge__(self, other):
        """Greater than or equal to. Determins if self arrival
        time was later or equal to other's arrival time

        :param Observation other: Who we are comparing this to

        :return: Bool, True if self arrived later or same time
        as other, False otherise

        :rtype: Bool
        """
        if self.time >= other.time:
            return True
        else:
            return False

    def __str__(self):
        """How to output and Observation object

        :return: a formated string for an Observation

        :rtype: str
        """
        return str(self.name + " at " + self.location + " (" +
                   self.timeString + ")")
