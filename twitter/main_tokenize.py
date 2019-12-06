from __future__ import division
import json
import pandas as pd
import numpy as np
import requests
import nltk
import string
import re
import os
from os import path
from time import sleep
from collections import Counter
from nltk.tokenize import TweetTokenizer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import twitter_samples
from random import shuffle

def tokenizeTweets(tweetList):
    useless_ones = nltk.corpus.stopwords.words("english") + list(string.punctuation)
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=False, reduce_len=False)
    retTweetList = []
    for tweet in tweetList:
        wordlist = [word for word in tokenizer.tokenize(tweet) if word not in useless_ones]
        retTweetList.append(wordlist)
    return retTweetList

def tokenizeTweet(tweet):
    useless_ones = nltk.corpus.stopwords.words("english") + list(string.punctuation)
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=False, reduce_len=False)
    wordlist = [word for word in tokenizer.tokenize(tweet) if word not in useless_ones]
    return wordlist

def stemTweets(tweetList):
    sno = nltk.stem.SnowballStemmer("english")
    retTweetList = []
    for words in tweetList:
        stemmed_words = [sno.stem(word) for word in words]
        retTweetList.append(stemmed_words)
    return retTweetList

def stemTweet(tweet):
    sno = nltk.stem.SnowballStemmer("english")
    stemmed_words = [sno.stem(word) for word in tweet]
    return stemmed_words

def main(twtInfo:object):
    clean_data_tweets = pd.read_json(twtInfo, orient="records")
    nltk.download("stopwords")
    nltk.download("punkt")
    tweets = clean_data_tweets["text"]
    data_id = clean_data_tweets["id"]
    data_tc_tweets = []
    for tweet in tweets:
        data_tc_tweets.append(tokenizeTweet(tweet))
    data_tcs_tweets = []
    for tweet in data_tc_tweets:
        data_tcs_tweets.append(stemTweet(tweet))
    ret = []
    for i in range(len(data_tcs_tweets)):
        ret.append({})
        ret[i]["text"] = data_tcs_tweets[i]
        ret[i]["id"] = data_id[i]
    return pd.Series(ret).to_json(orient="records")

dat = main("test_clean_out.json")
with open("test_token_out.json", "w+") as out:
    out.write(dat)