""" Module containing shingling functionalities. """
import hashing


HASH_ID = 2


def shingle(doc, k):
    """
    Given a document, creates its set of character shingles of some length k.
    Then represent the document as the set of the hashes of the shingles,
    for some hash function.
    """
    shingles = []
    hash_function = hashing.hash_family(HASH_ID)
    if len(doc) <= k:
        shingles.append(hash_function(doc))
    else:
        shingles = [hash_function(doc[i:i+k]) for i in range(0, len(doc)-k+1)]
    return shingles


if __name__ == "__main__":
    # example of usage for shingle()
    print shingle('a rose is a rose is a rose', 4)
    print shingle('a ros', 4)
    print shingle('a ro', 4)
