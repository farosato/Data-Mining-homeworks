""" Module containing streaming algorithms for frequency moments estimation. """
from __future__ import division
from xxhash import xxh64
import random


MAX_SEED = 18446744073709551615L  # = 2**64-1


est_num, group_size = 0, 0
fm_random_hashes = []
fm_estimates = []
ams_random_hashes = []
ams_estimates = []


def init(est_num_, group_size_):
    """ Initialize global variables. """
    global est_num, group_size, fm_random_hashes, fm_estimates, ams_random_hashes, ams_estimates

    est_num = est_num_
    group_size = group_size_

    fm_random_hashes = ams_random_hashes = _pick_random_numbers(est_num, MAX_SEED)
    fm_estimates = [0] * est_num
    ams_estimates = [0] * est_num


def flajolet_martin(item):
    """ Estimate stream 0-th frequency moment. """
    for i, seed in enumerate(fm_random_hashes):
        signature = xxh64(item, seed=seed).intdigest()
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


def _tail_length(sign):
    """ Compute binary signature 'tail length'. """
    tail_length = 0
    while sign != 0:
        if sign & 1:  # lsb is 1
            return tail_length
        tail_length += 1
        sign >>= 1
    return len(bin(sign))


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


def _pick_random_numbers(k, max_num):
    """
    Create a list of k random integer values in [0, max_num].
    Can't use range or xrange in python 2 because of overflow
    problems with very large ranges.
    """
    if k > max_num:
        raise ValueError('Not enough unique values in range.')

    rand_list = []

    while k > 0:
        # Get a random number in range.
        rand_index = random.randint(0, max_num)

        # Ensure that each random number is unique.
        while rand_index in rand_list:
            rand_index = random.randint(0, max_num)

        # Add the random number to the list.
        rand_list.append(rand_index)
        k -= 1
    return rand_list
