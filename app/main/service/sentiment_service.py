from transformers import AutoTokenizer,AutoModelForSequenceClassification
from transformers import pipeline
import app.main.service.twitter_service as twittos
import app.main.service.helper_service as helper

import re
import json
import requests

MODEL_NAME = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
MODEL_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment-latest"

TWITTER_USERS = ["pontifex", "elonmusk", "realDonaldTrump", "POTUS", "KimKardashian","DalaiLama","a2lean"]

#Only for using the hugginface api
def prepare_request_for_huggingface():
    keys = helper.load_keys()
    API_TOKEN = keys["api_token_huggingface"]
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    return headers

def tweets_with_vote_huggingface(tweets):
    data = []
    tweets_valuation = []
    user_vote = 0
    neutral_tweets_nr = 0

    # Creating a list and using it for the valuation
    tweets_list = twittos.tweets_object_to_list(tweets)

    for tweet in tweets_list:
        valuation = tweet_evaluator_hugginface({"inputs": tweet})[0][0]
        tweets_valuation.append(valuation)


    number_of_tweets = len(tweets_list)

    for i in range(number_of_tweets):
        user = tweets[i].user.screen_name
        text = tweets[i].full_text
        label = tweets_valuation[i]["label"]
        score = tweets_valuation[i]["score"]
        picture = tweets[i].user.profile_image_url

        data.append([user, text, label, score, picture])

        #Recursive function to get the user_vote and the neutral-tweets
        user_vote,neutral_tweets_nr = get_vote(label,user_vote,neutral_tweets_nr)


    if(number_of_tweets!=neutral_tweets_nr):
        user_vote = user_vote / (number_of_tweets - neutral_tweets_nr) * 100
    else:
        user_vote = 50

    return data,user_vote

def tweet_evaluator_hugginface(payload):
    headers = prepare_request_for_huggingface()
    data = json.dumps(payload)
    response = requests.request("POST", MODEL_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


#Only for local preparation of the model
def model_preparation(modelName):
    tokenizer = AutoTokenizer.from_pretrained(modelName)
    model = AutoModelForSequenceClassification.from_pretrained(modelName)

    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def tweets_evaluator(tweets):
    #Preparing the pipeline, using the given model.
    sentimentEvaluator = model_preparation(modelName=f"cardiffnlp/twitter-roberta-base-sentiment-latest")

    valuation = sentimentEvaluator(tweets)

    return valuation

def tweets_with_vote(tweets):
    data = []
    user_vote = 0
    neutral_tweets_nr = 0

    # Creating a list and using it for the valuation
    tweets_list = twittos.tweets_object_to_list(tweets)
    tweets_valuation = tweets_evaluator(tweets_list)

    number_of_tweets = len(tweets_list)

    for i in range(number_of_tweets):
        user = tweets[i].user.screen_name
        text = tweets[i].full_text
        label = tweets_valuation[i]["label"]
        score = tweets_valuation[i]["score"]
        picture = tweets[i].user.profile_image_url

        data.append([user, text, label, score, picture])

        #Recursive function to get the user_vote and the neutral-tweets
        user_vote,neutral_tweets_nr = get_vote(label,user_vote,neutral_tweets_nr)


    if(number_of_tweets!=neutral_tweets_nr):
        user_vote = user_vote / (number_of_tweets - neutral_tweets_nr) * 100
    else:
        user_vote = 50

    return data,user_vote


#Commons methods

def get_vote(label,user_vote,neutral_tweets_nr):
    user_vote = user_vote
    neutral_tweets_nr = neutral_tweets_nr

    if label == "positive":
        user_vote = user_vote + 1
    elif label == "neutral":
        neutral_tweets_nr = neutral_tweets_nr + 1

    return user_vote,neutral_tweets_nr

def get_user_score(user_name="pontifex",number = 20,type = "local",debug_mode="off"):

    #Getting twitter user tweets
    tweets = twittos.tweets_by_user(user_name,number)

    #Calculate votes for each tweet

    if type == "local":
      data, final_vote = tweets_with_vote(tweets)
    else:
      data, final_vote = tweets_with_vote_huggingface(tweets)

    #Only for debugging:
    if debug_mode == "on":
        for row in data:
            print(row)

    return {
        "img_url":re.sub("normal","400x400",data[0][4]),
        "answer":data[0][0]+" has a score of " + str(int(final_vote))+"/100"
    }

def test(number):
    for user in TWITTER_USERS:
        get_user_score(user,number)


