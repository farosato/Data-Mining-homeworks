""" Module containing hashing functionalities. """
import hashlib, random, binascii

# This is the number of components in the resulting MinHash signatures.
# Correspondingly, it is also the number of random hash functions that
# we will need in order to calculate the MinHash.
numHashes = 10;


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
    # TODO implement this once miwise_hashing() is implemented
    pass


if __name__ == "__main__":
    # example of usage for hash_family()
    # hash_function = hash_family(2)
    # print hash_function('hello')

    pass
