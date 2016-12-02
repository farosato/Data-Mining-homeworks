"""
Module containing near duplicates computation. Two implementations are provided:
- lsh-based
- brute force approach
"""
from __future__ import division
import hashing
import shingling


JACCARD_THRESHOLD = 0.8


def lsh_near_duplicates():
    """
    Given a collection of minwise hash signatures of a set of documents,
    it finds the all the documents pairs that are near each other.
    The procedure is defined in LRU book as follow:

    1. Pick a value of k and construct from each document the set of k-shingles.
    Optionally, hash the k-shingles to shorter bucket numbers.
    [NOTE: this step is implemented in shingling.py]

    2. Sort the document-shingle pairs to order them by shingle.

    3. Pick a length n for the minhash signatures. Feed the sorted list to the
    algorithm of Section 3.3.5 to compute the minhash signatures for all the
    documents.
    [NOTE: this step is implemented in hashing.minwise_hashing()]

    4. Choose a threshold t that defines how similar documents have to be in
    order for them to be regarded as a desired "similar pair." Pick a number
    of bands b and a number of rows r such that br = n, and the threshold
    t is approximately (1/b)^(1/r). If avoidance of false negatives is important,
    you may wish to select b and r to produce a threshold lower than t; if
    speed is important and you wish to limit false positives, select b and r to
    produce a higher threshold.
    [NOTE: t = 0.8, n = ]

    5. Construct candidate pairs by applying the LSH technique of Section 3.4.1.
    [NOTE: this step is implemented in hashing.lsh()]

    6. Examine each candidate pair's signatures and determine whether the fraction of
    components in which they agree is at least t.

    7. Optionally, if the signatures are sufficiently similar, go to the documents
    themselves and check that they are truly similar, rather than documents
    that, by luck, had similar signatures.
    """
    # TODO implement this once hashing.lsh() is implemented
    # TODO define n (minwise hash signature length)
    pass


def brute_force_near_duplicates(docs_shingles):
    """
    Given the shingles sets of each document in a set, finds the nearest neighbors
    by comparing all the shingle sets with each other.
    """
    neighbors = {}  # doc_id -> list of nearest neighbors doc_ids
    docs = len(docs_shingles)
    for i, s_row in enumerate(docs_shingles):
        for j in range(i, docs):
            if i != j and _jaccard_sim(docs_shingles[i], docs_shingles[j]) >= JACCARD_THRESHOLD:
                try:
                    neighbors[i].append(j)
                except KeyError:  # doc_id is not in dictionary keys
                    neighbors[i] = [j]
                try:
                    neighbors[j].append(i)
                except KeyError:  # doc_id is not in dictionary keys
                    neighbors[j] = [i]
    return neighbors


def _jaccard_sim(a, b):
    """
    Computes Jaccard similarity of the given sets.
    Note that params are required to be Python sets.
    """
    return len(a.intersection(b)) / len(a.union(b))


if __name__ == "__main__":
    # example of usage for brute_force_near_duplicates()
    # docs = ['a rose is', 'a rose is', 'a rose is', 'a rose is', 'a rose is', 'a rose is']
    # docs_shingles = [shingling.shingle_hash(d, 4) for d in docs]
    # for ds in docs_shingles:
    #     print ds
    # for i in brute_force_near_duplicates(docs_shingles).items():
    #     print i

    pass
