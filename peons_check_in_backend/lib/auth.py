from uuid import uuid4
import hashlib
from datetime import timedelta

from aclaaa import session

from peons_check_in_backend.db import auth


def exist(name):
    return auth.exist(name)


def hash_password(password, salt):
    target = (password + salt).encode('utf-8')
    return hashlib.sha512(target).hexdigest()


def register(name, password):
    permissions = [
        "api_worker",
    ]
    salt = str(uuid4().hex)
    hashed_password = hash_password(password, salt)
    account = {
        "name": name,
        "hashed_password": hashed_password,
        "salt": salt,
    }
    for permission in permissions:
        account[permission] = 1
    auth.insert(account)


def create_session_id():
    return str(uuid4())


def login(name, password):
    account = auth.get(name)
    password = hash_password(password, account.get("salt", ""))
    if password != account["hashed_password"]:
        return None
    else:
        session_id = create_session_id()

        session_content = account
        del session_content["hashed_password"]
        del session_content["salt"]

        expire_time = timedelta(days=30)

        _session = session.get()
        _session.hmset(name=session_id, mapping=session_content)
        _session.expire(name=session_id, time=expire_time)
        return session_id


def logout(session_id):
    _session = session.get()
    _session.delete(session_id)
