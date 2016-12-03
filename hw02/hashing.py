""" Module containing hashing functionalities. """
from __future__ import division
import hashlib
import itertools
import random
import binascii


DOCS_MINHASH_SIZE = 8       # n = br
JACCARD_THRESHOLD = 0.8     # t = (1/b)^(1/r)
BANDS = 2                   # b
ROWS_PER_BAND = 4           # r

HASH_ID = 2

"""
This is the number of components in the resulting MinHash signatures.
Correspondingly, it is also the number of random hash functions that
we will need in order to calculate the MinHash.
"""
NUM_HASHES = 10
# Record the maximum shingle ID that we assigned.
max_shingle_id = 2**32-1


def hash_family(i, hash_size, max_length=20):
    """
    Implement a family of hash functions. It hashes strings and
    takes an integer to define the member of the family.
    Return a hash function parametrized by i.

    :param hash_size: how many bytes we want back
    :param max_length: how long can our i be (in decimal)
    """
    salt = str(i).zfill(max_length)[-max_length:]

    def hash_member(x):
        return hashlib.sha1(x + salt).digest()[-hash_size:]
    return hash_member


def minwise_hashing(sets):
    """
    Given a collection of sets of objects (e.g., strings, or numbers), creates
    a minwise hashing based signature for each set.
    """
    random_hash = _pick_random_numbers(NUM_HASHES, max_shingle_id)

    signatures = []
    for s in sets:
        # The resulting minhash signature for this document.
        signature = []
        # For each of the random hash functions...
        for i in range(0, NUM_HASHES):
            # For each of the shingles actually in the document, calculate its hash code
            # using hash function 'i'.

            for shingle in s:
                hash_function = hash_family(random_hash[i],8)
                hash_code = hash_function(shingle)

                if i == 0:
                    min_hash_code=hash_code

                # Track the lowest hash code seen (lexicographic).
                if hash_code < min_hash_code:
                    min_hash_code = hash_code

            # Add the smallest hash code value as component number 'i' of the signature.
            signature.append(min_hash_code)

        # Store the MinHash signature for this document.
        signatures.append(signature)

    return signatures


def lsh(docs_hashes):
    """
    Given a collection of minwise hash signatures of a set of documents,
    find all the documents pairs that are near each other.
    """
    if DOCS_MINHASH_SIZE != BANDS*ROWS_PER_BAND:
        raise ValueError('n = br constraint does not hold.')

    near_duplicates = set()

    """
    For each band, append to hash tables list a sublist composed by an hash function
    (in case we would apply a different one to each band) and a dictionary
    (collection of buckets) such that an entry is (hash -> list of doc_ids).
    """
    hash_tables = []
    for i in range(BANDS):
        hash_tables.append([hash_family(HASH_ID, DOCS_MINHASH_SIZE), {}])

    """ For each band, construct candidate pairs """
    for i, h in enumerate(docs_hashes):
        for j in range(BANDS):
            start = j*BANDS
            sub_h = hash_tables[j][0](h[start:start+ROWS_PER_BAND])
            try:
                hash_tables[j][1][sub_h].append(i)
            except KeyError:  # hash is not in dictionary keys
                hash_tables[j][1][sub_h] = [i]

    """
    For each candidate pair, check whether the fraction of components in which
    they agree is at least t. If it is so, then they are near duplicates.
    """
    for t in hash_tables:
        for _, candidates in t[1].iteritems():
            for pair in itertools.product(candidates, repeat=2):
                first, second = pair[0], pair[1]
                if first != second:
                    if _signatures_bands_similarity(docs_hashes[first], docs_hashes[second]) >= JACCARD_THRESHOLD:
                        near_duplicates.add(first)
                        near_duplicates.add(second)

    return near_duplicates


def _pick_random_numbers(k, max_num):
    """
    Create a list of k random values in [0, max_num].
    """
    rand_list = []

    while k > 0:
        # Get a random shingle ID.
        rand_index = random.randint(0, max_num)

        # Ensure that each random number is unique.
        while rand_index in rand_list:
            rand_index = random.randint(0, max_num)

        # Add the random number to the list.
        rand_list.append(rand_index)
        k -= 1

    return rand_list


def _signatures_bands_similarity(first_sign, second_sign):
    agreed = 0
    for j in range(BANDS):
        start = j * BANDS
        end = start + ROWS_PER_BAND
        if first_sign[start:end] == second_sign[start:end]:
            agreed += 1
    return agreed / BANDS


if __name__ == "__main__":
    # example of usage for hash_family()
    # hash_function = hash_family(2)
    # print hash_function('hello')

    pass
