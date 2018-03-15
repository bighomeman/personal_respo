#!/usr/bin/python

import os
import time
import datetime
from parser_config import trie_store_path,source_store_path


def store_run(storeDate):
    try:
        print("Starting command."),time.ctime()
        # execute the command
        command = r'python merge_blacklist.py "%s"' %(storeDate)
        status = os.system(command)
        print('done'+"-"*100),time.ctime()
        print("Command status = %s."%status)
    except Exception, e:
        print e

def run(delta,server,entertime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')):

    startTime = datetime.datetime.strptime(entertime, '%Y-%m-%d %H:%M:%S')
    #begin= '2017-05-24 23:59:57'
    #beginTime = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
    #print startTime
    while True:
        print 'The next start time :',startTime
        while datetime.datetime.now() < startTime:
            #print 'beginTime',beginTime
            #print 'startTime',startTime
            time.sleep(1)
            #beginTime = beginTime+second

        storeDate = datetime.datetime.now().strftime('%Y-%m-%d')
        blacklist_dir = source_store_path[1]+source_store_path[0]+'-'+storeDate+".json"
        # print blacklist_dir
        blacklist_Trie_dir = trie_store_path[1]+trie_store_path[0]+'-'+storeDate+".json"
        # print blacklist_Trie_dir

        if not (os.path.exists(blacklist_dir) and os.path.exists(blacklist_Trie_dir)):
            store_run(storeDate)

        try:
            print("Starting command."),time.ctime()
            # execute the command
            gte = (startTime-delta).strftime('%Y-%m-%d %H:%M:%S')
            lte = (startTime).strftime('%Y-%m-%d %H:%M:%S')
            timestamp = (startTime).strftime('%Y-%m-%dT%H:%M:%S.%f')+"+08:00"
            command = r'python TrieSearch.py "%s" "%s" "%s" "%s"' %(gte,lte,timestamp,server)
            status = os.system(command)
            print('done'+"-"*100),time.ctime()
            print("Command status = %s."%status)
            startTime = startTime+delta
        except Exception, e:
            print e

if __name__=="__main__":
    entertime = '2018-03-15 15:30:00'
    delta = datetime.timedelta(minutes=5)
    # run(delta = delta,server = '172.23.2.150',entertime = entertime)
    run(delta,server = '172.23.2.150')
