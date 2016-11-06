from __future__ import division
import unicodecsv as csv
import pickle
from preprocess_recipes import DEST as SRC
from math import log10, sqrt
import time

DEST = 'doc_term_matrix_and_index.pickle'
DEST_OPT = 'optimized_index.pickle'
FIELDS_WEIGHTS = [4, 1, 1, 1, 1, 1, 3, 3, 2]  # sorted according to header line


def _bsearch_posting(plist, doc_id):
    """Performs binary search on the posting list, returning the posting whose doc_id is the one specified."""
    min_i = 0
    max_i = len(plist) - 1
    while True:
        if max_i < min_i:
            raise ValueError(doc_id)  # not found
        mid = (min_i + max_i) // 2
        if plist[mid][0] < doc_id:
            min_i = mid + 1
        elif plist[mid][0] > doc_id:
            max_i = mid - 1
        else:
            return mid


if __name__ == "__main__":
    start_time = time.time()

    # Scan each doc, and each term in it, building as you go both
    # the doc-term (sparse) matrix and (its transpose) the index.
    with open(SRC, 'rb') as tsv_file:
        tsvReader = csv.reader(tsv_file, delimiter='\t')
        next(tsvReader)  # skip header line

        # the index is represented as a dictionary of term -> list of postings pairs:
        # a posting is represented as a list [doc_id, tf]
        # e.g. { 'apple': [ [0, 3], [3, 1], ... ], 'banana': [ [0, 5], ... ], ... }
        index = {}

        # the doc-term matrix is represented as a list of docs (rows):
        # each doc is a dictionary (sparse vector) of term -> tf pairs;
        # to decrease memory requirements, the matrix cells (instead of the single tf value)
        # actually contain (the reference to) the corresponding posting in the index (memory sharing)
        # e.g. [ { 'apple': [0, 3], 'banana': [0, 5], ... }, { ... }, ... ]
        doc_term_matrix = []

        for doc_id, doc in enumerate(tsvReader):
            doc_term_matrix.append({})
            for field_id, field in enumerate(doc):
                for term in field.split():
                    try:
                        # increment tf taking into account the weight of the field in which term occurs.
                        # e.g. if term occurs in title, then it is more relevant than the same term occurring in method.
                        # therefore, in the first case tf is increased more (it also makes total score increase).
                        doc_term_matrix[doc_id][term][1] += FIELDS_WEIGHTS[field_id]
                    except KeyError:  # term is not in the dictionary
                        doc_term_matrix[doc_id][term] = [doc_id, FIELDS_WEIGHTS[field_id]]

                    # share the memory for the postings/matrix cells
                    try:
                        index[term][_bsearch_posting(index[term], doc_id)] = doc_term_matrix[doc_id][term]
                    except KeyError:  # term is not in the index
                        index[term] = [doc_term_matrix[doc_id][term]]
                    except ValueError:  # a posting with that doc_id is not in the posting list
                        index[term].append(doc_term_matrix[doc_id][term])

        # note: by construction, the index contains, for each term, a posting list that is ORDERED wrt the doc_ids

        num_docs = doc_id + 1

    # Pickle (serialize) the doc-term matrix and the index;
    # we're pickling this "non-optimized" version of the index because
    # it can be extended simply should new recipes be added to the corpus
    # (optimized version we're going to create really can't be extended)
    # note: pickle supports "object sharing", preserving our memory sharing trick (JSON doesn't)
    with open(DEST, 'wb') as data_dump:
        # need to pickle them together for the sharing to be preserved
        pickle.dump([num_docs, doc_term_matrix, index], data_dump)

    # Optimize index for query processing;
    # for each posting in a term posting list, we want to have the complete (query-independent) factor
    # (i.e. tf * idf^2 / ||doc||), instead of the simple tf.

    # first we compute the idf for each term
    idf = {}
    for term in index:
        doc_freq = len(index[term])
        idf[term] = log10(num_docs/doc_freq)

    # then we compute the document vectors lengths
    doc_lengths = []
    for doc_id, doc in enumerate(doc_term_matrix):
        squared_sum = 0
        for term in doc:
            doc_term_matrix[doc_id][term][1] *= idf[term]
            squared_sum += doc_term_matrix[doc_id][term][1]**2
        doc_len = sqrt(squared_sum)

        # remember the memory sharing?
        # we computed the vector length, then we might as well exploit this loop
        # to finish the computation of the query-independent factor
        for term in doc:
            try:
                doc_term_matrix[doc_id][term][1] *= idf[term] / doc_len
            except ZeroDivisionError:
                # can only happen if the doc is made up of words present in ALL other docs
                # in that case the tf-idf is zero, so nothing to do
                pass

    # Pickle (serialize) the optimized index
    with open(DEST_OPT, 'wb') as data_dump:
        pickle.dump(index, data_dump)

    print("\n--- %s seconds ---" % (time.time() - start_time))
