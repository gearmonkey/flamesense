#!/usr/bin/env python
# encoding: utf-8
"""
firealarm.py

take in an exquisitetweet conversation url and uses the Musicmetric sentiment analyzer to deterimine if it's a flame war (generally highly negative comments) and find the troll (the author of the comment that dragged the conversation negative the most)

call like this:
python firealarm.py http://exquisitetweets.com/path/to/converstaion

Created by Benjamin Fields on 2011-05-08.
"""

import sys
import os
import urllib2
import re
import logging
from simplejson import loads
log = logging.getLogger(__name__)

from apikey import *


def process_exquisite(raw_html):
	'''
	takes in html of the sort found from an equisite tweet conversation and returns
	'''
	return re.findall('http://twitter.com/[\w]*/status/([\d]*)">[\d]', raw_html)
	
def determine_tweet_sentiment(status_id):
	'''
	grabs the tweet identified by status_id and send the text to the musicmetric sentiment service
	returns the sentiment of the tweet, 1 is very negative, 5 is very positive
	'''
	data = loads(urllib2.urlopen("http://api.twitter.com/1/statuses/show/{0}.json".\
				format(status_id)).read())
	tweet_content = data["text"].encode('utf-8')
	score =  int(loads(urllib2.urlopen("http://apib1.semetric.com/musicmetric/sentiment?token="+\
					API_KEY, data = tweet_content).read())['score'])
	log.debug( (data["text"]) +  "::" +  str(score))
	return score
	
def find_max_neg_delta(senti_list):
	'''
	finds the highest magnitude decrease in sentiment point
	returns the index
	'''
	max_neg_delta = 0
	last_senti = senti_list[0]
	winner_idx = None
	for idx, current_senti in enumerate(senti_list[1:]):
		if current_senti - last_senti < max_neg_delta:
			max_neg_delta = current_senti
			winner_idx = idx
		last_senti = current_senti
	return winner_idx

def main(argv):
	print 'fetching the conversation at', argv[1]
	raw_data = urllib2.urlopen(argv[1]).read()
	status_IDs = process_exquisite(raw_data)
	status_IDs.reverse() #flip them to be in written order
	
	print 'Is the conversation a flame war?'
	sentiments = map(lambda x:determine_tweet_sentiment(x), status_IDs)
	mean_sent = reduce(lambda x,y:x+y, sentiments)/float(len(sentiments))
	if mean_sent < 3:
		print "\tyes"
	elif mean_sent > 3:
		print "\tno"
	else:
		print "\tmaybe"
	
	print "Where's the troll?"
	winner_idx = find_max_neg_delta(sentiments)
	try:
		print '\t', re.findall('(http://twitter.com/[\w]*/status/'+\
				str(status_IDs[winner_idx])+')">[\d]', raw_data)[0]
	except TypeError:
		print "no troll, this conversation was flat."
		return 0
		
	data = loads(urllib2.urlopen("http://api.twitter.com/1/statuses/show/{0}.json".\
				format(status_IDs[winner_idx])).read())
	print "Author:", data['user']['name'], 'username:', data['user']['screen_name']
	print "Now stop feeding the trolls!"
	return 0
	
if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, 
		format='%(asctime)s %(levelname)s %(message)s')
	sys.exit(main(sys.argv))

