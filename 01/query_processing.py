import preprocessing
import pickle
import unicodecsv as csv
from store_recipes import DEST as SRC
from build_index import DEST_OPT as IDX_SRC
from collections import defaultdict
from operator import itemgetter

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

    # return the docs in descending order of the score
    # TODO think about using the approach discussed in class (add items to a fixed-size heap) and return only first k docs
    sorted_results = sorted(scores.items(), key=itemgetter(1))
    return sorted_results


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
        print 'loading index...'
        index = pickle.load(pickled_index)

    with open(SRC, 'rb') as tsv_file:
        # TODO could be too costly to load all corpus in a list, think about accessing directly .html files and rescrap them
        print 'loading corpus...'
        tsvReader = csv.reader(tsv_file, delimiter='\t')
        next(tsvReader)  # skip header line
        corpus = list(tsvReader)


    # TODO create while loop to allow user to retype queries
    #query = raw_input('\nType your query: ')

    # dummy example
    query = 'butter apple'

    result = process_query(index, query)
    for k in result:
        present_recipe(corpus[k[0]])