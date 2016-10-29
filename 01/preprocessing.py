"""Module containing preprocessing functions."""
import nltk
from unidecode import unidecode

stopwords = set(nltk.corpus.stopwords.words('english'))
stemmer = nltk.stem.porter.PorterStemmer()


def preprocess(text, stem=False):
    tokens = _tokenize(text)
    tokens = _normalize(tokens)
    tokens = _remove_non_alphanum(tokens)
    tokens = _remove_stopwords(tokens)
    if (stem): tokens = _stem(tokens)
    return tokens


def _tokenize(text):
    return nltk.word_tokenize(text)


def _normalize(tokens):
    """Normalize tokens by removing diacritics and converting to lowercase."""
    return [unidecode(t.decode('utf-8').lower()) for t in tokens]


def _remove_non_alphanum(tokens):
    return [t for t in tokens if t.isalnum()]


def _remove_stopwords(tokens):
    return [t for t in tokens if t not in stopwords]


def _stem(tokens):
    return [stemmer.stem(t) for t in tokens]
