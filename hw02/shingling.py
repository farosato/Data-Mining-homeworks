""" Module containing shingling functionalities. """
import hashing


HASH_ID = 2


def shingle(doc, k):
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
