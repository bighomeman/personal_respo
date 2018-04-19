# -*- coding: utf-8 -*-

import urllib2
import datetime
# import json
from store_json import *

def publicwww_Coinhive():
	# url = 'https://publicwww.com/websites/\"coinhive.min.js\"/?export=csv&key=312ce2140c52db8a884555e41d5aabe3'
	url = 'https://publicwww.com/websites/\"coinhive.min.js\"/?export=csv'
	f = urllib2.urlopen(url) 
	data = f.read().split('\n')[:-1]
	# print data
	domain_dict = {}
	for domain in data:
		domain_dict[domain.split(";")[0]] = {
		'type':'coinhive',
		'status':'unknown',
		'false_positive':'unknown',
		'source':'https://publicwww.com/websites/\"coinhive.min.js\"/',
		'date':datetime.datetime.now().strftime('%Y-%m-%d')
		}
	return domain_dict

def main():
	print json.dumps(publicwww_Coinhive(),indent=4)
	dict = publicwww_Coinhive()
	store_json(dict,'publicwww_Coinhive')

if __name__ == '__main__':
	# publicwww_Coinhive()
	main()
