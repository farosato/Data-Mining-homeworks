# coding: utf-8

"""
Module containing preprocessing functions.
Non-ASCII characters are used. Be sure to set utf-8 encoding in your text editor.
"""
import nltk
from unidecode import unidecode

HALF = u'½'
HALF_REPLACEMENT = u'.5'

stopwords = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.porter.PorterStemmer()


def preprocess(text, stem=False):
    tokens = _tokenize(text)
    tokens = _normalize(tokens)
    tokens = _remove_stopwords(tokens)
    if stem: tokens = _stem(tokens)
    return tokens


def _tokenize(text):
    return nltk.word_tokenize(text)


def _normalize(tokens):
    """Normalize tokens by removing diacritics and converting to lowercase."""
    tokens = _replace_half(tokens) # has to be called before unideconding
    return [unidecode(t.lower()) for t in tokens]


def _remove_non_alphanum(tokens):
    return [t for t in tokens if t.isalnum()]


def _remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords]


def _stem(tokens):
    return [stemmer.stem(t) for t in tokens]


def _replace_half(tokens):
    """Replace non-ASCII 'half' character to preserve ingredients quantities"""
    return [t.replace(HALF, HALF_REPLACEMENT) for t in tokens]