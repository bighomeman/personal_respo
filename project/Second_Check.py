#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import datetime

def query_last(es,gte,lte,time_zone,dip):
	search_option = {
		"size": 0,
		"query": {
			"bool": {
				"must": [
					{
						"query_string": {
							"query": "dip:{}".format(dip),
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
			"sip": {
				"terms": {
					"field": "sip",
					"size": 100,
					"order": {
						"_count": "desc"
					}
				}
			}
		}
	}
	result = es.search(
		index = "tcp-*",
		body  = search_option
	)
	return result

def get_date_flow(es,gte,lte,time_zone,dip,sip_filter):
	search_option = {
		"size": 0,
		"query": {
			"bool": {
				"must": [
					{
						"query_string": {
							"query": "dip:{0}{1}".format(dip,sip_filter),
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
			"sip": {
				"terms": {
					"field": "sip",
					"size": 100,
					"order": {
						"flow": "desc"
					}
				},
				"aggs":{
					"flow": {
						"sum": {
							"field": "flow"
						}
					},
					"date": {
						"date_histogram": {
							"field": "@timestamp",
							"interval": "5m",
							"time_zone":time_zone,
							"min_doc_count": 1
						},
						"aggs": {
							"flow": {
								"sum": {
									"field": "flow"
								}
							}
						}	
					}
				}
			}
		}
	}
	result = es.search(
		index = "tcp-*",
		body  = search_option
	)
	return result

def calc_median(datalist):
	datalist.sort()
	half = len(datalist) // 2
	return (datalist[half]+datalist[~half])/2.0

def calc_MAD(datalist):
	median = calc_median(datalist)
	return calc_median([ abs(data-median) for data in datalist ])
	
def main(es,gte,lte,time_zone,dip):
	result = query_last(es=es,gte=gte,lte=lte,time_zone=time_zone,dip=dip)
	sip_list = []
	sip_filter = ""
	for sip in result["aggregations"]["sip"]["buckets"]:
		sip_list.append(sip["key"])
	if sip_list:
		for sip in sip_list:
			if sip != sip_list[-1]:
				sip_filter = sip_filter + "sip:{0} OR ".format(sip)
			else:
				sip_filter = sip_filter + "sip:{0}".format(sip)
		sip_filter = " AND (" + sip_filter + ")"

	temp_lte = datetime.datetime.strptime(lte,'%Y-%m-%d %H:%M:%S')
	gt = (temp_lte - datetime.timedelta(hours = 72)).strftime('%Y-%m-%d %H:%M:%S')
	res = get_date_flow(es=es,gte=gt,lte=lte,time_zone=time_zone,dip=dip,sip_filter=sip_filter)

	ret_siplist = []
	for sip_item in res["aggregations"]["sip"]["buckets"]:
		datelist = []
		flowlist = []
		for item in sip_item["date"]["buckets"]:
			datelist.append(item["key"])
			flowlist.append(item["flow"]["value"])
		if len(datelist)<3:
			continue
		date_dev = [datelist[i+1]-datelist[i]  for i in range(len(datelist)-1)]
		if (calc_MAD(date_dev) == 0) and (calc_MAD(flowlist) == 0):
			ret_siplist.append(sip_item["key"])
	return ret_siplist		
