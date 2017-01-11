from __future__ import division
from freq_moments_estimation import FreqMomentsEstimator
import time
import os

ACC_LOG_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_prep.txt')
ACC_LOG_RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_prep_results.txt')
ACC_LOG_SRC_TEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_test.txt')
ACC_LOG_RES_TEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_test_results.txt')
EST_NUM = 100
GROUP_SIZE = 10


def est_0th_fm(freq_moments_est, file_name, actual_value):
    # type: (FreqMomentsEstimator, str, int) -> None
    print '\nEstimating 0-th frequency moment...'
    with open(file_name, 'r') as src:
        start_time = time.time()
        res, line = 0, src.readline()
        while line != '':
            freq_moments_est.flajolet_martin(line)
            line = src.readline()
        print 'time:   %s seconds' % (time.time() - start_time)

        res = freq_moments_est.fm_estimate()
        print 'act F0: %s' % actual_value
        print 'est F0: %s' % res
        errors(res, actual_value)


def est_2nd_fm(freq_moments_est, file_name, actual_value):
    # type: (FreqMomentsEstimator, str, int) -> None
    print '\nEstimating 2-nd frequency moment...'
    with open(file_name, 'r') as src:
        start_time = time.time()
        res, line = 0, src.readline()
        while line != '':
            freq_moments_est.alon_matias_szegedy(line)
            line = src.readline()
        print 'time:   %s seconds' % (time.time() - start_time)

        res = freq_moments_est.ams_estimate()
        print 'act F2: %s' % actual_value
        print 'est F2: %s' % res
        errors(res, actual_value)


def errors(est_value, act_value):
    abs_err = abs(act_value - est_value)
    print 'abs error: %s' % abs_err
    print 'rel error: %s' % (abs_err / act_value)


def get_actual_values(file_name):
    with open(file_name, 'r') as src:
        res = ()
        line = src.readline()
        while line != '':
            res += (int(line.split(':')[1].strip()), )
            line = src.readline()
    return res


if __name__ == '__main__':
    # initialize data structures
    fme = FreqMomentsEstimator(EST_NUM, GROUP_SIZE)
    act_f0, act_f2 = get_actual_values(ACC_LOG_RES_TEST)

    # compute estimates
    est_0th_fm(fme, ACC_LOG_SRC_TEST, act_f0)
    est_2nd_fm(fme, ACC_LOG_SRC_TEST, act_f2)
