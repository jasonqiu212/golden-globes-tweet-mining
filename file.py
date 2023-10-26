"""This file provides operations to read and write to files."""

import json

from tweet import Tweet


def load_tweets(year=2013):
    """
    Loads tweets from JSON data file.

    Args:
        year: The year of the award ceremony.
    Returns:
        List of tweets from JSON file.
    """
    # with open("gg{}.json".format(year)) as json_file:
    with open("gg{}-subset.json".format(year)) as json_file:
        data = json.load(json_file)

        return list(map(lambda t: Tweet(t['text'], t['user']['screen_name']), data))


def load_awards(year=2013):
    """
    Loads official award names from JSON answer file.

    Args:
        year: The year of the award ceremony.
    Returns:
        List of official award names from JSON file.
    """
    with open("gg{}answers.json".format(year)) as json_file:
        data = json.load(json_file)
        return list(data['award_data'].keys())


def write_results(data):
    """Writes extracted information to JSON results file."""
    # TODO
    # Format of data:
    # {
    #   'hosts': [...],
    #   'awards': [...],
    #   'award_results': {
    #       'award1': {
    #           'presenters': [...],
    #           'nominees': [...],
    #           'winner': ''
    #       },
    #       'award2': {
    #           'presenters': [...],
    #           'nominees': [...],
    #           'winner': ''
    #       },
    #       ...
    #   }
    # }
    return


def write_human_readable_results(data):
    """Writes extracted information to human-readable results file."""
    # TODO: data has same format as above, but could include additional information
    return


def read_results(year, component):
    """
    Reads specified component from JSON results file.

    Args:
        year: The year of the award ceremony.
        component: Component of results to read.
    Returns:
        List of host or award names, if for 'hosts' or 'awards' components.
        Dictionary with hard-coded award names as keys and results as entries, 
        if for 'nominees', 'presenters', or 'winner' components.
    """
    with open("gg{}results.json".format(year)) as json_file:
        data = json.load(json_file)
        if component == 'hosts' or component == 'awards':
            return data[component]
        awards = list(data['award_results'].keys())
        return dict((award, data['award_results'][award][component]) for award in awards)
