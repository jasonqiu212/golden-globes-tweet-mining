"""This file provides operations to read and write to files."""

import json

from tweet import Tweet


def load_tweets(file_name):
    """
    Loads tweets from JSON data file.

    Args:
        file_name: File name of JSON data file.
    Returns:
        List of tweets from JSON file.
    """
    # Uncomment following line to try on smaller subset of datafile
    with open(file_name) as json_file:
        # with open("gg{}-subset.json".format(2013)) as json_file:
        data = json.load(json_file)

        return list(map(lambda t: Tweet(t['text'], t['user']['screen_name']), data))


def load_awards(file_name):
    """
    Loads official award names from JSON answer file.

    Args:
        file_name: File name of JSON answer file.
    Returns:
        List of official award names from JSON file.
    """
    with open(file_name) as json_file:
        data = json.load(json_file)
        return list(data['award_data'].keys())


def write_results(data, year):
    """Writes extracted information to JSON results file."""
    json_object = json.dumps(data, indent=4)
    with open("gg{}results.json".format(year), "w") as f:
        f.write(json_object)
    print('5/6: Finished writing to JSON result file.')


def write_human_readable_results(data, year):
    """Writes extracted information to human-readable results file."""
    lines = []

    lines.append('Hosts: ' + ', '.join(data['hosts']))
    lines.append('')

    lines.append('Awards: ' + ', '.join(data['awards']))
    lines.append('')

    for award in data['award_results'].keys():
        award_result = data['award_results'][award]

        lines.append('Award: ' + award)
        lines.append('Presenters: ' + ', '.join(award_result['presenters']))
        lines.append('Nominees: ' + ', '.join(award_result['nominees']))
        lines.append('Winner: ' + award_result['winner'])
        lines.append('')

    with open("gg{}results_humanreadable.txt".format(year), "w") as f:
        f.writelines(line + '\n' for line in lines)
    print('6/6: Finished writing to human readable result file.')


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
