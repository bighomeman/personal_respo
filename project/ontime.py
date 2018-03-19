#!/usr/bin/python

import os
import time
import datetime
from parser_config import trie_store_path,source_store_path,frequency
import TrieSearch,merge_blacklist


def store_run(storeDate):
    try:
        print("Downloading blacklists"),time.ctime()

        merge_blacklist.main(storeDate)

        # execute the command
        # command = r'python merge_blacklist.py "%s"' %(storeDate)
        # status = os.system(command)
        print("-"*25+'DONE'+"-"*25),time.ctime()
        # print("Command status = %s."%status)
    except Exception, e:
        print e

def run(delta,entertime):

    startTime = datetime.datetime.strptime(entertime, '%Y-%m-%d %H:%M:%S')
    #begin= '2017-05-24 23:59:57'
    #beginTime = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
    #print startTime
    while True:
        print 'The next start time :',startTime
        while datetime.datetime.now() < startTime:
            minus_time = startTime - datetime.datetime.now()
            sleep_time = minus_time.days*86400+minus_time.seconds
            #print 'beginTime',beginTime
            #print 'startTime',startTime
            time.sleep(sleep_time)
            #beginTime = beginTime+second

        storeDate = datetime.datetime.now().strftime('%Y-%m-%d')
        blacklist_dir = source_store_path[1]+source_store_path[0]+'-'+storeDate+".json"
        # print blacklist_dir
        blacklist_Trie_dir = trie_store_path[1]+trie_store_path[0]+'-'+storeDate+".json"
        # print blacklist_Trie_dir

        if not (os.path.exists(blacklist_dir) and os.path.exists(blacklist_Trie_dir)):
            store_run(storeDate)

        try:
            print("Checking the DNS."),time.ctime()
            # execute the command
            gte = (startTime-delta-delta).strftime('%Y-%m-%d %H:%M:%S')
            lte = (startTime).strftime('%Y-%m-%d %H:%M:%S')
            timestamp = (startTime).strftime('%Y-%m-%dT%H:%M:%S.%f')+"+08:00"

            TrieSearch.main(gte,lte,timestamp)

            # command = r'python TrieSearch.py "%s" "%s" "%s"' %(gte,lte,timestamp)
            # status = os.system(command)
            print("-"*25+'DONE'+"-"*25),time.ctime()
            # print("Command status = %s."%status)
            startTime = startTime+delta
        except Exception, e:
            print e

if __name__=="__main__":
    # entertime = '2018-03-15 15:30:00'
    entertime = frequency[0]
    delta = frequency[1]
    run(delta = delta,entertime = entertime)
