import logging

from .connect import get_mongo_db
from .collection import MongoCollection

_LOGGER = logging.getLogger("connector.session")


class MongoSession(object):
    def __init__(self):
        self.db = get_mongo_db()

    def close(self):
        try:
            self.db = None
        except Exception as e:
            _LOGGER.warning("mongodb got %s when closing, ignored.", str(e))

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def getCollection(self, collection_name) -> MongoCollection:
        return MongoCollection(self.db.get_collection(collection_name))
