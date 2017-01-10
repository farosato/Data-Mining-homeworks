""" Module containing streaming algorithms for frequency moments estimation. """
from __future__ import division
from xxhash import xxh64
import random

MAX_SEED = 18446744073709551615L  # = 2**64-1, since xxh64 accepts only unsigned 64-bit integers as seed


class FreqMomentsEstimator:
    def __init__(self, est_num, group_size):
        self.est_num = est_num              # number of estimates
        self.group_size = group_size        # number of estimates in a group (only for flajolet-martin)
        self.fm_estimates = [0] * est_num   # list of est_num fm independent estimates (i.e. max tail length seen)
        self.ams_estimates = [0] * est_num  # list of est_num ams independent estimates

        # list of est_num random hash function seeds, to perform independent estimates
        self.random_seeds = _pick_random_numbers(est_num, MAX_SEED)

    def flajolet_martin(self, item):
        """
        Update stream 0-th frequency moment independent
        estimates using flajolet-martin algorithm.
        """
        for i, seed in enumerate(self.random_seeds):
            signature = xxh64(item, seed=seed).intdigest()
            new_est = _tail_length(signature)
            if new_est > self.fm_estimates[i]:
                self.fm_estimates[i] = new_est

    def fm_estimate(self):
        """
        Estimate stream 0-th frequency moment applying
        median of the averages technique on independent
        flajolet-martin estimates (i.e. max tail length seen).
        """
        means = []
        for start in range(0, self.est_num, self.group_size):
            end = start + self.group_size
            means.append(_mean(self.fm_estimates[start:end]))
        return int(2 ** _median(means))

    def alon_matias_szegedy(self, item):
        """
        Update stream 2-nd frequency moment independent
        estimates using alon-matias-szegedy algorithm.
        """
        for i, seed in enumerate(self.random_seeds):
            self.ams_estimates[i] += _one_sign(item, seed)

    def ams_estimate(self):
        """
        Estimate stream 2-nd frequency moment computing
        average of independent alon-matias-szegedy
        estimates.
        """
        return int(_mean([x ** 2 for x in self.ams_estimates]))


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
    If hash signature is odd, then return +1 (-1 otherwise).
    """
    return 1 if (xxh64(item, seed=seed).intdigest() & 1) else -1


def _mean(values):
    return sum(values) / max(len(values), 1)


def _median(values):
    values = sorted(values)
    length = len(values)
    middle = length - 1
    return (values[int(length / 2)] + values[int(middle / 2)]) / 2


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
