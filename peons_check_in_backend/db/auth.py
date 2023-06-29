from aclmongo.connector.session import MongoSession

COLLECTION_NAME = "auth"


def insert(account):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.insert_one(account)


def get(mail):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"mail": mail}, {"_id": 0})
        return ret


def get_by_user_id(user_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"user_id": user_id}, {"_id": 0})
        return ret


def exist(mail):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"mail": mail}, {"_id": 0})
        if ret is None:
            return False
        else:
            return True


def update_permission(user_id, permission, active: bool):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        if active:
            col.update_one({"user_id": user_id}, {"$set": {permission: True}})
        else:
            col.update_one({"user_id": user_id}, {"$unset": {permission: ""}})


def update(account, new_account):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(account, {"$set": new_account})


def update_password(mail, new_password):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one({"mail": mail}, {"$set": {"hashed_password": new_password}})


def virtual_delete(mail):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one({"mail": mail}, {"$set": {"is_delete": True}})


def recover(mail):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one({"mail": mail}, {"$unset": {"is_delete": ""}})


def delete(mail):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.delete_one({"mail": mail})
