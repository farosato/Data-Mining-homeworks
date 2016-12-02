""" Module containing hashing functionalities. """
from __future__ import division
import hashlib
import itertools
import random
import binascii

# This is the number of components in the resulting MinHash signatures.
# Correspondingly, it is also the number of random hash functions that
# we will need in order to calculate the MinHash.
numHashes = 10;


DOCS_MINHASH_SIZE = 8       # n = br
JACCARD_THRESHOLD = 0.8     # t = (1/b)^(1/r)
BANDS = 2                   # b
ROWS_PER_BAND = 4           # r

HASH_ID = 2


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


def pickRandomCoeffs(k, maxN):
  # Create a list of 'k' random values.
  randList = []

  while k > 0:
    # Get a random shingle ID.
    randIndex = random.randint(0, maxN)

    # Ensure that each random number is unique.
    while randIndex in randList:
      randIndex = random.randint(0, maxN)

    # Add the random number to the list.
    randList.append(randIndex)
    k = k - 1

  return randList


def minwise_hashing(sets):
    """
    Given a collection of sets of objects (e.g., strings, or numbers), creates
    a minwise hashing based signature for each set.
    """
    # Record the maximum shingle ID that we assigned.
    maxShingleID = 2**32-1

    # We need the next largest prime number above 'maxShingleID'.
    # I looked this value up here:
    # http://compoasso.free.fr/primelistweb/page/prime/liste_online_en.php
    nextPrime = 4294967311

    coeffA = pickRandomCoeffs(numHashes,maxShingleID)
    coeffB = pickRandomCoeffs(numHashes,maxShingleID)

    signatures = []
    for sset in sets:
        print sset
        # The resulting minhash signature for this document.
        signature = []
        # For each of the random hash functions...
        for i in range(0, numHashes):
            # For each of the shingles actually in the document, calculate its hash code
            # using hash function 'i'.

            # Track the lowest hash ID seen. Initialize 'minHashCode' to be greater than
            # the maximum possible value output by the hash.
            minHashCode = nextPrime + 1
            nums=0
            # For each shingle in the document...
            for shingleID in sset:
                #Convert the shingle to integer to process his hashCode
                nums=nums+1
                shingleCode = binascii.crc32(shingleID) & 0xffffffff
                # Evaluate the hash function.
                hashCode = (coeffA[i] * shingleCode + coeffB[i]) % nextPrime

                # Track the lowest hash code seen.
                if hashCode < minHashCode:
                    minHashCode = hashCode
                # Add the smallest hash code value as component number 'i' of the signature.
            signature.append(minHashCode)

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
