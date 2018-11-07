
import twitterCredentials

import tweepy
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
import requests
import json

from pprint import pprint as pp
import pdb











## CONNECTING TO TWITTER API ###################################################################


auth = OAuthHandler(
    twitterCredentials.CONSUMER_KEY,
    twitterCredentials.CONSUMER_SECRET
    )

auth.set_access_token(
    twitterCredentials.ACCESS_TOKEN,
    twitterCredentials.ACCESS_TOKEN_SECRET
    )

twitter_api = tweepy.API(auth)



MATCH_HASHTAG = '#icanhazpd'





## CHECKING DOI WITHIN TWEETS ##################################################################


def check_tweet(tweet):
    print("Checking Tweet...")
    print(tweet)
    print()

    # Self explanatory
    doi_index = tweet.lower().find("doi:")

    response = {
        "correct_form": False,
        "doi": None,
        "reason": None
    }

    # making sure that 'DOI:' is included in the tweet
    if doi_index < 0:
        response['reason'] = '"DOI:" not in Tweet'
        return response

    # CONSOLE LOG
    print(doi_index)

    string_after_doi = tweet[doi_index:]
    # CONSOLE LOG
    print(string_after_doi)

    ignore, doi_string = string_after_doi.split(":")
    # CONSOLE LOG
    print(doi_string)

    doi_string_stripped = doi_string.strip()
    # CONSOLE LOG
    print(doi_string_stripped)

    doi, *anything_after_doi = doi_string_stripped.split()

    response['doi'] = doi

    # Validating DOI format
    if not doi.startswith("10."):
        response['reason'] = "Improper DOI"
        return response

    response['correct_form'] = True

    return response




## EXTRACTING AND PROCESSING DATA ##############################################################


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
        is_reply_tweet = tweet_detials['in_reply_to_user_id']


        # Checking the tweet format befor processing the request
        checked_tweet = check_tweet(tweet)

        if checked_tweet["correct_form"]:
            print("Tweet is formed correctly")

            #Extracting the DOI from the tweet
            tweeted_doi = checked_tweet['doi']

            # Connecting to Unpaywall API and passing the extracted DOI
            # in order to find a match
            response = requests.get(
                f'http://api.unpaywall.org/{tweeted_doi}?email=chrispyprogrammer@gmail.com'
                )

            # To handle cases where the DOI is not found or misspelled
            if response.reason == 'NOT FOUND':
                print(f"Could not find DOI: {tweeted_doi} in Database")

                not_found_message = (

                f"@{user_to_tweet_to} I'm a bot who uses the @unpaywall API to look for"\
                " free, legal full text documents. I didn't found anything in the data base"\
                f" corresponding to the DOI you provided --> {tweeted_doi}"

                    )

                twitter_api.update_status(not_found_message, in_reply_to_status_id = tweet_id)
                print("")

            else:

                json_data = response.json()

                #CONSOLE LOG
                print(f"Successfully retrieved PDF for DOI: {tweeted_doi}")

                # Extracting the link to the document
                free_fulltext_url = json_data['results'][0]['free_fulltext_url']

                my_reply = (

                f"@{user_to_tweet_to} I'm a bot who uses the @unpaywall API to look for"\
                " free, legal full text documents. I found a free copy of what you requested"\
                f" here: {free_fulltext_url}"

                )

                # Tweeting the result to the person who submited the request
                twitter_api.update_status(my_reply, in_reply_to_status_id = tweet_id)





## HANDLING WRONG TWEET FORMAT #################################################################


        else:
            if is_reply_tweet:

                # CONSOLE LOG
                print("This is a reply tweet")

                return True


            print(f"Tweet is formatted incorrectly")
            print(f"REASON: {checked_tweet['reason']}")
            print(checked_tweet['doi'])

            wrong_format_message = (

            f"@{user_to_tweet_to} I'm a bot who uses the @unpaywall API to look for"\
            " free, legal full text documents. I can find what you're looking for "\
            " if you add a DOI like this: 'DOI:10.9999/example1234' (remember to include"\
            " our hashtag too)"

                )

            twitter_api.update_status(wrong_format_message, in_reply_to_status_id = tweet_id)

        return True


    def on_error(self, status):
        print(status)




## TRACKING THE HASHTAG #######################################################################


if __name__ == '__main__':

    # Self explanatory
    listener = HashtagListner()
    stream = Stream(auth, listener)

    # To filter Twitter Streams in order to get data by specific keywords
    stream.filter(track=[MATCH_HASHTAG])


