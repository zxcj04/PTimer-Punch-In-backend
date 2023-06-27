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


def update(project, new_project):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.update_one(project, {"$set": new_project})


def delete(project_id):
    with MongoSession() as session:
        col = session.getCollection(COLLECTION_NAME)
        col.delete_one({"project_id": project_id})
