import preprocessing
import pickle
from store_recipes import DEST as SRC
from build_index import DEST_OPT as IDX_SRC
from collections import defaultdict
from operator import itemgetter
import time
import heapq

RESULT_SIZE = 20
DOC_ID_OFFSET = 1
REC_NAME = 0
REC_AUTHOR = 1
REC_PREP_TIME = 2
REC_COOK_TIME = 3
REC_PEOPLE_NUM = 4
REC_DIET_INFO = 5
REC_DESCR = 6
REC_INGR = 7
REC_METHOD = 8
SEPARATOR = 30
PROMPT = 'Type your query: '


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


def retrieve_docs_contents(processing_result):
    """Present to the user the contents of the K most related documents."""
    with open(SRC, 'r') as corpus:
        # get a sorted list of the doc-ids in the query processing result
        result_sorted_by_docid = sorted(processing_result, key=itemgetter(0))
        result_ids = [doc_id + DOC_ID_OFFSET for doc_id, _ in result_sorted_by_docid]

        # retrieve docs contents and sort them by score
        i = 0
        result_recipes = []
        for doc_id, recipe in enumerate(corpus):
            if doc_id > result_ids[-1]:
                break
            if doc_id == result_ids[i]:
                score = result_sorted_by_docid[i][1]
                result_recipes.append((recipe, score))
                i += 1
        result_recipes_sorted_by_score = sorted(result_recipes, key=itemgetter(1), reverse=True)

        # present first K contents
        for result_num, (recipe, score) in enumerate(result_recipes_sorted_by_score):
            if result_num >= RESULT_SIZE:
                break
            print '\nResult #%d (score: %f)' % (result_num + 1, score)
            present_recipe(recipe.split('\t'))


def present_recipe(recipe):
    # print recipe in a structured way
    print '\n\"' + recipe[REC_NAME] + '\" by ' + recipe[REC_AUTHOR]
    print 'Preparation time: ' + recipe[REC_PREP_TIME]
    print 'Cooking time: ' + recipe[REC_COOK_TIME]
    print recipe[REC_PEOPLE_NUM]

    if recipe[REC_DIET_INFO] != '':
        print 'Dietary: ' + recipe[REC_DIET_INFO]

    if recipe[REC_DESCR] != '':
        print '\nDescription:\n' + recipe[REC_DESCR]

    print '\nIngredients:'
    for i in recipe[REC_INGR].split('|'):
        print '- ' + i.strip()

    print '\nMethod:'
    for i in recipe[REC_METHOD].split('|'):
        print '- ' + i.strip()

    print '\n'+('#'*SEPARATOR)


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
