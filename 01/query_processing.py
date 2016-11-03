import preprocessing
import pickle
from store_recipes import DEST as SRC
from build_index import DEST_OPT as IDX_SRC
from collections import defaultdict
from operator import itemgetter
import time
import heapq

RESULT_SIZE = 20
REC_NAME = 0
REC_AUTHOR = 1
REC_PREP_TIME = 2
REC_COOK_TIME = 3
REC_PEOPLE_NUM = 4
REC_DIET_INFO = 5
REC_DESCR = 6
REC_INGR = 7
REC_METH = 8
PROMPT = 'Type your query: '


"""
def add_score(h, entry):
    # entry has to be a tuple (score, doc_id)
    if len(h) < RESULT_SIZE:
        heapq.heappush(h, entry)
    else:
        # Equivalent to a push, then a pop, but faster
        heapq.heappushpop(h, entry)
"""


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

    # TODO evaluate implementation with heap, after checking performances with complete corpus
    #sorted_results = sorted(scores.items(), key=itemgetter(1))
    #return sorted_results

    # return the unsorted set of docs
    return scores.items()


def retrieve_docs_contents(processing_result):
    """ Present to user the contents of the K most related documents """
    with open(SRC, 'r') as corpus:
        next(corpus)  # skip header line

        docs = []
        sorted_result_by_id = sorted(processing_result, key=itemgetter(0))
        for doc_id, _ in sorted_result_by_id:
            docs.append(doc_id)

        i = 0
        last = docs[len(docs) - 1]
        sorted_result_by_score = []
        for doc_id, line in enumerate(corpus):
            if doc_id > last:
                break
            if doc_id == docs[i]:
                sorted_result_by_score.append((line, sorted_result_by_id[i][1]))
                i += 1
        sorted_result_by_score = sorted(sorted_result_by_score, key=itemgetter(1))

        j = 0
        for e in sorted_result_by_score:
            if j >= RESULT_SIZE:
                break
            present_recipe(e[0].split('\t'))
            j += 1


def present_recipe(row):
    # print recipe in a structured way
    print '\n\"' + row[REC_NAME] + '\" by ' + row[REC_AUTHOR]
    print 'Preparation time: ' + row[REC_PREP_TIME]
    print 'Cooking time: ' + row[REC_COOK_TIME]
    print 'Serves: ' + row[REC_PEOPLE_NUM]

    if row[REC_DIET_INFO] != '':
        print 'Dietary: ' + row[REC_DIET_INFO]

    if row[REC_DESCR] != '':
        print '\nDescription:\n' + row[REC_DESCR]

    print '\nIngredients:'
    for i in row[REC_INGR].split('|'):
        print '- ' + i.strip()

    print '\nMethod:'
    for i in row[REC_METH].split('|'):
        print '- ' + i.strip()

    print '\n'+('#'*30)


if __name__ == "__main__":

    with open(IDX_SRC, 'rb') as pickled_index:
        print 'Loading index...'
        start_time = time.time()
        index = pickle.load(pickled_index)
        print("Index loaded in %s seconds." % (time.time() - start_time))

    query = raw_input('\n' + PROMPT)
    while query != '':
        start_time = time.time()
        retrieve_docs_contents(process_query(index, query))

        print("Query answered in %s seconds." % (time.time() - start_time))
        query = raw_input('\n' + PROMPT)
