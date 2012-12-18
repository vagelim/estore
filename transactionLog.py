#!/bin/env python
import redis
from easygui import *
import frame as frame
from time import time,ctime
import dbConfig as dbConfig


conf = dbConfig.dbConfig()
r = redis.StrictRedis(conf.Obj['host'], conf.Obj['port'], dbConfig.trans)


DEBUG = 1

TEST = "@TEST"
USER_TRANS = ":trans" #uid + USER_TRANS is the user transaction key
USER_COUNT = ":trans:count"
TRANS       = "@TRANS"
TRANS_COUNT = "@TRANS_C"
#transactionLog is to be called by every operation before performing its duties
#Will log to redis under key "@TRANS" by default
#Logs to file only if specified
def transactionLog(key,value="NA",operation=None,file=None,timestamp=time(),uid=None):
    """transactionLog(key,value=None,operation=None,file=None,timestamp=time(),user=None)
    Returns current transaction counter"""
    if DEBUG == 1:
        return 0
    if key == TEST:#If testing, do not log transactions
        return 0
    #IMPORTANT!! current_transaction will be zero upon install
    #This special case is the reason for this try,exception block
    try:
        current_transaction = int(r.get(TRANS_COUNT)) + 1
    except TypeError:
        r.set(TRANS_COUNT,0)
        current_transaction = 0
    key   = "[" + key + "]"
    try:
        value = "(" + value + ")"
    except TypeError:
        value = "(" + str(value) + ")"
    operation = "{" + operation + "}"
    transaction = str(current_transaction) + ":" + key + value + "-" + operation + ":" + str(timestamp)
    if file == None:
        if uid != None:
            user_key = uid + USER_TRANS
            r.lpush(user_key, transaction)
        r.lpush(TRANS, transaction)
    
    #NOTE: The transaction file is from oldest to latest, while the database is opposite
    else:
        handle = open(file,'a')
        handle.write(transaction)
        handle.close()
        
    if uid != None:
        user_count = user + USER_COUNT
        return r.incr(user_count)
    return r.incr(TRANS_COUNT)

def resetLog():
    delete(TRANS)
    delete(TRANS_COUNT)
