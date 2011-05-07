#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Benjamin Fields on 2011-05-08.
"""

import sys
import os
import urllib2
import re
from simplejson import loads
log = logging.getLogger(__name__)

from apikey_private import *


def process_exquisite(raw_html):
	'''
	takes in html of the sort found from an equisite tweet conversation and returns
	'''
	return map(lambda x:int(x[x.rindex('/')+1]),
				re.findall('http://twitter.com/[\w]*/status/[\d]*', raw_data))
	
def determine_tweet_sentiment(status_id):
	'''
	grabs the tweet identified by status_id and send the text to the musicmetric sentiment service
	returns the sentiment of the tweet, 1 is very negative, 5 is very positive
	'''
	data = loads(urllib2.urlopen("http://api.twitter.com/1/statuses/show/{0}.json".\
				format(twitter_id)).read())
	tweet_content = data["text"]
	return loads(urllib2.urlopen("http://apib1.semetric.com/musicmetric/sentiment?token="+\
					API_KEY, data = tweet_content).read())
	
def find_max_neg_delta(senti_list):
	'''
	finds the highest magnitude decrease in sentiment point
	returns the index
	'''
	max_neg_delta = 0
	last_senti = -1
	winner_idx = None
	for idx, current_senti in enumerate(senti_list[:-1]):
		if current_senti - last_senti < max_neg_delta:
			max_neg_delta = current_senti
			winner_idx = idx
	return winner_idx

def main():
	pass


if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG, 
		format='%(asctime)s %(levelname)s %(message)s')
	sys.exit(main(sys.argv))

