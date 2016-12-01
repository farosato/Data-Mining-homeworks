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


if __name__ == "__main__":
    # example of usage for hash_family()
    hash_function = hash_family(2)
    print hash_function('hello')
