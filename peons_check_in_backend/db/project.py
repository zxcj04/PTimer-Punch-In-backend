from aclmongo.connector.session import MongoSession

COLLECTION_NAME = "project"


def insert(project):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.insert_one(project)


def get(project_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"project_id": project_id}, {"_id": 0})
        return ret


def listProjects():
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find({}, {"_id": 0})
        return list(ret)


def exist(project_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        ret = col.find_one({"project_id": project_id}, {"_id": 0})
        if ret is None:
            return False
        else:
            return True


def update(project_id, new_project):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one({"project_id": project_id}, {"$set": new_project})


def recover(project_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(
            {"project_id": project_id}, {"$unset": {"is_delete": ""}}
        )


def virtual_delete(project_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(
            {"project_id": project_id}, {"$set": {"is_delete": True}}
        )


def delete(project_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.delete_one({"project_id": project_id})
