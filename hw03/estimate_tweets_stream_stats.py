from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from twitter_secret_keys import *
import stream_stats_estimation as sse
import json
import time
import os


DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tweets.txt')
QUERY = ['python', 'datamining', 'hashing']


class StatsListener(StreamListener):
    """ Estimate stream frequency moments when a tweet is received. """

    def __init__(self, est_num=None, group_size=None):
        super(StatsListener, self).__init__()
        self.est_num = est_num
        self.group_size = group_size
        if est_num is not None and group_size is not None:
            sse.init(est_num, group_size)

    def on_data(self, data):
        try:
            tweet = json.loads(data)
            tweet_text = str(tweet['text']).strip().replace('\n', ' ')
            with open(DEST, 'a') as dest:
                dest.write(tweet_text + '\n')
                print tweet_text
            if self.est_num is not None and self.group_size is not None:
                print 'F0: %s' % sse.flajolet_martin(tweet_text)
                print 'F2: %s' % sse.alon_matias_szegedy(tweet_text)
            print ''
        except BaseException as e:
            print 'Error on_data: %s' % str(e), '\n'
            time.sleep(1)
        return True

    def on_error(self, status):
        print status
        return True


if __name__ == '__main__':

    EST_NUM = 100
    GROUP_SIZE = 10

    # listener = StatsListener(EST_NUM, GROUP_SIZE)
    listener = StatsListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, listener)
    stream.filter(track=QUERY)
