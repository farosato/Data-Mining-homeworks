import pickle
from query_processing import process_query
from store_recipes import DEST as SRC, HEADER
from build_index import DEST_OPT as IDX_SRC
from operator import itemgetter
import unicodecsv as csv
import time

RESULT_SIZE = 20
DOC_ID_OFFSET = 1
SEPARATOR = 30
PROMPT = 'Type your query: '


def retrieve_docs_contents(processing_result):
    """Returns a list of the query processing results.\n
    Each result is a tuple (recipe, score).\n
    The recipe is a dictionary containing for each recipe property the corresponding content."""
    if processing_result is None or len(processing_result) <= 0:
        # returns empty list to prevent webapp to crash
        return []

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
                # convert the recipe from a list to a dictionary of prop_name -> prop_value pairs

                # splitting on '\t' is not returning all recipes fields correctly
                # (probably because unicodecsv separates fields in some strange way)
                # So... Let the motherfucker deal with it!
                # recipe = dict(zip(HEADER, recipe.decode('utf-8').split('\t')))  # always decode as early as possible

                tsv_reader = csv.reader([recipe], delimiter='\t', encoding='utf-8')
                recipe = [field for row in tsv_reader for field in row]
                recipe = dict(zip(HEADER, recipe))
                result_recipes.append((recipe, score))
                i += 1
        result_recipes_sorted_by_score = sorted(result_recipes, key=itemgetter(1), reverse=True)

        return result_recipes_sorted_by_score


def print_to_console(scored_recipes, max_num=RESULT_SIZE):
    for result_num, (recipe, score) in enumerate(scored_recipes):
        if result_num >= max_num:
            break
        print '\nResult #%d (score: %f)' % (result_num + 1, score)
        present_recipe(recipe)


def present_recipe(recipe):
    # print recipe in a structured way
    print '\n\"' + recipe['title'] + '\" by ' + recipe['author']
    print 'Preparation time: ' + recipe['prep_time']
    print 'Cooking time: ' + recipe['cook_time']

    people_num = recipe['serves'].split()
    if len(people_num) == 1:
        print 'Serves ' + people_num[0]
    else:
        print recipe['serves']

    if recipe['dietary_info'] != '':
        print 'Dietary: ' + recipe['dietary_info']

    if recipe['description'] != '':
        print '\nDescription:\n' + recipe['description']

    print '\nIngredients:'
    for i in recipe['ingredients'].split('|'):
        print '- ' + i.strip()

    print '\nMethod:'
    for i in recipe['method'].split('|'):
        print '- ' + i.strip()

    print '\n'+('#'*SEPARATOR)


def load_index():
    with open(IDX_SRC, 'rb') as pickled_index:
        print 'Loading index...'
        start_time = time.time()
        index = pickle.load(pickled_index)
        print("Index loaded in %s seconds." % (time.time() - start_time))
        return index


if __name__ == "__main__":

    index = load_index()

    query = raw_input('\n' + PROMPT)
    while query != '':
        start_time = time.time()
        scored_recipes = retrieve_docs_contents(process_query(index, query))
        print_to_console(scored_recipes)
        print("Query answered in %s seconds." % (time.time() - start_time))
        query = raw_input('\n' + PROMPT)
