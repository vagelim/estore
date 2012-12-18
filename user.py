#!/bin/env python
#User class for an object to maintain user state
import frame
import hashlib
import random
import dbConfig
import login

conf = dbConfig.dbConfig()
auth = frame.frame(conf.Obj['host'], conf.Obj['port'], dbConfig.user)
session = frame.frame(conf.Obj['host'], conf.Obj['port'], dbConfig.session)
TTL = 300

class User:
    def __init__(self, username=None,userID=None):
        self.username = username
        self.userID = userID
        if self.userID == None:
            self.userID = login.getuserID(username)
        else:
            self.userID = userID

        self.sessionID = 0
        self.items = {}#itemID:item_name
        #self.wallet = {} #dictionary of BTC wallet <nickname>:<addr>
    def populate(self):
        
        self.userID = login.getuserID(self.username)
        #Cast to string to get first digits, cast to int for use as sessionID
        self.sessionID = int(str(random.getrandbits(128))[:17])
        session_key = str(self.sessionID)
        user_key = str(self.userID)
        session.store(session_key, self.userID)
        session.store(user_key, self.sessionID)
        session.expire(session_key, TTL)
        session.expire(user_key, TTL)
        
    def create(self,username,password):
        """Takes username and hashed password"""
        userID = auth.incr('userID')
        if userID == False: #If key does not exist to increment
            auth.store('userID', 86)
            self.userID = auth.check('userID')

        self.sessionID = int(str(random.getrandbits(128))[:17])
        print self.userID
        print self.sessionID
        session_key = "session:" + str(self.sessionID)
        user_key = "session:" + str(self.userID)
        #check the following to see if it does not attempt an overwrite (hence sstore() not store())
        print auth.sstore('user:'+ username, self.userID)
        print auth.hstore('user:'+ str(self.userID), 'password', password)
        print auth.hstore('user:'+ str(self.userID), 'username', username)
        print session.store(session_key, self.userID)
        print session.store(user_key, self.sessionID)
        print session.expire(session_key, TTL)
        print session.expire(user_key, TTL)
