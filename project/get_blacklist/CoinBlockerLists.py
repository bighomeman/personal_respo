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
		'type':'coinMiner',
		'status':'unknown',
		'false_positive':'unknown',
		'source':'https://zerodot1.github.io/CoinBlockerLists/',
		'date':datetime.datetime.now().strftime('%Y-%m-%d')
		}
	return domain_dict

def main():
	# print json.dumps(CoinBlockerLists(),indent=4)
	dict = CoinBlockerLists()
	store_json(dict,'CoinBlockerLists')

# if __name__ == '__main__':
# 	main()
	
