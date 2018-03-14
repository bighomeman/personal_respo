#!/usr/bin/python

import os
import time
import datetime


second = datetime.timedelta(seconds=1)
day = datetime.timedelta(days=1)

def store_run():
    entertime = time.strftime("%Y-%m-%d %H:%M:%S")
    startTime = datetime.datetime.strptime(entertime, '%Y-%m-%d %H:%M:%S')
    #begin= '2017-05-24 23:59:57'
    #beginTime = datetime.datetime.strptime(begin, '%Y-%m-%d %H:%M:%S')
    #print startTime
    while True:
        print 'The next start time :',startTime
        while datetime.datetime.now() < startTime:
            #print 'beginTime',beginTime
            # print 'startTime',startTime
            time.sleep(1)
            #beginTime = beginTime+second
        try:
            print("Starting command."),time.ctime()
            # execute the command
            storeDate = (startTime).strftime('%Y-%m-%d')
            command = r'python merge_blacklist.py "%s"' %(storeDate)
            status = os.system(command)
            print('done'+"-"*100),time.ctime()
            print("Command status = %s."%status)
            startTime = startTime+day
        except Exception, e:
            print e

def run(entertime,delta,server='172.17.0.68'):

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
    entertime = '2018-03-12 17:50:00'
    delta = datetime.timedelta(minutes=5)
    run(entertime,delta,server = '172.23.2.143')
    # store_run()