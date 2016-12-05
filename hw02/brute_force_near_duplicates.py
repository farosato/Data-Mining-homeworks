"""
Module containing brute force near duplicates computation.
It is useful to create a .pickle object representing the set.
"""
import pickle
import time
from near_duplicates import SRC_BRUTE_FORCE_REPORT as DEST_REPORT
from near_duplicates import SRC_BRUTE_FORCE_SIM as DEST_SIM
from near_duplicates import SEPARATOR
from near_duplicates import TRAILER
from near_duplicates import brute_force_near_duplicates
from near_duplicates import create_documents_shingles


if __name__ == "__main__":
    docs_shingles = create_documents_shingles()

    print '\n', '#'*SEPARATOR, '\nPerforming brute force approach...'
    start_time = time.time()
    brute_force_sim = brute_force_near_duplicates(docs_shingles)
    tot_time = time.time() - start_time

    # Pickle results
    with open(DEST_SIM, 'wb') as data_dump:
        pickle.dump(brute_force_sim, data_dump)

    # print report
    with open(DEST_REPORT, 'w') as report:
        duplicates_num = 'Brute force approach found %s near duplicate pairs.' % len(brute_force_sim)
        report.write(duplicates_num + '\n')
        print duplicates_num

        running_time = 'Brute force approach took  %s seconds.' % tot_time
        report.write(running_time + '\n')
        print running_time

        report.write('\n')
        print '\n'

        for i in brute_force_sim:
            row = '%s <-> %s \tsim = %f' % ('{0: <5}'.format(i[0]), '{0: <5}'.format(i[1]), i[2])
            report.write(row + '\n')
            print row

        report.write(TRAILER)
