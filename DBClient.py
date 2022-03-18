import pymongo
from WatchOffer import WatchOffer

from WatchTimestamp import WatchTimestamp 

class DBClient:

    def __init__(self, uri: str):
        self.uri = uri
        self.client = pymongo.MongoClient(self.uri)
        self.watchTimestamp_collection = self.client.rku.watchtimestamps
        self.watchSnapshot_collection = self.client.rku.watchoffersnapshots

    def push_watchTimestamp(self, wt: WatchTimestamp):
        self.watchTimestamp_collection.insert_one(wt.pushable())

    def push_watchOfferSnapshot(self, wo: WatchOffer):
        self.watchSnapshot_collection.insert_one(wo.__dict__)

    def drop_watchOfferSnapshots(self):
        self.watchSnapshot_collection.drop()

