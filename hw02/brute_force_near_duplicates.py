"""
Module containing brute force near duplicates computation.
It is useful to create a .pickle object representing the set.
"""
import os
import pickle
import time
from near_duplicates import SRC_BRUTE_FORCE_DUPL as DEST_DUPL
from near_duplicates import SRC_BRUTE_FORCE_SIM as DEST_SIM
from near_duplicates import SEPARATOR
from near_duplicates import brute_force_near_duplicates
from near_duplicates import create_documents_shingles


DEST_REPORT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results.txt')
TRAILER = '\n' + '#'*SEPARATOR + '\n'


if __name__ == "__main__":
    docs_shingles = create_documents_shingles()

    print '\n', '#'*SEPARATOR, '\nPerforming brute force approach...'
    start_time = time.time()
    brute_force, similarities = brute_force_near_duplicates(docs_shingles)

    with open(DEST_REPORT, 'w') as report:
        duplicates_num = 'Brute force approach found %s near duplicates.' % len(brute_force)
        report.write(duplicates_num + '\n')
        print duplicates_num

        running_time = 'Brute force approach took  %s seconds.' % (time.time() - start_time)
        report.write(running_time + '\n')
        print running_time

        report.write('\n')
        print '\n'

        for i in similarities:
            row = '%d -> %d\t\tsim = %s' % (i[0], i[1], str(i[2]))
            report.write(row + '\n')
            print row

        report.write(TRAILER)

    # Pickle the near duplicates set
    with open(DEST_DUPL, 'wb') as data_dump:
        pickle.dump(brute_force, data_dump)

    with open(DEST_SIM, 'wb') as data_dump:
        pickle.dump(similarities, data_dump)
