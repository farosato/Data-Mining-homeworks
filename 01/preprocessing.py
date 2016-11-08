""" Module containing preprocessing functions. """
import nltk
from unidecode import unidecode
import re

stopwords = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.porter.PorterStemmer()


def preprocess(text, stem=False, query=False):
    tokens = _tokenize(text)
    tokens = _normalize(tokens)
    tokens = _remove_stopwords(tokens)
    if query:
        tokens = _remove_non_alphanum_in_query(tokens)
    else:
        tokens = _remove_non_alphanum(tokens)
    if stem:
        tokens = _stem(tokens)
    return tokens


def _tokenize(text):
    text = re.sub(r'(\S*?)/(\S*?)', r'\1 / \2', text)    # split all possible alternatives FIRST
    text = re.sub(r'(\d+)\s?/\s?(\d+)', r'\1/\2', text)  # THEN congeal only fractions
    return nltk.word_tokenize(text)  # splits off punctuation OTHER THAN PERIODS (trailing periods are still removed)


def _normalize(tokens):
    """ unidecode removes diacritics and converts special unicode characters (like fractions) into a
        somewhat "equivalent" ASCII representation """
    tokens = [unidecode(t.lower()) for t in tokens]
    return tokens


def _remove_non_alphanum(tokens):
    return [t for t in tokens if _isalnum(t)]


def _remove_non_alphanum_in_query(tokens):
    return [t for t in tokens if _isalnum_in_query(t)]


def _isalnum(t):
    if t.isalnum():
        return True
    elif (re.match(r'[+-]?[\d]+', t)              # signed number
            or re.match(r'[+-]?[\d]*\.[\d]+', t)  # decimal number
            or re.match(r'[\d]+.[\d]+', t)):      # fraction, range, or any other symbol separated pair of numbers
        return True
    return False


def _isalnum_in_query(t):
    # save reserved special characters in query
    if t == '||' or t[0] == '-':
        return True
    return _isalnum(t)


def _remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords]


def _stem(tokens):
    return [stemmer.stem(t) for t in tokens]
