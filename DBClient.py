import pymongo

from WatchTimestamp import WatchTimestamp 

class DBClient:

    def __init__(self, uri: str):
        self.uri = uri
        self.client = pymongo.MongoClient(self.uri)
        self.watchTimestamp_collection = self.client.rku.watchtimestamps

    def push_watchTimestamp(self, wt: WatchTimestamp):
        self.watchTimestamp_collection.insert_one(wt.pushable())

