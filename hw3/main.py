import argparse
import csv
import pprint
from observation_timeline import ObservationTimeline
from observation import Observation


def load_timeline(filename):
    """Loads an observations CSV file.

    :param str filename: The name of the observations CSV file to read

    :returns: A tuple with the following items:

                - A dictionary that maps a suspect's name to the
                  item they are currently carrying (based on data in
                  the CSV file).

                - An ObservationTimeline that contains the observation
                  data loaded from the CSV file.

    :rtype: tuple

    :raises ValueError: If there is an issue unpacking the values of a
        row into name, location, time, and item. Note that this is
        thrown when unpacking too few or two many values into a tuple
        of variables.

    :raises ValueError: If there is an issue loading the time (third
        column in each row) into a datetime object.

    :raises OSError: If there is an issue finding or opening the
        file. Note that this is thrown by the open() function.

    """
    try:
        # Create an empty timeline
        timeline = ObservationTimeline()
        # Dictionary mapping agent's name to held item
        carrying = {}
        # Read data from input file
        with open(filename, newline='') as csvfile:
            obs = csv.reader(csvfile, delimiter='\n')
            for row in obs:
                # Unpack each row
                col = tuple(row[0].split(','))
                # If too many or too few arguments, Error
                if not len(col) == 4:
                    raise ValueError("Unpacking row error")
                # Adds observation to timeline
                timeline.add(Observation(col[0], col[1], col[2]))
                # If agent is carrying item, add to timeline
                if not col[3] == '':
                    carrying.update({col[0]: col[3]})
        # Return Tuple of carried item dict and ObsTimeline
        return (carrying, timeline)
    except OSError:
        raise OSError("Cannot open file")


def main(args):
    """Program entry point.

    - Loads a CSV file of observations

    - Determines how items were exchanged during various rendezvous

      - Prints the exchanges as they happen, if desired

    - Prints the latest owner of a specific item, if desired.

      - Otherwise neatly prints a dictionary mapping suspects to
        the item they currently own.

    This program will return an exit code of `1` in one of two
    situations:

    - If the CSV file cannot be opened (i.e., load_timeline raises an
      :class:`OSError`), this program will simply print the exception
      and end.

    - If the CSV file cannot be loaded (i.e., load_timeline raises a
      :class:`ValueError`), we will print an error messsage and end.

    :param argparse.Namespace args: A Namespace that contains parsed
        command line arguments.

    :returns: Nothing

    """
    # Tuple of carried items and timeline
    time_tuple = load_timeline(args.observations)

    # For each Observation in list, calculated final held item
    for suspectPair in time_tuple[1].rendezvous():
        # If user wanted exchanges, print each exchange
        if args.exchanges:
            print(suspectPair[0].name + " meets with " +
                  suspectPair[1].name +
                  " to exchange " + time_tuple[0][suspectPair[0].name] +
                  " for " + time_tuple[0][suspectPair[1].name] + ".")
        # Trades items
        temp_item = time_tuple[0][suspectPair[0].name]
        time_tuple[0][suspectPair[0].name] = time_tuple[0][suspectPair[1].name]
        time_tuple[0][suspectPair[1].name] = temp_item

    # If no items specified or exchanges is true,
    # print list of final help items
    if (args.item == '') or (args.exchanges):
        pprint.pprint(time_tuple[0], indent=4)

    # If user specified an item, print who has said item
    if not args.item == '':
        for name, i in time_tuple[0].items():
            if i == args.item:
                print(name + " had the " + i)


if __name__ == '__main__':
    # Initialize CLI argument parser
    parser = argparse.ArgumentParser(
        description='List rendezvous exchanges based on a '
        'spreadsheet of suspect observations.'
    )

    # Add a positional argument for the observations file.
    parser.add_argument('observations',
                        help='A CSV file to read observations from.')

    # Add an optional flag, so that the user can tell us which item
    # they want to see the owner of
    parser.add_argument('--item', type=str, default='',
                        help='An optional item to print the owner of.')

    # Add an optional flag, that will tell us to print exchanges as
    # they occur instead of printing the whole mapping at the end.
    parser.add_argument('--exchanges', action='store_true',
                        help='Print all exchanges')

    # Parse the arguments
    args = parser.parse_args()

    # GO!
    main(args)
