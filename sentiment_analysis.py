from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize
import sys
sys.path.insert(0, 'preprocessing')
import read_data
import numpy as np
import pandas as pd
import argparse

# helper function to binarize ratings
def map_rating_to_sentiment(rating):
	if rating == 5:
		return 1
	else:
		return 0

def map_price_to_quantile(price, low, high):
	if price <= low: 
		return 0
	elif price >= high:
		return 1
	else: 
		return 100

# specify whether to do a test run on a small amount of data
parser = argparse.ArgumentParser()
parser.add_argument("--debug", action='store_true', default=False)
parser.add_argument("--mini", action='store_true', default=False)
args = parser.parse_args()
print args
print args.debug == True 

# read data and keep those with 1 or 5 star ratings
path = 'data/reviews_Electronics_5.json'
df = read_data.get_pandas_from_json(path)
df = df.loc[df['overall'].isin([1,5])].sample(18000)

#metadata_path = 'data/meta_pickle'
#metadata_df = pd.read_pickle(metadata_path)[['asin', 'price']]

#df = df.merge(metadata_df, how='inner', on='asin')
#print df.columns

# debug setting
if args.mini: 
	df = df.head(50)

# price quartiles
#low = df['price'].quantile(.25)
#high = df['price'].quantile(.75)
#df['price_quantile'] = df['price'].apply(map_price_to_quantile, args=(low, high))
#df = df.loc[df['price_quantile'] < 2]
#price = df['price_quantile']

print df.shape

# get columns for reviews + ratings, convert ratings to binary good/bad
reviews = df['reviewText']
ratings = df['overall']
ratings = ratings.map(map_rating_to_sentiment)

# for keeping track of error on each review
correct = 0
predictions = []
true = []
price_range = []

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



# go through reviews and ratings, averages sentiment across all sentences in a single review.
# predicts positive or negative based on which sentiment is higher, and then overall accuracy across all reviews.
# for review, rating, price in zip(reviews, ratings, price): 
# 	split_review = tokenize.sent_tokenize(review)
# 	results = []

# 	for sentence in split_review:
# 		ss = sid.polarity_scores(sentence)
# 		results.append(ss)
# 		# if args.debug:
# 		# 	print sentence
# 		# 	print ss
# 	if len(results) == 0: continue
# 	S = {k:[ results[j][k] for j in range(len(results)) ] for k in results[0].keys()}
# 	avg_sentiment = {k:( reduce(np.add, v)/len(v) ) for k,v in S.iteritems()}
# 	avg_pos = avg_sentiment['pos']
# 	avg_neg = avg_sentiment['neg']
# 	pred = 1 if avg_pos > avg_neg else 0
# 	if pred == rating: correct += 1
# 	predictions.append(pred)
# 	true.append(rating)
# 	price_range.append(price)
# 	if args.debug and pred != rating and rating == 0:
# 		print review
# 		print "Positive: ", avg_pos
# 		print "Negative: ", avg_neg
# 		print "True: ", rating


all_results = pd.DataFrame({'pred':predictions, 'true':true})
all_results['correct'] = all_results['pred'] == all_results['true'] 
#all_results = all_results.loc[all_results['price'] < 2]
accuracy = ( np.sum(all_results['correct']) * 1.0 ) / len(all_results)
one_star_accuracy = np.sum(all_results.loc[all_results['true'] == 0]['correct'])*1.0/len(all_results.loc[all_results['true'] == 0])
five_star_accuracy = np.sum(all_results.loc[all_results['true'] == 1]['correct'])*1.0/len(all_results.loc[all_results['true'] == 1])
# low_price_accuracy = np.sum(all_results.loc[all_results['price'] == 0]['correct'])*1.0/len(all_results.loc[all_results['price'] == 0])
# high_price_accuracy = np.sum(all_results.loc[all_results['price'] == 1]['correct'])*1.0/len(all_results.loc[all_results['price'] == 1])
# one_star_low_price = np.sum(all_results['correct'][(all_results['price'] == 0) & (all_results['true'] == 0)])
# five_star_low_price = np.sum(all_results['correct'][(all_results['price'] == 0) & (all_results['true'] == 1)])
# one_star_hi_price = np.sum(all_results['correct'][(all_results['price'] == 1) & (all_results['true'] == 0)])
# five_star_hi_price = np.sum(all_results['correct'][(all_results['price'] == 1) & (all_results['true'] == 1)])

print "Overall Accuracy = ", accuracy, 'given ', len(all_results), "total reviews"
print "5 star accuracy = ", five_star_accuracy, "given ", len(all_results.loc[all_results['true'] == 1]), " total 5 star reviews."
print "1 star accuracy = ", one_star_accuracy, "given ", len(all_results.loc[all_results['true'] == 0]), " total 1 star reviews."
# print "Lo price accuracy = ", low_price_accuracy, "given ", len(all_results.loc[all_results['price'] == 0]), " total low price reviews."
# print "Hi Price accuracy = ", high_price_accuracy, "given ", len(all_results.loc[all_results['price'] == 1]), " total high price reviews."

# print "one_star_low_price accuracy = ", one_star_low_price, "given ", len(all_results[(all_results['price'] == 0) & (all_results['true'] == 0)]), " total"
# print "five_star_low_price accuracy = ", five_star_low_price, "given ", len(all_results[(all_results['price'] == 0) & (all_results['true'] == 1)]), " total"
# print "one_star_hi_price accuracy = ", one_star_hi_price, "given ", len(all_results[(all_results['price'] == 1) & (all_results['true'] == 0)]), " total"
# print "five_star_hi_price accuracy = ", five_star_hi_price, "given ", len(all_results[(all_results['price'] == 1) & (all_results['true'] == 1)]), " total"
