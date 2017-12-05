import pandas as pd
import json

def get_pandas_from_json(file): 
	df = pd.read_json(file, lines=True)
	return df

def randomize(arrays, size=None):
    if not size: 
        size = arrays[0].shape[0]

    # Generate the permutation index array.
    np.random.seed(0)
    permutation = np.random.permutation(size)
    return [a[permutation] for a in arrays]

import pandas as pd
import numpy as np
import preprocessor as p
import re as regex
import re,string
import emoji

from nltk.stem.porter import *
stemmer = PorterStemmer()

def transform_tweet(line):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",line).split())


def strip_all_entities(text):
    entity_prefixes = ['@', '#', '_']
    text = text.replace('</br>', ' ')
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    text = text.replace('RT', '')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)


def remove_by_regex(t, regexp):
    t.replace(regexp, "", inplace=True)
    return t

def clean(tweets):
    tweets['text'] = tweets['text'].apply(lambda x: p.clean(x))
    return tweets

def remove_special_chars(t):  # it unrolls the hashtags to normal words
    special_chars = [",", ":", "\"", "=", "&", ";", "%", "$",
                     "@", "%", "^", "*", "(", ")", "{", "}",
                     "[", "]", "|", "/", "\\", ">", "<", "-",
                     "!", "?", ".", "'",
                     "--", "---", "#"]
    special_chars = [",", "\"", "=", "&", ";", "%", "$",
                     "@", "%", "^", "*", "{", "}",
                     "[", "]", "|", "\\", ">", "<", "-",
                      ".", "'",
                     "--", "---", "#"]
    special_chars = ["!", "?", "@", "."]
    for remove in map(lambda r: regex.compile(regex.escape(r)), special_chars):
        t.replace(remove, "", inplace=True)
    return t

def remove_usernames(t):
    return remove_by_regex(t, regex.compile(r"@[^\s]+[\s]?"))

def remove_numbers(t):
    return remove_by_regex(t, regex.compile(r"\s?[0-9]+\.?[0-9]*"))

def remove_emojis(string):
    return ' '.join(c for c in string if c not in emoji.UNICODE_EMOJI)

def clean_tweets(t):
    #t = t.dropna(subset=['tweet'])
   # t['text'] = pd.Series([row.decode('utf-8').encode('ascii', errors='ignore') for row in t['text']])
   # t['text'] = pd.Series([remove_emojis(row) for row in t['text']])
    t['tweet'] = remove_numbers(t['tweet'])
    t['tweet'] = [transform_tweet(row) for row in t['tweet']] 
    t['tweet'] = [removeNonAscii(row) for row in t['tweet']]

    return t

def removeNonAscii(s): 
    return ''.join(i for i in s if ord(i)<128)

def clean_txt(t): 
    t = pd.Series([strip_all_entities(row).lower() for row in t])
    t = remove_special_chars(t)
    t = remove_numbers(t)

    #t = [row.decode('utf-8').encode('ascii', errors='ignore') for row in t]
    t = [removeNonAscii(row) for row in t]
    return t