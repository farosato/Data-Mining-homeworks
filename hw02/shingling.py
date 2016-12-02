""" Module containing shingling functionalities. """
import hashing


def shingle(doc, k):
    """
    Given a document, creates its set of character shingles of some length k.
    """
    # TODO check if applying tokenization first is preferable in our application
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
    hash_function = hashing.hash_family(hashing.HASH_ID, hashing.DOCS_MINHASH_SIZE)
    return set([hash_function(s) for s in shingle(doc, k)])


if __name__ == "__main__":
    # example of usage for shingle() and shingle_hash()
    print shingle('a rose is a rose is a rose', 4)
    print shingle_hash('a rose is a rose is a rose', 4)
    print shingle('a ros', 4)
    print shingle_hash('a ros', 4)
    print shingle('a ro', 4)
    print shingle_hash('a ro', 4)
