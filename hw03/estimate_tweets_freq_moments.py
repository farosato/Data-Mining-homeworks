from freq_moments_estimation import FreqMomentsEstimator
import estimate_access_log_freq_moments as eal
import os

TWEETS_SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tweets.txt')
TWEETS_RES = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tweets_results.txt')
EST_NUM = 100
GROUP_SIZE = 10


if __name__ == '__main__':
    # initialize data structures
    fme = FreqMomentsEstimator(EST_NUM, GROUP_SIZE)
    act_f0, act_f2 = eal.get_actual_values(TWEETS_RES)

    # compute estimates
    eal.est_0th_fm(fme, TWEETS_SRC, act_f0)
    eal.est_2nd_fm(fme, TWEETS_SRC, act_f2)
