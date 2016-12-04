"""
Module containing near duplicates computation. Two implementations are provided:
- lsh-based
- brute force approach
"""
from __future__ import division
import __init__  # update Python PATH
from hw01.store_recipes import DEST as SRC
import hashing
import shingling
import time
import os
import pickle


SRC_BRUTE_FORCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brute_force_near_duplicates.pickle')
SEPARATOR = 50
SHINGLE_SIZE = 10


def lsh_near_duplicates(shingles_sets):
    """
    Given a collection of shingles sets of a set of documents,
    it finds the all the documents pairs that are near each other.
    The procedure is defined in LRU book as follow.
    """

    """
    1. Pick a value of k and construct from each document the set of k-shingles.
    Optionally, hash the k-shingles to shorter bucket numbers.

    2. Sort the document-shingle pairs to order them by shingle.

    [NOTE: previous steps are implemented in shingling.py. It is performed outside
    this function to reuse shingles in brute force approach.]

    3. Pick a length n for the minhash signatures. Feed the sorted list to the
    algorithm of Section 3.3.5 to compute the minhash signatures for all the
    documents.
    """

    minhash_signatures = hashing.minwise_hashing(shingles_sets)

    """
    4. Choose a threshold t that defines how similar documents have to be in
    order for them to be regarded as a desired "similar pair." Pick a number
    of bands b and a number of rows r such that br = n, and the threshold
    t is approximately (1/b)^(1/r). If avoidance of false negatives is important,
    you may wish to select b and r to produce a threshold lower than t; if
    speed is important and you wish to limit false positives, select b and r to
    produce a higher threshold.
    [NOTE: t = 0.8, n = 8]

    5. Construct candidate pairs by applying the LSH technique of Section 3.4.1.

    6. Examine each candidate pair's signatures and determine whether the fraction of
    components in which they agree is at least t.
    """

    return hashing.lsh(minhash_signatures)  # return near duplicates


def brute_force_near_duplicates(shingles_sets):
    """
    Given the shingles sets of each document in a set, finds the nearest neighbors
    by comparing all the shingle sets with each other.
    """
    near_duplicates = set()
    corpus_size = len(shingles_sets)
    for i, s_row in enumerate(shingles_sets):
        for j in range(i, corpus_size):
            if i != j and _jaccard_sim(shingles_sets[i], shingles_sets[j]) >= hashing.JACCARD_THRESHOLD:
                near_duplicates.add(i)
                near_duplicates.add(j)
    return near_duplicates


def create_documents_shingles(show_progress=False):
    """ Create documents shingles sets. """
    shingles_sets = []
    with open(SRC, 'r') as docs:
        docs.readline()  # skip header line

        print 'Shingling documents...'
        doc_id, line = 0, docs.readline()
        while line != '':
            if show_progress:
                print doc_id
            shingles_sets.append(shingling.shingle_hash(line, SHINGLE_SIZE))
            doc_id, line = doc_id + 1, docs.readline()
    return shingles_sets


def _jaccard_sim(a, b):
    """
    Computes Jaccard similarity of the given sets.
    Note that both params are required to be Python sets.
    """
    return len(a.intersection(b)) / len(a.union(b))


if __name__ == "__main__":
    docs_shingles = create_documents_shingles()

    # load previously computed brute force result, since it is constant
    # print '\n', '#'*SEPARATOR, '\nLoading brute force approach result...'
    # with open(SRC_BRUTE_FORCE, 'rb') as src:
    #     print 'Loading index...'
    #     brute_force = pickle.load(src)

    # find near duplicates using lsh approach
    print '\n', '#'*SEPARATOR, '\nPerforming lsh approach...'
    start_time = time.time()
    lsh = lsh_near_duplicates(docs_shingles)
    print 'LSH approach found %s near duplicates.' % len(lsh)
    print 'LSH approach took  %s seconds.' % (time.time() - start_time)

    # compare approaches
    # print '\n', '#'*SEPARATOR, '\nSize of intersection is %s duplicates.' % len(lsh.intersection(brute_force))
