"""This file reads in tweets from JSON data files."""

import json

from tweet import Tweet


def load_json(year=2013):
    """
    Loads tweets from JSON file.

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
