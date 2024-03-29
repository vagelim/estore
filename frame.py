#This is a framework providing support functions
import redis
import transactionLog as Trans
import random
import hashlib



class frame:
    def __init__(self, host, port, db):
        self.r = redis.StrictRedis(host, port, db)

    def append(self,key,value,delimiter=None):#Appends data to given key
        """append(key,value,delimiter=None)"""
        #Get current value and store it
        current = self.r.get(key)
        new_value = current
        if self.r.exists(key) == False:
            return False
        
        if delimiter == None:
            new_value = new_value + value
        else:
            new_value = new_value + delimiter + value
        
        Trans.transactionLog(key,new_value, "A")
        self.r.set(key,new_value)
        return True

    def prepend(self,key,value,delimiter=None):#Prepends data to given key
        """prepend(key,value,delimiter=None)"""
        #Get current value and store it
        current = self.r.get(key)
        new_value = current
        if current == None:
            return False
        
        if delimiter == None:
            new_value = value + new_value
        else:
            new_value = value + delimiter + new_value
        
        Trans.transactionLog(key,new_value, "P")
        self.r.set(key,new_value)
        return True

    #Secure Store
    def sstore(self,key,value):#Stores a value only if the key does not exist
        """sstore(key,value) Returns False if value exists"""
        if self.r.exists(key):
            return False
        else:
            Trans.transactionLog(key,value, "SS")
            self.r.set(key,value)
            return True

    def store(self,key,value,uid=None):#Default store, no checking
        Trans.transactionLog(key,value, "S",uid=uid)
        self.r.set(key,value)
        return True
    
    def multiStore(self,dictionary,uid=None):#Store multiple values
        """multiStore(dictionary) takes a dictionary of keys,values to store"""
        for each in dictionary:
            store(each,dictionary[each],uid=uid)
        
    def check(self,key):#Check key value (logs to transaction log)
        Trans.transactionLog(key,operation="C")
        if self.r.get(key) != None:
            return self.r.get(key)
        else:
            return False
    def delete(self,key):
        if self.r.exists(key):
            Trans.transactionLog(key,operation="D")
            self.r.delete(key)
            return True
        else:
            return False
    def exists(self,key):
        if self.r.exists(key):
            return True
        else:
            return False
    #Check the @SALT! key
    def checkSalt(self):
        """Returns the current salt if it exists, otherwise creates a new salt"""
    
        if self.r.exists('@SALT!'):
            return self.r.get('@SALT!')
            
        else:
            salt_seed = str(random.getrandbits(128))
            salt = hashlib.sha256(salt_seed).hexdigest()
            self.store('@SALT!',salt)
            return salt
    def incr(self,key):#Increment
        if self.r.exists(key) == False:
            return False
        self.r.incr(key)
        Trans.transactionLog(key,"NA",operation="INCR")
        return self.r.check(key)
    #Parse strings with the specified character as the delimiter, returning the first occurrence after the delimiter
    def parseString(self,string, delimiter):
        parsed   = string[:string.find(delimiter)]
        leftover = string[string.find(delimiter) +1 :] #The +1 is necessary because the first arg is inclusive
        return {'parsed':parsed,'leftover':leftover}


    def expire(self,key,ttl):
        self.r.expire(key,ttl)
        return ttl


    def hstore(self,key,field,value):
        self.r.hset(key,field,value)
        return True
