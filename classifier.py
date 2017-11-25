# Linear classifier of low income tweets vs high income tweets
import keras
import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Input, Lambda, Conv2D, MaxPooling2D, Flatten

# Take in df of low income tweets and df of high income tweets

q1_tweet_text = list(q1_tweets['tweets'])
q4_tweet_text = list(q4_tweets['tweets'])
n_q1 = len(q1_tweet_text)
n_q4 = len(q4_tweet_text)

y = np.concatenate((np.zeros((n_q1, 1)),np.ones(n_q1, 1))) 



