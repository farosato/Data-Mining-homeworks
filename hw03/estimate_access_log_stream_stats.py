from __future__ import division
import stream_stats_estimation as sse
import time
import os


# ACC_LOG_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_prep.txt')
# ACC_LOG_RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_prep_results.txt')
ACC_LOG_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_test.txt')
ACC_LOG_RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'access_log_test_results.txt')
EST_NUM = 10000
GROUP_SIZE = 100


def est_0th_fm(in_file, actual_value, progress=False):
    print '\nEstimating 0-th frequency moment...'
    with open(in_file, 'r') as src:
        start_time = time.time()

        res, line = 0, src.readline()
        while line != '':
            res = sse.flajolet_martin(line)
            if progress:
                print res
            line = src.readline()

        print 'time:   %s seconds' % (time.time() - start_time)
        print 'act F0: %s' % actual_value
        print 'est F0: %s' % res
        errors(res, actual_value)


def est_2nd_fm(in_file, actual_value, progress=False):
    print '\nEstimating 2-nd frequency moment...'
    with open(in_file, 'r') as src:
        start_time = time.time()

        res, line = 0, src.readline()
        while line != '':
            res = sse.alon_matias_szegedy(line)
            if progress:
                print res
            line = src.readline()

        print 'time:   %s seconds' % (time.time() - start_time)
        print 'act F2: %s' % actual_value
        print 'est F2: %s' % res
        errors(res, actual_value)


def errors(est_value, act_value):
    abs_err = abs(act_value - est_value)
    print 'abs error: %s' % abs_err
    print 'rel error: %s' % (abs_err / act_value)


def get_actual_values(in_file):
    with open(in_file, 'r') as src:
        res = ()
        line = src.readline()
        while line != '':
            res += (int(line.split(':')[1].strip()), )
            line = src.readline()
    return res


if __name__ == '__main__':

    sse.init(EST_NUM, GROUP_SIZE)

    act_f0, act_f2 = get_actual_values(ACC_LOG_RES)

    est_0th_fm(ACC_LOG_SRC, act_f0)

    # est_2nd_fm(ACC_LOG_SRC, act_f2)
