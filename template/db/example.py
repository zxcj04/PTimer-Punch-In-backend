from aclmongo.connector.session import MongoSession


def insert():
    with MongoSession() as session:
        col = session.getCollection("dev")
        col.insert_one({"ping": "pong"})
