#!/bin/env python
import frame as frame

import dbConfig as dbConfig
import user as usr
import hashlib

conf = dbConfig.dbConfig()
host = conf.Obj['host']
port = conf.Obj['port']
auth = frame.frame(host, port, dbConfig.user)
session = frame.frame(host, port, dbConfig.session)
salt = frame.frame(host, port, dbConfig.trans)

def valid_username(username):
    userID = auth.check(username) 
    if userID == False:
        return True

def valid_login(username, password):
    #Check if username exists in db
    userID = auth.check('user:'+ username) 
    if userID == False:
        return False
    stored_salt = salt.checkSalt()
    salt_pass = hashlib.sha256(stored_salt + password).hexdigest()
    stored_pass = auth.r.hget('user:' + userID, 'password')
    if stored_pass == salt_pass:
        return True
    else:
        return False

def logmein(username=None):
    if username == None:
        return False
    user = usr.User(username=username)
    user.populate()
    return user

def create_login(username,password):
    user = usr.User(username=username)
    user.create(username, password)

def verifySession(userID,sessionID,User=None):
    """verifySession(User, userID, sessionID) must have a User obj"""
    if User == None:
        return False
    user = usr.User()
    if userID == None:
        if sessionID != user.sessionID:
            return False
        sessionID = 'session:' + str(sessionID)
        current = session.check(sessionID) 
        if current!= None:
            if user.sessionID == current:
                return True
            else:
                return False
        else:#if current sessionID does not exist in database
            #do some cleanup of keys just in case
            return False


def getuserID(username):
    return auth.check(username)


def saltPassword(password):
    salt = frame.frame(host, port, dbConfig.trans)
    salt_seed = salt.checkSalt()
    return hashlib.sha256(salt_seed + password).hexdigest()




    



