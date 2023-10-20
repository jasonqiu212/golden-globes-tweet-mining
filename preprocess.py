"""This file preprocesses the tweets before extraction."""

import ftfy
from langdetect import detect
import unidecode

def fixMojibake(str):
    return ftfy.fix_text(str)

def transformToASCII(str):
    return unidecode(str)

def removeURLs(str):
    return str

def removeWhitespace(str):
    return str

def isEnglish(str):
    """
    Checks if text is in English.

    Args:
        str: Text to check.
    
    Returns:
        True, if text is in English. False otherwise.
    """
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
        tweet.applyPreprocessing(fixMojibake)
        tweet.applyPreprocessing(transformToASCII)
        tweet.applyPreprocessing(removeURLs)
        tweet.applyPreprocessing(removeWhitespace)
    return filter(lambda t : isEnglish(t.text), tweets)
