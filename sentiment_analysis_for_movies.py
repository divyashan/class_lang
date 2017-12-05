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

# helper function to binarize ratings
def map_rating_to_sentiment(rating):
	if rating == 5:
		return 1
	else:
		return 0

# specify whether to do a test run on a small amount of data
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true', default=False)
parser.add_argument("--mini", action='store_true', default=False)
args = parser.parse_args()
print args
print args.debug == True 

# read data and keep those with 1 or 5 star ratings
review_list = []
y = []
i = 0
for basepath in ['../wiml_project/class_lang/aclImdb/train/neg/', '../wiml_project/class_lang/aclImdb/train/pos/']:
    files = listdir(basepath)
    for fname in files:
        f = open(basepath + fname, 'r')
        text = ' '.join(f.readlines())
        review_list.append(text)
        y.append(i)
    i += 1

def removeNonAscii(s): 
    return ''.join(i for i in s if ord(i)<128)



review_list = [removeNonAscii(row) for row in review_list]
review_list_series = pd.Series(review_list)


review_df = pd.DataFrame({'reviewText':review_list_series, 'rating':y})

# get columns for reviews + ratings, convert ratings to binary good/bad
reviews = review_df['reviewText']
ratings = review_df['rating']


# for keeping track of error on each review
correct = 0
predictions = []
true = []

# the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# go through reviews and ratings, averages sentiment across all sentences in a single review.
# predicts positive or negative based on which sentiment is higher, and then overall accuracy across all reviews.
for review, rating in zip(reviews, ratings): 
	split_review = tokenize.sent_tokenize(review)
	results = []

	for sentence in split_review:
		ss = sid.polarity_scores(sentence)
		results.append(ss)
		# if args.debug:
		# 	print sentence
		# 	print ss
	if len(results) == 0: continue
	S = {k:[ results[j][k] for j in range(len(results)) ] for k in results[0].keys()}
	avg_sentiment = {k:( reduce(np.add, v)/len(v) ) for k,v in S.iteritems()}
	avg_pos = avg_sentiment['pos']
	avg_neg = avg_sentiment['neg']
	pred = 1 if avg_pos > avg_neg else 0
	if pred == rating: correct += 1
	predictions.append(pred)
	true.append(rating)
	if args.debug and pred != rating and rating == 0:
		print review
		print "Positive: ", avg_pos
		print "Negative: ", avg_neg
		print "True: ", rating


all_results = pd.DataFrame({'pred':predictions, 'true':true})
all_results['correct'] = all_results['pred'] == all_results['true'] 
accuracy = ( np.sum(all_results['correct']) * 1.0 ) / len(all_results)
one_star_accuracy = np.sum(all_results.loc[all_results['true'] == 0]['correct'])*1.0/len(all_results.loc[all_results['true'] == 0])
five_star_accuracy = np.sum(all_results.loc[all_results['true'] == 1]['correct'])*1.0/len(all_results.loc[all_results['true'] == 1])

print "Overall Accuracy = ", accuracy, 'given ', len(all_results), "total reviews"
print "5 star accuracy = ", five_star_accuracy, "given ", len(all_results.loc[all_results['true'] == 1]), " total 5 star reviews."
print "1 star accuracy = ", one_star_accuracy, "given ", len(all_results.loc[all_results['true'] == 0]), " total 1 star reviews."
