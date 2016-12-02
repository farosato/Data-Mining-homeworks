""" Module containing hashing functionalities. """
import hashlib


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


def lsh(docs_hashes):
    """
    Given a collection of minwise hash signatures of a set of documents,
    find all the documents pairs that are near each other.
    """
    # TODO implement this once miwise_hashing() is implemented
    pass


if __name__ == "__main__":
    # example of usage for hash_family()
    # hash_function = hash_family(2)
    # print hash_function('hello')

    pass
