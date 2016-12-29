""" Script for 2-nd frequency moment exact computation (to be run from compute-stream-stats.sh). """
import sys


if __name__ == '__main__':
    SRC = sys.argv[1]  # .txt file containing items frequencies

    with open(SRC, 'r') as src:

        result, line = 0, src.readline()
        while line != '':
            freq = line.strip().split(' ')[0]
            result += int(freq)**2
            line = src.readline()

    print 'F2: %d' % result
