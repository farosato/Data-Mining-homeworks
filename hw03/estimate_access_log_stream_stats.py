import stream_stats_estimation as sse
import time


# SRC = 'access_log_prep.txt'
SRC = 'access_log_test.txt'


def est_0th_fm(progress=False):
    print '\nEstimating 0-th frequency moment...'
    with open(SRC, 'r') as src:
        start_time = time.time()

        res, line = 0, src.readline()
        while line != '':
            res = sse.flajolet_martin(line)
            if progress:
                print res
            line = src.readline()

        print 'time: %s seconds' % (time.time() - start_time)
        print 'F0:   %s' % res


def est_2nd_fm(progress=False):
    print '\nEstimating 2-nd frequency moment...'
    with open(SRC, 'r') as src:
        start_time = time.time()

        res, line = 0, src.readline()
        while line != '':
            res = sse.alon_matias_szegedy(line)
            if progress:
                print res
            line = src.readline()

        print 'time: %s seconds' % (time.time() - start_time)
        print 'F2:   %s' % res


if __name__ == '__main__':

    EST_NUM = 100
    GROUP_SIZE = 10

    sse.init(EST_NUM, GROUP_SIZE)

    # est_0th_fm()

    est_2nd_fm()
