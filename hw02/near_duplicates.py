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
from shutil import copyfile


SRC_BRUTE_FORCE_REPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brute_force_results.txt')
SRC_BRUTE_FORCE_SIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brute_force_similarities.pickle')
DEST_REPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.txt')
SEPARATOR = 60
TRAILER = '\n' + '#'*SEPARATOR + '\n'

SHINGLE_SIZE = 10


def lsh_near_duplicates(shingle_sets, debug=False):
    """
    Given a collection of shingles sets of a collection of documents,
    it finds all the documents pairs that are near each other.
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

    minhash_signatures = hashing.minwise_hashing(shingle_sets, debug)

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

    return hashing.lsh(minhash_signatures, debug)  # return near duplicates


def brute_force_near_duplicates(shingle_sets):
    """
    Given the shingles sets of each document in a set, finds the nearest neighbors
    by comparing all the shingle sets with each other.
    """
    similarities = set()
    corpus_size = len(shingle_sets)
    for i in range(0, corpus_size):
        for j in range(i + 1, corpus_size):
            similarity = _jaccard_sim(shingle_sets[i], shingle_sets[j])
            if similarity >= hashing.JACCARD_THRESHOLD:
                similarities.add((i, j, similarity))
    return similarities


def create_documents_shingles(show_progress=False):
    """ Create documents shingles sets. """
    shingle_sets = []
    with open(SRC, 'r') as docs:
        docs.readline()  # skip header line

        print 'Shingling documents...'
        doc_id, line = 0, docs.readline()
        while line != '':
            if show_progress:
                print doc_id
            shingle_sets.append(shingling.shingle(line, SHINGLE_SIZE))
            doc_id, line = doc_id + 1, docs.readline()
    return shingle_sets


def _jaccard_sim(a, b):
    """
    Computes Jaccard similarity of the given sets.
    Note that both params are required to be Python sets.
    """
    intersection = len(a.intersection(b))
    return intersection / (len(a) + len(b) - intersection)


if __name__ == "__main__":
    docs_shingles = create_documents_shingles()
    # No real point in hashing the shingles since we're going to perform minhashing (except trivial compression)
    docs_shingles = [shingling.hash_shingles(s) for s in docs_shingles]

    # load previously computed brute force result, since it is constant
    print '\n', '#'*SEPARATOR, '\nLoading brute force approach result...'
    with open(SRC_BRUTE_FORCE_SIM, 'rb') as src:
        brute_force_sim = pickle.load(src)

    # find near duplicates using lsh approach
    print '\n', '#'*SEPARATOR, '\nPerforming lsh approach (b = %d, r = %d)...' % (hashing.BANDS, hashing.ROWS_PER_BAND)
    start_time = time.time()
    lsh_sim = lsh_near_duplicates(docs_shingles, debug=True)
    tot_time = time.time() - start_time

    # write report
    copyfile(SRC_BRUTE_FORCE_REPORT, DEST_REPORT)
    with open(DEST_REPORT, 'a') as report:
        report.write('\n')

        duplicates_num = 'LSH approach found %s near duplicate pairs.' % len(lsh_sim)
        report.write(duplicates_num + '\n')

        running_time = 'LSH approach took  %s seconds.' % tot_time
        report.write(running_time + '\n')

        report.write('\n')

        for t in lsh_sim:
            row = '%s <-> %s \tsim = %f' % ('{0: <5}'.format(t[0]), '{0: <5}'.format(t[1]), t[2])
            report.write(row + '\n')

        report.write(TRAILER)

        # compute approaches intersection
        lsh_pairs = {(a, b) for (a, b, c) in lsh_sim}
        brute_force_pairs = {(a, b) for (a, b, c) in brute_force_sim}
        intersection_size = '\nSize of intersection between approaches is %s duplicate pairs.' % \
                            len(lsh_pairs.intersection(brute_force_pairs))
        report.write(intersection_size + '\n')

        report.write(TRAILER)

    # print report
    print TRAILER
    with open(DEST_REPORT, 'r') as report:
        print report.read()
