
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import sys
sys.path.insert(0, 'preprocessing')
import read_data
import numpy as np
import pandas as pd
import argparse
from os import listdir
from os.path import isfile, join


# specify whether to do a test run on a small amount of data
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true', default=False)
parser.add_argument("--mini", action='store_true', default=False)
args = parser.parse_args()
print args
print args.debug == True 

# read data and keep those with 1 or 5 star ratings
tweet_list = []
y = []
i = 0

happy_tweets = []
sad_tweets = []
tweets = pd.read_csv('../wiml_project/class_lang/tweets.csv')['tweet']
for tweet in tweets: 
	words = tweet.split(' ')
	if ':)' in words or ':-)' in words: 
		happy_tweets.append(' '.join([w for w in words if w not in [':)', ':-)']]))
	elif ':(' in words or ':-(' in words: 
		sad_tweets.append(' '.join([w for w in words if w not in [':(', ':-(']]))

print len(happy_tweets), happy_tweets[:10]
print len(sad_tweets), sad_tweets[:10]

all_tweets = happy_tweets + sad_tweets
labels = [1]*len(happy_tweets) + [0]*len(sad_tweets)

tweets = pd.DataFrame({'tweet':all_tweets, 'sentiment':labels})

clean_tweets = read_data.clean_tweets(tweets)['tweet']
print clean_tweets.head(20)


# for keeping track of error on each review
correct = 0
predictions = []
true = []

# the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# go through reviews and ratings, averages sentiment across all sentences in a single review.
# predicts positive or negative based on which sentiment is higher, and then overall accuracy across all reviews.
for tweet, label in zip(all_tweets, labels): 
	ss = sid.polarity_scores(tweet)
	if ss['pos'] > ss['neg']: 
		pred = 1
	else:
		pred = 0

	if pred == label: correct += 1
	predictions.append(pred)
	true.append(label)
	if args.debug and pred != label and label == 0:
		print review
		print "Positive: ", avg_pos
		print "Negative: ", avg_neg
		print "True: ", label

	if pred != label: 
		print tweet
		print "pred", pred
		print "label", label

all_results = pd.DataFrame({'pred':predictions, 'true':true})
all_results['correct'] = all_results['pred'] == all_results['true'] 
accuracy = ( np.sum(all_results['correct']) * 1.0 ) / len(all_results)
one_star_accuracy = np.sum(all_results.loc[all_results['true'] == 0]['correct'])*1.0/len(all_results.loc[all_results['true'] == 0])
five_star_accuracy = np.sum(all_results.loc[all_results['true'] == 1]['correct'])*1.0/len(all_results.loc[all_results['true'] == 1])

print "Overall Accuracy = ", accuracy, 'given ', len(all_results), "total reviews"
print "5 star accuracy = ", five_star_accuracy, "given ", len(all_results.loc[all_results['true'] == 1]), " total 5 star reviews."
print "1 star accuracy = ", one_star_accuracy, "given ", len(all_results.loc[all_results['true'] == 0]), " total 1 star reviews."
