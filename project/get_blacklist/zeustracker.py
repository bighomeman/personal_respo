#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import os
# os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
from store_json import *

def get_tr_list(url):
	'''
	获取html页面，提取所有的'tr'标签
	'''
	response = requests.get(url)
	bs = BeautifulSoup(response.text,"html.parser")
	tr_list = bs.find_all('tr')
	return tr_list

def zeustracker(url='https://zeustracker.abuse.ch/monitor.php?filter=all'):
	'''
	清洗zeustracker的数据
	'''
	tag = {
	u'1':'Bulletproof hosted',
	u'2':'Hacked webserver',
	u'3':'Free hosting service',
	u'4':'Unknown',
	u'5':'Hosted on a FastFlux botnet'
	}
	tr_list = get_tr_list(url)
	domain_dict = {}
	pattern = re.compile('^[0-9.]+$')
	for tr in tr_list[7:]:
		td_list = tr.find_all('td')
		host = td_list[2].get_text()
		if not pattern.findall(host):
			domain_dict[host] = {
			'type':tag[td_list[4].get_text()]+'/'+td_list[1].get_text(),
			'status':td_list[5].get_text(),
			'date':td_list[0].get_text(),
			'source':'https://zeustracker.abuse.ch/monitor.php?host={}'.format(host),
			'fp':'unknown',
			'level':judge_level('unknown',td_list[5].get_text())
			}

	return domain_dict

def judge_level(fp,status):
	'''
	根据fp、status判断level
	'''
	if status == 'online':
		if fp == 'high':
			return 'WARNING'
		else:
			return 'CRITICAL'
	elif status == 'unknown':
		if fp == 'low':
			return 'CRITICAL'
		elif fp == 'high':
			return 'INFO'
		else:
			return 'WARNING'
	else:
		if fp == 'low' or fp == 'unknown':
			return 'WARNING'
		else:
			return 'INFO'

if __name__=="__main__":
    dict = zeustracker()
    store_json(dict,'zeustracker')