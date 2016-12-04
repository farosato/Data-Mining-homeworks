"""
Module containing brute force near duplicates computation.
It is useful to create a .pickle object representing the set.
"""
import os
import pickle
import time
from near_duplicates import SRC_BRUTE_FORCE as DEST_DUPL
from near_duplicates import SEPARATOR
from near_duplicates import brute_force_near_duplicates
from near_duplicates import create_documents_shingles


DEST_REPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.txt')


if __name__ == "__main__":
    docs_shingles = create_documents_shingles()

    print '\n', '#'*SEPARATOR, '\nPerforming brute force approach...'
    start_time = time.time()
    brute_force = brute_force_near_duplicates(docs_shingles)

    with open(DEST_REPORT, 'w') as report:
        report.write('Brute force approach found %s near duplicates.\n' % len(brute_force))
        print 'Brute force approach found %s near duplicates.' % len(brute_force)

        report.write('Brute force approach took  %s seconds.\n' % (time.time() - start_time))
        print 'Brute force approach took  %s seconds.' % (time.time() - start_time)

        report.write('#'*SEPARATOR)
        report.write('\n')

    # Pickle the near duplicates set
    with open(DEST_DUPL, 'wb') as data_dump:
        pickle.dump(brute_force, data_dump)
