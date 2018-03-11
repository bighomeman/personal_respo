#!/usr/bin/python
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import json
import datetime,sys
from blacklist_tools import load_dict

class ESclient(object):
	def __init__(self,server='192.168.0.122',port='9222'):
		self.__es_client=Elasticsearch([{'host':server,'port':port}])

	def get_es_domain(self,gte,lte,size=500000):
		'''
		获取es的dns-*索引的domain
		'''
		search_option={
            "size": 0,
            "query": {
              "bool": {
                "must": [
                  {
                    "query_string": {
                      "query": "isresponse:0"
                    }
                  },
                  {
                    "range": {
                      "@timestamp": {
                        "gte": gte,
                        "lte": lte,
                        "format": "yyyy-MM-dd HH:mm:ss"
                      }
                    }
                  }
                ],
                "must_not": []
              }
            },
            "_source": {
              "excludes": []
            },
            "aggs": {
              "domainMD": {
                "terms": {
                  "field": "domain",
                  "size": size,
                  "order": {
                    "_count": "desc"
                  }
                }
              }
            }
        }

		search_result=self.__es_client.search(
			index='dns-*',
			body=search_option
			)
		print search_result
		return search_result

	def es_index(self,doc):
		'''
		数据回插es的alert-*索引
		'''
		ret = self.__es_client.index(
			index = 'alert-{}'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
			doc_type = 'netflow_v9',
			body = doc
			)

def isMatch(Trie,dname,domain =[]):
	'''
	判断dname是否在Trie里，返回匹配成功的域名，如['a','b','c']匹配上['b','c']则返回['b','c']
	'''
	if not Trie:
		return domain
	elif not dname:
		return False
	else:
		level = dname[-1]
		if level in Trie:
			domain.insert(0,level)
			return isMatch(Trie[level],dname[:-1],domain)
		else:
			return False

def find_match_DNS(Trie,split_DNSList):
	'''
	查找所有匹配Trie的DNS，返回两个列表：match_DNSList为从es获得的dns，match_blacklist为从blacklist对应前者的dns，
	如['a','b','c']，匹配上['b','c']，则前者在match_DNSList，后者在match_blacklist
	'''
	match_DNSList=[]
	match_blacklist = []
	for split_DNS in split_DNSList:
		res = isMatch(Trie,split_DNS,[])
		if res:
			match_DNSList.append(split_DNS)
			match_blacklist.append(res)
	return match_DNSList,match_blacklist

def get_split_DNSList(search_result):
	'''
	清洗es获得的数据
	'''
	split_DNSList=[]
	for item in search_result[u'aggregations'][u'domainMD']['buckets']:
		split_DNSList.append(item[u'key'].encode('unicode-escape').split('.'))
	return split_DNSList

def main(gte,lte,timestamp):
	time=lte.split(" ")
	blacklist_dir = ".\data\\resourceFile-"+str(time[0])+".json"
	blacklist_Trie_dir = ".\data\\TrieFile-"+str(time[0])+".json"
	es = ESclient(server = '192.168.0.122')
	search_result = es.get_es_domain(gte,lte,size=50000)
	split_DNSList = get_split_DNSList(search_result)

	# test：
	# split_DNSList.append(['vmay','com'])
	# split_DNSList.append(['a','vmay','com'])

	blacklist_Trie = load_dict(blacklist_Trie_dir)
	match_DNSList,match_blacklist = find_match_DNS(blacklist_Trie,split_DNSList)
	print match_DNSList
	print match_blacklist
	'''
	匹配的DNS回插到es
	'''
	if match_DNSList:
		blacklist = load_dict(blacklist_dir)
		for i in range(len(match_blacklist)):
			domain = u'{}'.format('.'.join(match_blacklist[i]))
			doc = blacklist[domain]
			doc['domain'] = '.'.join(match_DNSList[i])
			doc['@timestamp'] = timestamp
			es.es_index(doc)

if __name__ == '__main__':
	main(sys.argv[1],sys.argv[2],sys.argv[3])
