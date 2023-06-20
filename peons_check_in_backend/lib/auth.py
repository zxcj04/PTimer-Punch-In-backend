import hashlib
from datetime import timedelta
from uuid import uuid4

from aclaaa import session

from peons_check_in_backend.db import auth


def exist(mail):
    return auth.exist(mail)


def hash_password(password, salt):
    target = (password + salt).encode("utf-8")
    return hashlib.sha512(target).hexdigest()


def register(mail, name, password):
    permissions = [
        "api_worker",
    ]
    salt = str(uuid4().hex)
    hashed_password = hash_password(password, salt)
    account = {
        "user_id": str(uuid4()),
        "mail": mail,
        "name": name,
        "hashed_password": hashed_password,
        "salt": salt,
    }
    for permission in permissions:
        account[permission] = 1
    auth.insert(account)


def create_session_id():
    return str(uuid4())


def login(mail, password):
    account = auth.get(mail)
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


def get_user_id(session_id):
    _session = session.get()
    account = _session.hgetall(session_id)
    account = {
        k.decode("utf-8"): v.decode("utf-8") for k, v in account.items()
    }
    return account["user_id"]
