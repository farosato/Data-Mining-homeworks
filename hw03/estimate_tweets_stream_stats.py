from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_secret_keys import *
from freq_moments_estimation import FreqMomentsEstimator
import json
import time
import os

DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tweets.txt')
QUERY = ['python', 'datamining', 'hashing']
EST_NUM = 100
GROUP_SIZE = 10


class StatsListener(StreamListener):
    """ Estimate stream frequency moments when a tweet is received. """

    def __init__(self, est_num=None, group_size=None, progress=False):
        super(StatsListener, self).__init__()
        self.est_num = est_num
        self.group_size = group_size
        self.progress = progress
        if est_num is not None and group_size is not None:
            self.fme = FreqMomentsEstimator(est_num, group_size)

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            tweet_text = str(tweet['text']).strip().replace('\n', ' ')
            with open(DEST, 'a') as dest:
                dest.write(tweet_text + '\n')
                print tweet_text
            if self.est_num is not None and self.group_size is not None:
                self.fme.flajolet_martin(tweet_text)
                self.fme.alon_matias_szegedy(tweet_text)
                if self.progress:
                    print 'F0: %s' % self.fme.fm_estimate()
                    print 'F2: %s' % self.fme.ams_estimate()
            print ''
        except BaseException as e:
            print 'Error on_data: %s' % str(e), '\n'
            time.sleep(1)
        return True

    def on_error(self, status):
        print status
        return True


if __name__ == '__main__':

    listener = StatsListener()
    # listener = StatsListener(EST_NUM, GROUP_SIZE, True)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=QUERY)
