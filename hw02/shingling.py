""" Module containing shingling functionalities. """
import hashing


def shingle(doc, k):
    """
    Given a document, creates its set of character shingles of some length k.
    """
    if len(doc) <= k:
        shingles = {doc}
    else:
        shingles = {doc[i:i+k] for i in range(0, len(doc)-k+1)}
    return shingles


def hash_shingles(shingle_set):
    """
    Represent the document as the set of the hashes of the shingles,
    for some hash function.
    """
    hash_function = hashing.hash_family()
    return {hash_function(s) for s in shingle_set}


if __name__ == "__main__":
    # example of usage for shingle() and shingle_hash()
    shingles = shingle('a rose is a rose is a rose', 4)
    print shingles
    print hash_shingles(shingles)
