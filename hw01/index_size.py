import pickle
import time
from pympler import asizeof
from build_index import DEST_OPT

if __name__ == "__main__":
    with open(DEST_OPT,'rb') as pickled_index:
        print 'Loading index...'
        start_time = time.time()
        index = pickle.load(pickled_index)
        print 'Evaluating index size...'
        print "\nInverted Index size is %d bytes." % asizeof.asizeof(index)
        print("\n--- %s seconds ---" % (time.time() - start_time))
