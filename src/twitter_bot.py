
'''
TASK:

* login for twinter api

* stream and listen to a specific hashtag

* if "#icanhazpdf" is find, call Unpaywall API and look for the
  requested PDF

* Tweet a reply with the PDF url

'''

import twitterCredentials

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import requests



## THIS PART NEED TO BE REVIEWED ######################################################


# This class streams and processing live tweets.
class HashtagListner(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':

    # This handles Twitter authetification and the connection to Twitter
    # streaming API all these keys are in twitterCredentials.py file.
    listener = HashtagListner()

    auth = OAuthHandler(
        twitterCredentials.CONSUMER_KEY,
        twitterCredentials.CONSUMER_SECRET
        )

    auth.set_access_token(
        twitterCredentials.ACCESS_TOKEN,
        twitterCredentials.ACCESS_TOKEN_SECRET
        )

    stream = Stream(auth, listener)

    # To filter Twitter Streams in order to get data by specific keywords
    stream.filter(track=['#icanhazpdf'])


#######################################################################################


# CONNECTING TO UNPAYWALL API



#response = requests.get('api.unpaywall.org/my/request?email=chrispyprogrammer@gmail.com')






