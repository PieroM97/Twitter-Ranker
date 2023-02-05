import tweepy
import werkzeug.exceptions
import app.main.service.helper_service as helper


def config_api():
    # Read the config file

    keys = helper.load_keys()

    # Read the values
    api_key = keys["api_key"]
    api_key_secret = keys["api_key_secret"]
    access_token = keys["access_token"]
    access_token_secret = keys["access_token_secret"]

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    return api

def initializate_service():
    api = config_api()
    tweets = api.user_timeline(scren_name = "potus", count = 1, tweet_mode ="extended")
    return api, tweets

def tweets_by_user(user_name, number=20):

    api,tweets = initializate_service()

    try:
        tweets = api.user_timeline(screen_name=user_name, count=number, tweet_mode='extended')
    except:
        raise werkzeug.exceptions.NotFound

    return tweets


def tweets_object_to_list(tweets):
    data = []

    for tweet in tweets:
        data.append(tweet.full_text)

    return data



