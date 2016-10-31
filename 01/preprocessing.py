# coding: utf-8

"""
Module containing preprocessing functions.
Non-ASCII characters are used. Be sure to set utf-8 encoding in your text editor.
"""
import nltk
from unidecode import unidecode
import re

stopwords = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.porter.PorterStemmer()


def preprocess(text, stem=False):
    tokens = _tokenize(text)
    tokens = _normalize(tokens)
    tokens = _remove_non_alphanum(tokens)
    tokens = _remove_stopwords(tokens)
    if stem: tokens = _stem(tokens)
    return tokens


def _tokenize(text):
    text = re.sub(r'(\S*?)/(\S*?)', r'\1 / \2', text) # split all possible alternatives FIRST
    text = re.sub(r'(\d+)\s?/\s?(\d+)', r'\1/\2', text) # THEN congeal only fractions
    # finally word_tokenize splits off punctuation OTHER THAN PERIODS (note: trailing periods are still removed)
    return nltk.word_tokenize(text)


def _normalize(tokens):
    # unidecode removes diacritics and converts special unicode characters (like fractions) into a
    # somewhat "equivalent" ASCII representation (e.g. splits u'½' in '1/2')
    tokens = [unidecode(t.lower()) for t in tokens]
    # tokens = _replace_fractions(tokens) # do we even care? disabled for now
    return tokens


def _replace_fractions(tokens):
    pass


def _remove_non_alphanum(tokens):
    return [t for t in tokens if _isalnum(t)]


def _isalnum(t):
    if t.isalnum():
        return True
    elif (re.match(r'[+-]?[\d]+', t)  # signed number
            or re.match(r'[+-]?[\d]*\.[\d]+', t)  # decimal number
            or re.match(r'[\d]+.[\d]+', t)):  # fraction, range, or any other symbol separated pair of numbers
        return True
    else:
        return False


def _remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords]


def _stem(tokens):
    return [stemmer.stem(t) for t in tokens]
