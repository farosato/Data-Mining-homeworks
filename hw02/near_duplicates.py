from __future__ import division


JACCARD_THRESHOLD = 0.8


def lsh_near_duplicates():
    """
    Given a collection of minwise hash signatures of a set of documents,
    it finds the all the documents pairs that are near each other.
    """
    # TODO implement this once hashing.lsh() is implemented
    pass


def brute_force_near_duplicates(docs_shingles):
    """
    Given the shingles sets of each document in a set, finds the nearest neighbors
    by comparing all the shingle sets with each other.
    """
    neighbors = {}  # doc_id -> list of nearest neighbors doc_ids
    docs = len(docs_shingles)
    for i, s_row in enumerate(docs_shingles):
        for j in range(i, docs):
            if i != j and _jaccard_sim(docs_shingles[i], docs_shingles[j]) >= JACCARD_THRESHOLD:
                try:
                    neighbors[i].append(j)
                except KeyError:  # doc_id is not in dictionary keys
                    neighbors[i] = [j]
                try:
                    neighbors[j].append(i)
                except KeyError:  # doc_id is not in dictionary keys
                    neighbors[j] = [i]
    return neighbors


def _jaccard_sim(a, b):
    """
    Computes Jaccard similarity of the given sets.
    Note that params are required to be Python sets.
    """
    return len(a.intersection(b)) / len(a.union(b))


if __name__ == "__main__":
    # example of usage for brute_force_near_duplicates()
    # import shingling
    # docs = ['a rose is', 'a rose is', 'a rose is', 'a rose is', 'a rose is', 'a rose is']
    # docs_shingles = [shingling.shingle_hash(d, 4) for d in docs]
    # for ds in docs_shingles:
    #     print ds
    # for i in brute_force_near_duplicates(docs_shingles).items():
    #     print i

    pass
