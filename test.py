#!/bin/env python
import frame as frame
import dbConfig as dbConfig


def test():
    conf = dbConfig.dbConfig()
    host = conf.Obj['host']
    port = conf.Obj['port']
    testDB = dbConfig.test
    print 'Host: ' + host
    print 'Port: ' + str(port)

    test = frame.frame(host,port,testDB)

    
    key1 = 'key1'
    key2 = 'key2'
    value1 = 'value1'
    value2 = 'value2'

    print 'Append to NonExistent Key (F): ' + str(test.append(key1,value1))
    print 'Create New Key (T): ' + str(test.store(key1,value1))
    print 'Append to Existent Key (T): ' + str(test.append(key1,value2, ','))
    print 'Print Appended Key value ("value1,value2"): ' + str(test.check(key1))
    print 'Check Key exists (T): ' + str(test.exists(key1))
    print 'Delete Key (T): ' + str(test.delete(key1))
    print 'Check NonExistent Key (F): ' + str(test.exists(key1))

if __name__ == '__main__':
    test()
