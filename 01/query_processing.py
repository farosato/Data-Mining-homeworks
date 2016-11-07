""" Module containing query processing functions. """
import preprocessing
from collections import defaultdict


def process_query(index, text):
    # preprocess the query
    tokens = preprocessing.preprocess(text.decode())  # need the query to be unicode

    # represent the query as a vector of tf
    query_vec = {}
    for t in tokens:
        try:
            query_vec[t] += 1
        except KeyError:
            query_vec[t] = 1

    # score the docs that contain at least a term of the query
    scores = defaultdict(int)
    for term in query_vec:
        try:
            for posting in index[term]:
                doc_id, qif = posting  # qif is the query independent factor stored in the optimized index
                scores[doc_id] += query_vec[term] * qif
                # note: we're ignoring the query vector length cause it is just a constant factor for ALL the docs
                # (i.e. it won't change the similarity ordering)
        except KeyError:  # term is not in the index
            pass

    # return the unsorted set of docs
    return scores.items()