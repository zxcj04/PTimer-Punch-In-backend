from aclmongo.connector.session import MongoSession


COLLECTION_NAME = "auth"


def insert(account):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.insert_one(account)


def get(name):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"name": name}, {"_id": 0})
        return ret


def exist(name):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"name": name}, {"_id": 0})
        if ret is None:
            return False
        else:
            return True


def update(account, new_account):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(account, {"$set": new_account})
