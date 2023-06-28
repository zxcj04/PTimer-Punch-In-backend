from aclmongo.connector.session import MongoSession

COLLECTION_NAME = "user"


def insert(user):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.insert_one(user)


def get(user_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"user_id": user_id}, {"_id": 0})
        return ret


def exist(user_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"user_id": user_id}, {"_id": 0})
        if ret is None:
            return False
        else:
            return True


def update(user_id, new_user):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one({"user_id": user_id}, {"$set": new_user})


def delete(user_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.delete_one({"user_id": user_id})
