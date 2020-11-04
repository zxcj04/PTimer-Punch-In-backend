from pymongo import MongoClient


_MONGO_DB = None


def setup(config: dict):
    global _MONGO_DB
    user = config.get("user")
    pwd = config.get("pwd")
    host = config.get("host")
    port = config.get("port", 27017)
    db_name = config.get("db")
    auth_db = config.get("auth_db", "admin")
    connection_info = f"mongodb://{user}:{pwd}@{host}:{port}/{auth_db}"
    _MONGO_DB = MongoClient(connection_info)[db_name]


def get_mongo_db():
    return _MONGO_DB
