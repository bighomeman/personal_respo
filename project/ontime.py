#!/usr/bin/python

import os
import time
import datetime
from configuration import set_data_path,set_frequency,logger_info,logger_error
import TrieSearch,merge_blacklist

data_path = set_data_path()
frequency = set_frequency()

def store_run(storeDate):
    try:
        logger_info.info("Download starting.")

        merge_blacklist.main(storeDate)

        logger_info.info("Download completed.")

    except Exception, e:
        logger_error.error("Download failed.\n{0}".format(e))

def run():
    entertime = frequency[0]
    delta = frequency[1]

    startTime = datetime.datetime.strptime(entertime, '%Y-%m-%d %H:%M:%S')
    #begin= '2017-05-24 23:59:57'
    #beginTime = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
    #print startTime
    logger_info.info("Starting theat DNS checking.")
    while True:
        logger_info.info("The next start time :{0}".format(startTime))
        if datetime.datetime.now() < startTime:
            minus_time = startTime - datetime.datetime.now()
            sleep_time = minus_time.days*86400+minus_time.seconds
            # print sleep_time
            time.sleep(sleep_time)

        storeDate = datetime.datetime.now().strftime('%Y-%m-%d')
        blacklist_dir = os.path.join(data_path,'source'+'-'+storeDate+".json")
        # print blacklist_dir
        blacklist_Trie_dir = os.path.join(data_path,'trie'+'-'+storeDate+".json")
        # print blacklist_Trie_dir

        if not (os.path.exists(blacklist_dir) and os.path.exists(blacklist_Trie_dir)):
            store_run(storeDate)

        try:
            logger_info.info("Checking the DNS.")
            # execute the command
            gte = (startTime-delta).strftime('%Y-%m-%d %H:%M:%S')
            lte = (startTime).strftime('%Y-%m-%d %H:%M:%S')

            if time.daylight == 0:
                time_zone = "%+03d:%02d" % (-(time.timezone/3600),time.timezone%3600/3600.0*60)
            else:
                time_zone = "%+03d:%02d" % (-(time.altzone/3600),time.altzone%3600/3600.0*60)

            timestamp = (startTime).strftime('%Y-%m-%dT%H:%M:%S.%f')+time_zone

            TrieSearch.main(gte,lte,timestamp,time_zone)

            # command = r'python TrieSearch.py "%s" "%s" "%s"' %(gte,lte,timestamp)
            # status = os.system(command)
            logger_info.info("Checking completed.")
            # print("Command status = %s."%status)
            startTime = startTime+delta
        except Exception, e:
            logger_error.error("Checking failed.\n{0}".format(e))

if __name__=="__main__":
    run()
