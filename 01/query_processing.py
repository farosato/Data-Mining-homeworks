import preprocessing
import pickle
from build_index import DEST_OPT as IDX_SRC
from collections import defaultdict
from operator import itemgetter

with open(IDX_SRC, 'rb') as pickled_index:
    index = pickle.load(pickled_index)

def process_query(text):
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

    # return the docs in descending order of the score
    # TODO think about using the approach discussed in class (add items to a fixed-size heap) and return only first k docs
    sorted_results = sorted(scores.items(), key=itemgetter(1))
    return sorted_results

if __name__ == "__main__":
    """ dummy example """
    query = 'butter apple'
    result = process_query(query)
    for k in result:
        print k
