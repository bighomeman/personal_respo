#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import os
os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
from store_json import *

def get_tr_list(url):
	'''
	获取html页面，提取所有的'tr'标签
	'''
	response = requests.get(url)
	bs = BeautifulSoup(response.text,"html.parser")
	tr_list = bs.find_all('tr')
	return tr_list

def ransomwaretracker(url = 'https://ransomwaretracker.abuse.ch/tracker/online/'):
	'''
	清洗ransomwaretracker的数据
	'''
	tr_list = get_tr_list(url)
	domain_dict = {}
	pattern_ip = re.compile('^[0-9.]+$')
	pattern_date = re.compile('^[0-9-]+')
	for tr in tr_list[1:]:
		td_list = tr.find_all('td')
		host = td_list[3].a.get_text()
		if not pattern_ip.findall(host):
			domain_dict[host] = {
			'type':td_list[1].span.get_text()+'/'+td_list[2].span.get_text(),
			'status':'online',
			'date':pattern_date.findall(td_list[0].get_text())[0],
			'source':'https://ransomwaretracker.abuse.ch/host/{}/'.format(host),
			'fp':'unknown',
			'level':'CRITICAL'
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
    dict = ransomwaretracker()
    store_json(dict,'ransomwaretracker')