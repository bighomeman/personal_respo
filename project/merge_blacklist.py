# -*- coding: utf-8 -*-
import os,sys
from blacklist_tools import *
from configuration import data_path,moudle_name,logger_info,logger_error

sys.dont_write_bytecode = True

# 存储原始数据
def get_blacklist_module():
    parse_blacklist = moudle_name
    for file_name in parse_blacklist:
        module = __import__('get_blacklist.{0}'.format(file_name),fromlist=True)
        logger_info.info('Downloading {0}.'.format(file_name))
        try:
            module.main()
            logger_info.info('Download {0} completed.'.format(file_name))
        except Exception as e:
            logger_error.error('Download {0} failed.'.format(file_name))
        

def merge_blacklist(dir,date,name):
    parse_blacklist = moudle_name
    i = 0
    merge_result = {}
    for file_name in parse_blacklist:
        if os.path.exists(file_name + '.json'):
            result = load_dict(file_name + '.json')
        else:
            continue
        # print len(result)
        if i ==0:
            merge_result = result
        else:
            merge_result = update_dict(result,merge_result)
        i = i + 1
        # print len(merge_result)
    saveAsJSON(date,merge_result,dir,name)

    for file_name in parse_blacklist:
        if os.path.exists(file_name+'.json'):
            os.remove(file_name+'.json')

#建Trie树

def store_trie(dir, date, name):
    path = data_path + 'source' + "-" +date + '.json'
    result = load_dict(path)
    # print result
    saveAsJSON(date,create_Trie([x.split('.') for x in result.keys()]),dir,name)

def main(storeDate):
    get_blacklist_module()
    merge_blacklist(data_path,storeDate,'source')
    store_trie(data_path,storeDate,'trie')



