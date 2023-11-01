"""This file contains constants of keywords for parsing and a method to parse keywords from award names."""

AWARD_CATEGORIES = {'film', 'picture', 'television', 'series',
                    'song', 'score', 'actress', 'actor', 'director', 'screenplay', 'script'}
AWARD_CATEGORIES_PICTURE_TYPE = {'film', 'picture', 'television', 'series',
                                 'song', 'score', 'screenplay', 'script'}
AWARD_CATEGORIES_CELEBRITY_TYPE = {'actress', 'actor', 'director'}
AWARD_QUALIFIERS = {'picture', 'television', 'mini-series', 'series',
                    'comedy', 'musical', 'drama', 'animated', 'supporting', 'foreign', 'language'}

WINNER_KEYWORDS = {'wins', 'receives'}

WINNERS = ["award", "winner", "won", "receives", "recipient",
           "nominee", "nominated", "prize", "congratulations", "honored", "got"]

NOMINEES = []

PRESENTER_KEYWORDS_PLURAL = {'award', 'present', 'to present'}
PRESENTER_KEYWORDS_SINGULAR = {'awards', 'presents', 'to present'}


def extract_keywords_from_award_names(award_names):
    """
    Extracts keywords from award names.

    Args:
        award_names: List of award names. 
    Returns:
        Dictionary of award names mapped to their corresponding list of keywords.
    """
    keywords = {}
    for award_name in award_names:
        keywords[award_name] = {'must_have': [], 'qualifiers': []}

        if ' award' in award_name:
            award_celebrity_name = award_name.split(' award')[0]
            keywords[award_name]['must_have'].append('award')
            keywords[award_name]['must_have'].append(award_celebrity_name)
            continue

        keywords[award_name]['must_have'].append('best')

        words = award_name.split()
        for word in words:
            if word in AWARD_CATEGORIES:
                keywords[award_name]['must_have'].append(word)
                break

        for word in words:
            if word in AWARD_QUALIFIERS:
                keywords[award_name]['qualifiers'].append(word)

    return keywords
