import pymongo


class MongodbDriver(object):

    def __init__(self, db='device', collection='change_compare'):
        self.client = pymongo.MongoClient('127.0.0.1', 27017)
        self.db = self.client[db]
        self.col = self.db[collection]

    def insert(self, content):
        return self.col.insert(content)

    def find(self, sort_by, **filters,):
        data = self.col.find(filters)
        if sort_by:
            data.sort(sort_by, pymongo.DESCENDING)
        return data