""" Module containing streaming algorithms for frequency moments estimation. """
from __future__ import division
import __init__
import hw02.hashing as hw_utils
import time
from xxhash import xxh64


MAX_SEED = 18446744073709551615L  # = 2**64-1


fm_random_hashes = []
fm_estimates = []
ams_random_hashes = []
ams_estimates = []


def flajolet_martin(item, est_num, group_size):
    """ Estimate stream 0-th frequency moment. """
    for i, seed in enumerate(fm_random_hashes):
        signature = bin(xxh64(item, seed=seed).intdigest())
        new_est = 2**(_tail_length(signature))
        if new_est > fm_estimates[i]:
            fm_estimates[i] = new_est

    means = []
    for start in range(0, est_num, group_size):
        means.append(_mean(fm_estimates[start:start+group_size]))

    return int(_median(means))


def alon_matias_szegedy(item):
    """ Estimate stream 2-nd frequency moment. """
    for i, seed in enumerate(ams_random_hashes):
        if _one_sign(item, seed):
            ams_estimates[i] += 1
        else:
            ams_estimates[i] -= 1
    return int(_mean([x**2 for x in ams_estimates]))


def _tail_length(bin_sign):
    """
    Compute binary signature 'tail length'.
    Signature is assumed to be big endian.
    """
    tail_length = 0
    for bit in bin_sign[:1:-1]:  # truncate first two chars, iterate from last
        if bit == '1':
            return tail_length
        tail_length += 1
    return tail_length


def _one_sign(item, seed):
    """
    Hash an item to a random value in {-1,+1}.
    If signature is odd, then return True (False otherwise).
    True maps to +1, False maps to -1.
    """
    return True if (xxh64(item, seed=seed).intdigest() & 1) else False


def _mean(values):
    return sum(values) / max(len(values), 1)


def _median(values):
    values = sorted(values)
    length = len(values)
    middle = length - 1
    return (values[int(length/2)] + values[int(middle/2)]) / 2


if __name__ == '__main__':

    EST_NUM = 100
    GROUP_SIZE = 10

    # fm_random_hashes = hw_utils._pick_random_numbers(EST_NUM, MAX_SEED)
    # fm_estimates = [0] * EST_NUM

    ams_random_hashes = hw_utils._pick_random_numbers(EST_NUM, MAX_SEED)
    ams_estimates = [0] * EST_NUM

    with open('access_log_test.txt', 'r') as src:

        # 0-th frequency moment
        # start_time = time.time()
        #
        # line = src.readline()
        # while line != '':
        #     print flajolet_martin(line, EST_NUM, GROUP_SIZE)
        #     line = src.readline()
        #
        # print 'time: %s seconds' % (time.time() - start_time)

        # 2-nd frequency moment
        start_time = time.time()

        line = src.readline()
        while line != '':
            print alon_matias_szegedy(line)
            line = src.readline()

        print 'time: %s seconds' % (time.time() - start_time)
