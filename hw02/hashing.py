""" Module containing hashing functionalities. """
import hashlib


def hash_family(i):
    """
    Implement a family of hash functions. It hashes strings and
    takes an integer to define the member of the family.
    Return a hash function parametrized by i.
    """
    result_size = 8     # how many bytes we want back
    max_length = 20     # how long can our i be (in decimal)
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
    pass


if __name__ == "__main__":
    # example of usage for hash_family()
    hash_function = hash_family(2)
    print hash_function('hello')
