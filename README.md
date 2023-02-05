#Twitter-Ranker: Sentiment Analysis for Twitter Profiles

This project uses sentiment analysis to evaluate the positivity of a Twitter profile based on the last 100 tweets. The evaluation is on a scale from 0 to 100, where 100 represents an extremely positive profile and 0 represents an extremely negative one. The sentiment analysis is performed using a BERT model.

##Configuration

In order to use this project, you will need to create API keys for both Hugging Face and Twitter. The Hugging Face API keys are not mandatory, but are necessary if you wish to run the sentiment analysis model through Hugging Face, rather than locally. The Twitter API keys are required in order to access Twitter data and perform the sentiment analysis.

Once you have obtained your API keys, you will need to add them to the keys.json file in the project directory. The file should look like this:

```
{
    "twitter_api_key": "<your_twitter_api_key>",
    "twitter_api_secret_key": "<your_twitter_api_secret_key>",
    "twitter_access_token": "<your_twitter_access_token>",
    "twitter_access_token_secret": "<your_twitter_access_token_secret>",
    "hugging_face_api_key": "<your_hugging_face_api_key>"
}
```

Make sure to replace <your_hugging_face_api_key>, <your_twitter_api_key>, <your_twitter_api_secret_key>, <your_twitter_access_token>, and <your_twitter_access_token_secret> with your own API keys.


##How to Use

The sentiment analysis of Twitter profiles can be easily accessed through a user-friendly interface. To use the app, simply search for the username of the Twitter user you would like to evaluate. The evaluation result will be displayed on a scale from 0 to 100, where 100 represents an extremely positive profile and 0 represents an extremely negative one.

To connect to the interface, you will need to access localhost on port 5000. The app is built using the Flask framework, which is a lightweight and easy-to-use web framework for Python.

###Running the App

To run the app on your local machine, you will need to have the necessary dependencies installed. These include Flask and the necessary libraries for running the BERT model. Once you have these dependencies installed, you can start the app by running the following command in your terminal:

>$ FLASK_APP=main.py FLASK_ENV=development flask run

This will start a local server on your machine, and you can access the user interface by visiting localhost:5000 in your web browser.

It's possible to create a docker image. Run:
 
>  docker build -t twitter-ranker .    

##Some info about the technologies used here

###Introduction to Sentiment Analysis

Sentiment analysis is a field of natural language processing that focuses on determining the sentiment expressed in a piece of text, such as a tweet. The sentiment can be positive, negative, or neutral. In this project, the sentiment analysis is performed on the last 100 tweets of a Twitter profile to provide an overall evaluation of its positivity.

###BERT Model

BERT (Bidirectional Encoder Representations from Transformers) is a state-of-the-art deep learning model for natural language processing tasks, such as sentiment analysis. It has been pre-trained on a massive corpus of text, allowing it to understand the context and meaning of words in a sentence. In this project, the BERT model is fine-tuned on a sentiment analysis task to evaluate the positivity of Twitter profiles.