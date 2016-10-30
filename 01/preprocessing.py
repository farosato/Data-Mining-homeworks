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
    return nltk.word_tokenize(text)


def _normalize(tokens):
    # unidecode removes diacritics and converts special unicode characters (like fractions) into a
    # somewhat "equivalent" ASCII representation (e.g. splits u'½' in '1/2')
    return [unidecode(t.lower()) for t in tokens]
    # tokens = _replace_fractions(tokens) # do we even care? disabled for now


def _replace_fractions(tokens):
    # return [t.replace(u'½', u'0.5') for t in tokens]
    pass


def _remove_non_alphanum(tokens):
    return [t for t in tokens if _isalnum(t)]


def _isalnum(t):
    if t.isalnum():
        return True
    elif re.match(r'[0-9]*[./][0-9]+'): # decimal number or fraction
        return True;
    else:
        return False


def _remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords]


def _stem(tokens):
    return [stemmer.stem(t) for t in tokens]
