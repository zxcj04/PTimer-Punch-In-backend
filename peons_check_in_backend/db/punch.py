from aclmongo.connector.session import MongoSession


COLLECTION_NAME = "punch"


def insert(record):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.insert_one(record)


def get(punch_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"punch_id": punch_id}, {"_id": 0})
        return ret


def get_user_active_punch(user_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        records = col.find({"user_id": user_id}, {"_id": 0}, [("punch_in_time", -1)])
        records = list(records)
        if len(records) == 0:
            return None
        record = records[0]
        if record is None:
            return None
        elif record.get("punch_out_time", None) is not None:
            return None
        return record


def get_user_all_punch(user_id, limit=50):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        records = col.find({"user_id": user_id}, {"_id": 0}, [("punch_in_time", -1)], limit=limit)
        records = list(records)
        return records


def get_all_punch(limit=50):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        records = col.find({}, {"_id": 0}, [("punch_in_time", -1)], limit=limit)
        records = list(records)
        return records


def exist(punch_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"punch_id": punch_id}, {"_id": 0})
        if ret is None:
            return False
        else:
            return True


def update(record_id, new_record):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one({"punch_id": record_id}, {"$set": new_record})


def update_punch_out_time(record_id, punch_out_time):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one({"punch_id": record_id}, {"$set": {"punch_out_time": punch_out_time}})
