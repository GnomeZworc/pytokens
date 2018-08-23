# pytokens
# create by gnomezworc
#
#!/usr/bin/python3

import datetime

from pymongo import MongoClient

class mongo():
    connect = None
    db = None
    api_name = None

    def __init__(self, host='127.0.0.1', port='80', database='database', protocol='mongodb', api=''):
        self.api_name = api
        self.connect = MongoClient(protocol + "://" + host + ":" + port + "/")
        self.db = self.connect[database]
        self.logs("api start")
    def close(self):
        self.connect.close()
        self.logs("api stop")
    def logs(self, message):
        elem = {}
        elem["timestamp"] = datetime.datetime.now()
        elem["message"] = message
        self.db[self.api_name + "_logs"].insert_one(elem)
    def insert(self, collection, elem):
        collection = self.api_name + "_" + collection
        self.db[collection].insert_one(elem)
        self.logs("add elem in " + collection)
    def findOne(self, collection, find):
        collection = self.api_name + "_" + collection
        self.logs("find one " + str(find) + " in " + collection)
        return self.db[collection].find_one(find)
