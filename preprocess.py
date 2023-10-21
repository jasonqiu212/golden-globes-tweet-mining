"""This file preprocesses the tweets before extraction."""

import ftfy
from langdetect import detect
import re
from unidecode import unidecode

def fixMojibake(str):
    """
    Fixes mojibake in text.
    """
    return ftfy.fix_text(str)

def transformToASCII(str):
    """
    Replaces non-ASCII characters with ASCII counterparts.
    Removes characters otherwise.
    """
    return unidecode(str)

def removeExtraWhitespace(str):
    """Replaces extra whitespace with a single space."""
    return re.sub(" +", " ", str)

def removeURLs(str):
    """Removes URLs from text."""
    return re.sub("https?:\/\/(\S*)", "", str)

def isEnglish(str):
    """Checks if text is in English."""
    return detect(str) == 'en'

def preprocess(tweets):
    """
    Preprocesses list of tweets.

    Args:
        tweets: List of tweets.
    
    Returns:
        Preprocessed list of tweets.
    """
    for tweet in tweets:
        tweet.applyTextPreprocessing(fixMojibake)
        tweet.applyTextPreprocessing(transformToASCII)
        tweet.applyTextPreprocessing(removeExtraWhitespace)
        tweet.applyTextPreprocessing(removeURLs)
    return list(filter(lambda t : isEnglish(t.text), tweets))
