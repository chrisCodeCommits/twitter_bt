
import twitterCredentials

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import requests
import json





## CONNECTING TO TWITTER API ##########################################################


auth = OAuthHandler(
    twitterCredentials.CONSUMER_KEY,
    twitterCredentials.CONSUMER_SECRET
    )

auth.set_access_token(
    twitterCredentials.ACCESS_TOKEN,
    twitterCredentials.ACCESS_TOKEN_SECRET
    )

twitter_api = tweepy.API(auth)




## EXTRACTING AND PROCESSING DATA #####################################################


# This class streams and processing live tweets.
class HashtagListner(StreamListener):


    def on_data(self, data):

        # These lines convert gathered data to a python dictionary
        # in order to allow an easy extraction of any piece of info
        # about the tweet! Notice on the second line, I'm using
        # the key 'text' because that is where the tweet is located.
        tweet_detials    = json.loads(data)
        tweet            = tweet_detials['text']
        tweet_id         = tweet_detials['id']
        user_to_tweet_to = tweet_detials['user']['screen_name']


        #Extracting the DOI from tweets
        tweeted_doi = tweet.split(" ")[1]

        # Connecting to Unpaywall API and passing the extracted DOI
        # in order to find a match
        response = requests.get(
            f'http://api.unpaywall.org/{tweeted_doi}?email=chrispyprogrammer@gmail.com'
            )

        json_data = response.json()

        # Extracting the link to the document
        free_fulltext_url = json_data['results'][0]['free_fulltext_url']


        my_reply = (

        f"@{user_to_tweet_to} I'm a bot who uses the @unpaywall API to look for"\
        "free, legal full text documents. I found a free copy of what you requested"\
        f"here: {free_fulltext_url}"

        )


        # Tweeting the result to the person who submited the request
        twitter_api.update_status(my_reply, in_reply_to_status_id = tweet_id)

        print('code executed')

        return True


    def on_error(self, status):
        print(status)




## TRACKING THE HASHTAG ###############################################################


hashtag = '#tstapp2018twmat'


if __name__ == '__main__':

    # Self explanatory
    listener = HashtagListner()
    stream = Stream(auth, listener)

    # To filter Twitter Streams in order to get data by specific keywords
    # #icanhazpd
    stream.filter(track=[hashtag])






