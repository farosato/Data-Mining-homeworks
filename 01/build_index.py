import unicodecsv as csv
from preprocess_recipes import DEST as SRC


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
    with open(SRC, 'rb') as tsv_file:
        tsvReader = csv.reader(tsv_file, delimiter='\t')
        next(tsvReader)  # skip header line

        # scan each doc, and each term in it, building as you go both
        # the doc-term (sparse) matrix and (its transpose) the index

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
            for field in doc:
                for term in field.split():
                    try:
                        doc_term_matrix[doc_id][term][1] += 1  # increment tf
                    except KeyError:  # term is not in the dictionary
                            doc_term_matrix[doc_id][term] = [doc_id, 1]

                    # share the memory for the postings/matrix cells
                    try:
                        index[term][_bsearch_posting(index[term], doc_id)] = doc_term_matrix[doc_id][term]
                    except KeyError:  # term is not in the index
                        index[term] = [doc_term_matrix[doc_id][term]]
                    except ValueError:  # a posting with that doc_id is not in the posting list
                        index[term].append(doc_term_matrix[doc_id][term])

        # note: by construction, the index contains, for each term, a posting list that is ORDERED wrt the doc_ids

        print '### Doc-term matrix ###'
        print doc_term_matrix
        print '\n### Index ###'
        print index
