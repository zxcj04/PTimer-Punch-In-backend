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


def get_user_punch_list(user_id, start=None, end=None, limit=0):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        findFilter = {}
        if user_id:
            findFilter["user_id"] = user_id
        if start and end:
            findFilter["$or"] = [
                {
                    "punch_in_time": {
                        "$gte": start,
                        "$lte": end,
                    }
                },
                {
                    "punch_out_time": {
                        "$gte": start,
                        "$lte": end,
                    }
                },
            ]
        records = col.find(
            findFilter,
            {"_id": 0},
            [("record_time", -1)],
            limit=limit,
        )
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
        col.update_one({"punch_id": record_id, "is_delete": {"$ne": True}}, {"$set": new_record})


def update_punch_out_time(record_id, punch_out_time):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(
            {"punch_id": record_id, "is_delete": {"$ne": True}},
            {"$set": {"punch_out_time": punch_out_time}},
        )


def recover(record_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(
            {"punch_id": record_id}, {"$unset": {"is_delete": ""}}
        )


def virtual_delete(punch_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(
            {"punch_id": punch_id}, {"$set": {"is_delete": True}}
        )


def delete(punch_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.delete_one({"punch_id": punch_id})
