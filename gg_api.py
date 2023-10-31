from extract import extract
from file import load_awards, load_tweets, read_results, write_human_readable_results, write_results
from merge import merge
from preprocess import preprocess


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    return read_results(year, 'hosts')


def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    return read_results(year, 'awards')


def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    return read_results(year, 'nominees')


def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    return read_results(year, 'winner')


def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    return read_results(year, 'presenters')


def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    print("Pre-ceremony processing complete.")
    return


def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    YEAR = 2013

    tweets = preprocess(load_tweets(YEAR))
    official_award_names = load_awards(YEAR)
    preliminary_results = extract(tweets, official_award_names)
    final_results = merge(preliminary_results)
    write_results(final_results, YEAR)
    write_human_readable_results(final_results, YEAR)


if __name__ == '__main__':
    main()
