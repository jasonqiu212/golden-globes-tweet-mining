"""This file preprocesses the tweets before extraction."""

import re

import ftfy
from langdetect import detect
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
    try:
        language = detect(str)
        return language == 'en'
    except:
        return False


def remove_symbol_and_split(match):
    return re.sub(r'([a-z])([A-Z])', r'\1 \2', match.group(1))


def process_ats(str):
    return re.sub("@(\S*)", remove_symbol_and_split, str)


def process_hashtags(str):
    return re.sub("#(\S*)", remove_symbol_and_split, str)


def replace_ampersand(str):
    return re.sub("&", "and", str)


def preprocess(str):
    str = fix_mojibake(str)
    str = transform_to_ASCII(str)
    str = remove_extra_whitespace(str)
    str = remove_URLs(str)
    str = process_ats(str)
    str = process_hashtags(str)
    str = str.lower()
    str = replace_ampersand(str)
    return str
