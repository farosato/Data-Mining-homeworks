""" Module containing hashing functionalities. """
from __future__ import division
import hashlib


JACCARD_THRESHOLD = 0.8


def hash_family(i, result_size=8, max_length=20):
    """
    Implement a family of hash functions. It hashes strings and
    takes an integer to define the member of the family.
    Return a hash function parametrized by i.

    :param result_size: how many bytes we want back
    :param max_length: how long can our i be (in decimal)
    """
    salt = str(i).zfill(max_length)[-max_length:]

    def hash_member(x):
        return hashlib.sha1(x + salt).digest()[-result_size:]
    return hash_member


def minwise_hashing(sets):
    """
    Given a collection of sets of objects (e.g., strings, or numbers), creates
    a minwise hashing based signature for each set.
    """
    pass


def lsh_minwise(docs_hashes):
    """
    Given a collection of minwise hash signatures of a set of documents,
    find all the documents pairs that are near each other.
    """
    # TODO implement this once miwise_hashing() is implemented
    pass


def lsh_shingles(docs_shingles):
    """
    Given the shingles sets of each document in a set, finds the nearest neighbors
    by comparing all the shingle sets with each other.
    """
    neighbors = {}  # doc_id -> list of nearest neighbors doc_ids
    docs = len(docs_shingles)
    for i, s_row in enumerate(docs_shingles):
        for j in range(i, docs):
            if i != j and _jaccard(docs_shingles[i], docs_shingles[j]) >= JACCARD_THRESHOLD:
                try:
                    neighbors[i].append(j)
                except KeyError:  # doc_id is not in dictionary keys
                    neighbors[i] = [j]
                try:
                    neighbors[j].append(i)
                except KeyError:  # doc_id is not in dictionary keys
                    neighbors[j] = [i]
    return neighbors


def _jaccard(a, b):
    """
    Computes Jaccard similarity of the given sets.
    Note that params are required to be Python sets.
    """
    return len(a.intersection(b)) / len(a.union(b))


if __name__ == "__main__":
    # example of usage for hash_family()
    # hash_function = hash_family(2)
    # print hash_function('hello')

    # example of usage for lsh_shingles()
    # import shingling
    # docs = ['a rose is', 'a rose is', 'a rose is', 'a rose is', 'a rose is', 'a rose is']
    # docs_shingles = [shingling.shingle_hash(d, 4) for d in docs]
    # for ds in docs_shingles:
    #     print ds
    # for i in lsh_shingles(docs_shingles).items():
    #     print i

    pass
