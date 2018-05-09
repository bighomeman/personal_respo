#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import datetime
# import json
from store_json import *

def CoinBlockerLists():
	url = 'https://raw.githubusercontent.com/ZeroDot1/CoinBlockerLists/master/list.txt'
	f = urllib2.urlopen(url) 
	data = f.read().split('\n')[:-1]
	# print data
	domain_dict = {}
	for domain in data:
		domain_dict[domain] = {
		'maltype':'coinminer',
		'desc_maltype':unicode('[coinminer]挖矿机相关域名','utf-8'),
		'desc_subtype':'https://zerodot1.github.io/CoinBlockerLists/'
		}
	return domain_dict

def main():
	# print json.dumps(CoinBlockerLists(),indent=4)
	dict = CoinBlockerLists()
	store_json(dict,'CoinBlockerLists')

# if __name__ == '__main__':
# 	main()
	
