""" Script for k-th frequency moment exact computation (to be run from compute-stream-stats.sh). """
from sys import argv

if __name__ == '__main__':
    K = int(argv[1])    # frequency moment order
    SRC = argv[2]       # .txt file containing items frequencies

    with open(SRC, 'r') as src:
        result, line = 0, src.readline()
        while line != '':
            freq = line.strip().split(' ')[0]
            result += int(freq)**K
            line = src.readline()
    print 'F%d: %d' % (K, result)
