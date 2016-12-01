""" Module containing shingling functionalities. """
import hashing


HASH_ID = 2


def shingle(doc, k):
    """
    Given a document, creates its set of character shingles of some length k.
    """
    if len(doc) <= k:
        shingles = [doc]
    else:
        shingles = [doc[i:i+k] for i in range(0, len(doc)-k+1)]
    return set(shingles)


def shingle_hash(doc, k):
    """
    Represent the document as the set of the hashes of the shingles,
    for some hash function.
    """
    hash_function = hashing.hash_family(HASH_ID)
    return set([hash_function(s) for s in shingle(doc, k)])


if __name__ == "__main__":
    # example of usage for shingle()
    print shingle('a rose is a rose is a rose', 4)
    print shingle_hash('a rose is a rose is a rose', 4)
    print shingle('a ros', 4)
    print shingle_hash('a ros', 4)
    print shingle('a ro', 4)
    print shingle_hash('a ro', 4)
