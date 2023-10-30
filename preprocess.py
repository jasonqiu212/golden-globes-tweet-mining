"""This file preprocesses the tweets before extraction."""

import ftfy
from langdetect import detect
import re
from unidecode import unidecode


def fix_mojibake(str):
    """
    Fixes mojibake in text.
    """
    return ftfy.fix_text(str)


def transform_to_ASCII(str):
    """
    Replaces non-ASCII characters with ASCII counterparts.
    Removes characters otherwise.
    """
    return unidecode(str)


def remove_extra_whitespace(str):
    """Replaces extra whitespace with a single space."""
    return re.sub(" +", " ", str)


def remove_URLs(str):
    """Removes URLs from text."""
    return re.sub("https?:\/\/(\S*)", "", str)


def is_english(str):
    """Checks if text is in English."""
    return detect(str) == 'en'


def remove_symbol_and_split(match):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', match.group(1))


def process_ats(str):
    return re.sub("@(\S*)", remove_symbol_and_split, str)


def process_hashtags(str):
    return re.sub("#(\S*)", remove_symbol_and_split, str)


def get_hashtags(str):
    hashtags = re.findall(r'#\w+', str)
    list = []
    for i in hashtags:
        word_without_hashtag = i.lstrip('#')
        formatted_word = re.sub(
            r'([a-z])([A-Z])', r'\1 \2', word_without_hashtag)
        list.append(formatted_word)
    return list


def preprocess(tweets):
    for tweet in tweets:
        tweet.applyTextPreprocessing(fix_mojibake)
        tweet.applyTextPreprocessing(transform_to_ASCII)
        tweet.applyTextPreprocessing(remove_extra_whitespace)
        tweet.applyTextPreprocessing(remove_URLs)
        tweet.applyTextPreprocessing(process_ats)
        tweet.hashtags = get_hashtags(tweet.text)
        tweet.applyTextPreprocessing(process_hashtags)
    return list(filter(lambda t: is_english(t.text), tweets))
