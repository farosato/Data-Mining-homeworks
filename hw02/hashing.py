""" Module containing hashing functionalities. """
from __future__ import division
import hashlib
import random


NUM_HASH = 10               # n = br
JACCARD_THRESHOLD = 0.8     # t = (1/b)^(1/r)
BANDS = 2                   # b
ROWS_PER_BAND = 5           # r

MAX_HASH_ID_LENGTH = 20                     # max num of decimal digits for hash member id
MAX_HASH_ID = 10**MAX_HASH_ID_LENGTH - 1    # max hash member id
DEFAULT_HASH_ID = 2
DEFAULT_HASH_SIZE = 10


def hash_family(i=DEFAULT_HASH_ID, hash_size=DEFAULT_HASH_SIZE):
    """
    Implement a family of hash functions. It hashes strings and
    takes an integer to define the member of the family.
    Return a hash function parametrized by i.

    :param i: hash family member id
    :param hash_size: how many bytes we want back
    """
    salt = str(i).zfill(MAX_HASH_ID_LENGTH)[-MAX_HASH_ID_LENGTH:]

    def hash_member(x):
        return hashlib.sha1(x + salt).digest()[-hash_size:]
    return hash_member


def minwise_hashing(sets):
    """
    Given a collection of sets of objects (e.g., strings, or numbers),
    creates a minwise hashing based signature for each set.
    """
    random_hash_ids = random.sample(xrange(0, MAX_HASH_ID), NUM_HASH)  # xrange to avoid BIG static list
    hash_functions = [hash_family(hid) for hid in random_hash_ids]

    signatures = []
    for s in sets:
        # The resulting minhash signature for this document.
        signature = []

        """
        MinHash signatures are made of a numbers of components equal to NUM_HASH.
        Correspondingly, it is also the number of random hash functions that we will need
        in order to calculate the MinHash signatures.
        """
        for hash_func in hash_functions:
            # For each of the shingles actually in the document, calculate its hash code
            # using the hash function.

            # initialize min_hash
            shingle = s.pop()
            min_hash = hash_func(shingle)
            s.add(shingle)

            for shingle in s:
                hash_code = hash_func(shingle)
                # Track the lowest hash code seen (lexicographic).
                if hash_code < min_hash:
                    min_hash = hash_code

            # Add the smallest hash code value as the i-th component of the signature.
            signature.append(min_hash)

        # Store the MinHash signature for this document.
        signatures.append(''.join(signature))
    return signatures


def lsh(docs_hashes):
    """
    Given a collection of minwise hash signatures of a set of documents,
    find all the documents pairs that are near each other.
    """
    if NUM_HASH != BANDS * ROWS_PER_BAND:
        raise ValueError('n = br constraint does not hold.')

    similarities = []

    """
    For each band, append to hash tables list a sublist composed by an hash function
    (in case we would apply a different one to each band) and a dictionary
    (collection of buckets) such that an entry is (hash -> list of doc_ids).
    """
    hash_tables = []
    for i in range(BANDS):
        hash_tables.append([hash_family(DEFAULT_HASH_ID, NUM_HASH), {}])

    """
    For each band, construct candidate pairs. If two signatures are equals in at least
    one band, then they are a candidate pair.
    """
    for i, h in enumerate(docs_hashes):
        for j in range(BANDS):
            start = j*ROWS_PER_BAND*DEFAULT_HASH_SIZE
            sub_h = hash_tables[j][0](h[start:start+ROWS_PER_BAND*DEFAULT_HASH_SIZE])
            try:
                hash_tables[j][1][sub_h].append(i)
            except KeyError:  # hash is not in dictionary keys
                hash_tables[j][1][sub_h] = [i]

    """
    For each candidate pair, check whether the fraction of bands in which
    they agree is at least t. If it is so, then they are near duplicates.
    """
    for t in hash_tables:
        for _, candidates in t[1].iteritems():
            cand_size = len(candidates)
            for i in range(0, cand_size):
                for j in range(i + 1, cand_size):
                    first, second = candidates[i], candidates[j]
                    similarity = _signatures_bands_similarity(docs_hashes[first], docs_hashes[second])
                    if similarity >= JACCARD_THRESHOLD:
                        similarities.append((first, second, similarity))
    # filter out duplicate pairs (i.e. a,b = b,a)
    return set((a, b, c) if a <= b else (b, a, c) for a, b, c in similarities)


def _signatures_bands_similarity(first_sign, second_sign):
    """
    Evaluate fraction of bands in which signatures agree.
    """
    agreed = 0
    for j in range(BANDS):
        start = j*ROWS_PER_BAND*DEFAULT_HASH_SIZE
        end = start + ROWS_PER_BAND
        if first_sign[start:end] == second_sign[start:end]:
            agreed += 1
    return agreed / BANDS
