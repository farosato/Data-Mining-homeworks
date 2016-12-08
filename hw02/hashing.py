""" Module containing hashing functionalities. """
from __future__ import division
import hashlib
import random


HASHES_PER_SIGNATURE = 100  # n = b * r
JACCARD_THRESHOLD = 0.8     # threshold = (1/b)^(1/r)
BANDS = 20                  # b
ROWS_PER_BAND = 5           # r

MAX_HASH_ID_LENGTH = 20                     # max num of decimal digits for hash member id
MAX_HASH_ID = 10L**MAX_HASH_ID_LENGTH - 1    # max hash member id
DEFAULT_HASH_ID = 2
DEFAULT_HASH_SIZE = 8


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
    # Pick several "independent" hash functions.
    random_hash_ids = random.sample(xrange(0, MAX_HASH_ID), HASHES_PER_SIGNATURE)  # xrange to avoid BIG static list
    hash_functions = [hash_family(hid) for hid in random_hash_ids]

    signatures = []  # signature matrix (HASHES_PER_SIGNATURE x |sets|)
    for s in sets:
        # The resulting minhash signature for this particular document.
        signature = []

        """
        MinHash signatures are made of a numbers of components (minhashes) equal to HASES_PER_SIGNATURE.
        Correspondingly, it is also the number of random hash functions that we will need
        in order to calculate the minhash signatures.
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
                # Track the minimum hash code seen (lexicographic since hashes are strings).
                if hash_code < min_hash:
                    min_hash = hash_code

            # Add the minimum hash code value as the i-th component of the signature.
            signature.append(min_hash)

        # Store the MinHash signature for this document.
        signatures.append(signature)
    return signatures


def lsh(signatures):
    """
    Given a matrix of minwise hash signatures for a set of documents,
    find all the documents pairs that are near each other.
    """
    if HASHES_PER_SIGNATURE != BANDS * ROWS_PER_BAND:
        raise ValueError('n = b * r constraint does not hold.')

    similarities = []

    """
    For each band we have an hash table represented as a dictionary
    where an entry is a (bucket_id -> list of doc_ids) pair.
    """
    hash_function = hash_family()
    bands_hash_tables = []
    for i in range(BANDS):
        bands_hash_tables.append([hash_family(DEFAULT_HASH_ID, HASHES_PER_SIGNATURE), {}])

    """
    For each band, construct candidate pairs. If two signatures are equals in at least
    one band, then they are a candidate pair.
    """
    for doc_id, sig in enumerate(signatures):
        for band_idx in range(BANDS):
            start_row = band_idx * ROWS_PER_BAND
            end_row = start_row + ROWS_PER_BAND
            band = sig[start_row : end_row]
            bucket_idx = bands_hash_tables[band_idx][0](''.join(band))
            try:
                bands_hash_tables[band_idx][1][bucket_idx].append(doc_id)
            except KeyError:  # hash is not in dictionary keys
                bands_hash_tables[band_idx][1][bucket_idx] = [doc_id]


    """
    For each candidate pair, check whether the fraction of signatures in which
    they agree is at least equal to the threshold. If it is so, then they actually are near duplicates.
    """
    for band_struct in bands_hash_tables:
        for _, candidates in band_struct[1].iteritems():
            for c1_idx, c1 in enumerate(candidates):
                for c2 in candidates[c1_idx + 1:]:
                    similarity = _compute_signatures_similarity(signatures[c1], signatures[c2])
                    if similarity >= JACCARD_THRESHOLD:
                        similarities.append((c1, c2, similarity))
    # filter out duplicate pairs (i.e. a,b = b,a) (two candidates could collide in more than one band)
    return set((a, b, s) if a <= b else (b, a, s) for a, b, s in similarities)


def _pick_random_numbers(k, max_num):
    """
    Create a list of k random integer values in [0, max_num].
    Can't use range or xrange in python 2 because of overflow problems with very large ranges.
    """
    if k > max_num:
        raise ValueError('Not enough unique values in the range.')
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

def _compute_signatures_similarity(sig1, sig2):
   """
    Evaluate fraction of minhashes in which signatures agree.
    """
    if len(sig1) != len(sig2) or len(sig1) != HASHES_PER_SIGNATURE:
        raise ValueError('Signatures should both have n components.')

    match = 0
    for minhash1, minhash2 in zip(sig1, sig2):
        if minhash1 == minhash2:
            match += 1
    return match / HASHES_PER_SIGNATURE
