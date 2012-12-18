#!/bin/env python
import ConfigParser
import os
import frame

PATH = os.path.dirname(os.path.abspath(__file__)) + '/'

db_file = 'db.cfg'
db_file = PATH + 'conf/' + db_file

keys = ['type','host','port']
defaults = ['redis','localhost','6379']

#Databases
trans   = 0 #trans stores all transactions across all databases as well as salt info for hashes
user    = 1
session = 2
test    = 9

class dbConfig:
    def check(self):
        try:
            if os.path.exists(db_file)==False:
                self.write()          
        except IOError as e:
            self.write()

    def read(self):
        config = ConfigParser.RawConfigParser()
        config.read(db_file)
        dbtype = config.get('Database',keys[0])
        host = config.get('Database',keys[1])
        port = config.get('Database',keys[2])
        self.Obj= {'type':dbtype, 'host':host, 'port':int(port)}
        return self.Obj
    
    def write(self):
        config = ConfigParser.RawConfigParser()
        section = 'Database'
        config.add_section(section)
        config.set(section, keys[0], defaults[0])
        config.set(section, keys[1], defaults[1])
        config.set(section, keys[2], defaults[2])
        with open(db_file, 'wb') as configfile:
            config.write(configfile)
        
    def __init__(self):
        self.Obj = {}
        self.check()
        self.read()

DEBUG = 1
if __name__ == '__main__':
    if DEBUG == 1:
        conf = dbConfig()
        conf.check()
        conf.read()
        print conf.Obj
        print conf.Obj['type']
