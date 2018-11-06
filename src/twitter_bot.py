
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
import json






## CONNECTING TO TWITTER API AND GETTING THE NEEDED DATA ##############################


# This class streams and processing live tweets.
class HashtagListner(StreamListener):


    def on_data(self, data):

        # These lines convert gathered data to a python dictionary
        # in order to allow an easy extraction of any piece of info
        # about the tweet! Notice on the second line, I'm using
        # the key 'text' because that is where the tweet is located.
        tweet_detials   = json.loads(data)
        tweet           = tweet_detials['text']

        #Extracting the DOI from tweets
        tweeted_doi = tweet.split(" ")[1]

        # Connecting to Unpaywall API and passing the extracted DOI
        # in order to find a match
        response = requests.get(
            f'http://api.unpaywall.org/{tweeted_doi}?email=chrispyprogrammer@gmail.com'
            )

        print(type(response))

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
    # #icanhazpd
    stream.filter(track=['#tstapp2018twmat'])






