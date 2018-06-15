#!/usr/bin/python
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
import json,re
import datetime,sys,os
from blacklist_tools import load_dict,create_Trie
from configuration import set_data_path,get_es_config,logger_info,logger_error,get_syslog_config
import Second_Check

data_path = set_data_path()
ES_config = get_es_config()

class ESclient(object):
	def __init__(self):
		self.__es_client=Elasticsearch([{'host':ES_config[0],'port':ES_config[1]}])

	def get_es_domain(self,gte,lte,time_zone):
		# 获取es的dns-*索引的domain
		search_option={
			"size": 0,
			"query": {
				"bool": {
					"must": [
						{
							"query_string": {
							"query": "domain:*.*",
							'analyze_wildcard': True
							}
						},
						{
							"range": {
							"@timestamp": {
								"gte": gte,
								"lte": lte,
								"format": "yyyy-MM-dd HH:mm:ss",
								"time_zone": time_zone
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
				"domain": {
					"terms": {
						"field": "domain",
						"size": 50000,
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
		# print search_result
		return search_result

	def get_domain_info(self,gte,lte,domain,time_zone):
		#反查可疑domain的answer
		search_option={
			"size": 0,
			"query": {
				"bool": {
					"must": [
						{
							"query_string": {
							"query": "domain:{0} AND isresponse:1".format(domain),
							'analyze_wildcard': True
							}
						},
						{
							"range": {
							"@timestamp": {
								"gte": gte,
								"lte": lte,
								"format": "yyyy-MM-dd HH:mm:ss",
								"time_zone": time_zone
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
					"answer": {
						"terms": {
							"field": "answer",
							"size": 50,
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
		# print json.dumps(search_result,indent=4)
		return search_result
	
	def second_check(self,gte,lte,time_zone,dip):
		return Second_Check.main(es=self.__es_client,gte=gte,lte=lte,time_zone=time_zone,dip=dip)

	def es_index(self,doc):
		# 数据回插es的alert-*索引
		ret = self.__es_client.index(
			index = 'alert-{}'.format(datetime.datetime.now().strftime('%Y-%m-%d')),
			doc_type = 'netflow_v9',
			body = doc
			)

def isMatch(Trie,dname,domain =[]):
	# 判断dname是否在Trie里，返回匹配成功的域名，如['a','b','c']匹配上['b','c']则返回['b','c']
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
	# 清洗es获得的数据
	split_DNSList=[]
	for item in search_result[u'aggregations'][u'domain'][u'buckets']:
		split_DNSList.append(item[u'key'].encode('unicode-escape').split('.'))
	return split_DNSList

def get_answer_list(search_result):
	answer_list = []
	for answer_bucket in search_result[u'aggregations'][u'answer'][u'buckets']:
		answer = answer_bucket[u'key'].encode('unicode-escape')
		answer_list.append(answer)
	return answer_list

def check_whitelist(match_DNSList,match_blacklist):
	try:
		with open(os.path.join(data_path,"local_Whitelist.txt"),'r') as f:
			text = f.read().split('\n')[6:-1]
	except Exception as e:
		logger_error.error("Get whitelist failed.\n{0}".format(e))
	split_DNSList = []
	for domain in text:
		split_DNSList.append(domain.split('.'))
	white_Trie = create_Trie(split_DNSList)
	ret_DNSList = []
	ret_blacklist = []
	for i in range(len(match_DNSList)):
		if not isMatch(white_Trie,match_DNSList[i],domain =[]):
			ret_DNSList.append(match_DNSList[i])
			ret_blacklist.append(match_blacklist[i])
	return ret_DNSList,ret_blacklist
	


def main(gte,lte,timestamp,time_zone):
	time=datetime.datetime.now().strftime('%Y-%m-%d')
	blacklist_dir = os.path.join(data_path,'source'+'-'+str(time)+".json")
	# print blacklist_dir
	blacklist_Trie_dir = os.path.join(data_path,'trie'+'-'+str(time)+".json")
	# print blacklist_Trie_dir
	count = 0
	temp_time = datetime.datetime.strptime(lte,'%Y-%m-%d %H:%M:%S')
	while (not (os.path.exists(blacklist_dir) and os.path.exists(blacklist_Trie_dir))) and count<30:
		temp_time = temp_time + datetime.timedelta(days = -1)
		time = temp_time.strftime('%Y-%m-%d %H:%M:%S').split(" ")
		blacklist_dir = os.path.join(data_path,'source'+'-'+str(time)+".json")
		blacklist_Trie_dir = os.path.join(data_path,'trie'+'-'+str(time)+".json")
		count += 1
	if count == 30:
		logger_error.error('No blacklist data in last 30 days.')
		return 1
	es = ESclient()
	try:
		logger_info.info('Getting ES DNS domain completed.')
		search_result = es.get_es_domain(gte=gte,lte=lte,time_zone=time_zone)
		logger_info.info('Get ES DNS domain completed.')
	except Exception as e:
		logger_error.error("Get ES DNS domain failed.\n{0}".format(e))
	
	split_DNSList = get_split_DNSList(search_result)

	blacklist_Trie = load_dict(blacklist_Trie_dir)
	match_DNSList,match_blacklist = find_match_DNS(blacklist_Trie,split_DNSList)
	match_DNSList,match_blacklist = check_whitelist(match_DNSList,match_blacklist)
	logger_info.info('Match DNS list :\n{0}'.format(match_DNSList))
	logger_info.info('Match DNS blacklist :\n{0}'.format(match_blacklist))
	syslogger = get_syslog_config()
	# 匹配的DNS回插到es
	if match_DNSList:
		dip_list = []
		ipv4_pattern = re.compile('^(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}$')
		try:
			blacklist = load_dict(blacklist_dir)
			for i in range(len(match_blacklist)):
				domain = u'{}'.format('.'.join(match_blacklist[i]))
				domain_es = '.'.join(match_DNSList[i])
				doc = blacklist[domain]
				doc['domain'] = domain_es
				doc['@timestamp'] = timestamp
				doc['level'] = "INFO"
				doc['type'] = "MAL_DNS"
				doc['desc_type'] = "[MAL_DNS] Request of Malicious Domain Name Detection"
				doc['desc_subtype'] = "[{0}] Malicious domain name:{1}".format(doc['subtype'],domain)
				search_result = es.get_domain_info(gte=gte,lte=lte,domain=domain_es,time_zone=time_zone)
				answer_list = get_answer_list(search_result)
				dip_list = dip_list + answer_list
				for answer in answer_list:
					doc['answer'] = answer
					es.es_index(doc)
					if syslogger:
						syslogger.info(doc)
#					print doc
					if ipv4_pattern.findall(answer):
						temp_lte = datetime.datetime.strptime(lte,'%Y-%m-%d %H:%M:%S')
						gt = (temp_lte - datetime.timedelta(hours = 72)).strftime('%Y-%m-%d %H:%M:%S')
						sip_list = es.second_check(gte=gt,lte=lte,time_zone=time_zone,dip=answer)
#						print sip_list
						if sip_list:
							for sip in sip_list:
								doc["sip"] = sip
								doc["level"] = "WARNING"
								es.es_index(doc)
								if syslogger:
									syslogger.info(doc)
		except Exception as e:
			logger_error.error("Insert the alert of theat DNS to ES failed.\n{0}".format(e))

# if __name__ == '__main__':
# 	main()
