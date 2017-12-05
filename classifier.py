# Linear classifier of low income tweets vs high income tweets
import keras
import numpy as np
import pandas as pd
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input, Lambda, Conv2D, MaxPooling2D, Flatten

# Take in df of low income tweets and df of high income tweets

q1_tweet_text = pd.read_csv('q1_tweets.csv')

q4_tweet_text = pd.read_csv('q4_tweets.csv')
n_q1 = len(q1_tweet_text)
n_q4 = len(q4_tweet_text)

y = np.concatenate((np.zeros(n_q1),np.ones(n_q4))) 

print q1_tweet_text[:5]

