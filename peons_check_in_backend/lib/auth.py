import hashlib
from datetime import timedelta
from uuid import uuid4

from aclaaa import session

from peons_check_in_backend.lib import user
from peons_check_in_backend.db import auth


class AuthError(Exception):
    pass


def exist(mail):
    return auth.exist(mail)


def hash_password(password, salt):
    target = (password + salt).encode("utf-8")
    return hashlib.sha512(target).hexdigest()


def register(mail, password, info: dict):
    permissions = [
        "api_worker",
    ]
    salt = str(uuid4().hex)
    hashed_password = hash_password(password, salt)
    user_id = str(uuid4())
    account = {
        "user_id": user_id,
        "mail": mail,
        "hashed_password": hashed_password,
        "salt": salt,
    }
    for permission in permissions:
        account[permission] = 1
    auth.insert(account)

    info["mail"] = mail

    try:
        new_user = user.User(user_id, info)
        user.create_user(new_user)
    except user.UserError as e:
        auth.delete(mail)
        raise AuthError(e)


def create_session_id():
    return str(uuid4())


def login(mail, password):
    account = auth.get(mail)
    if account is None:
        raise AuthError("user not found")
    user_id = account["user_id"]
    if not user.is_user_active(user_id):
        raise AuthError("user not active")
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


def change_password(session_id, old_password, new_password):
    user_id = get_user_id(session_id)
    account = auth.get_by_user_id(user_id)
    if account is None:
        raise AuthError("user not found")
    password = hash_password(old_password, account.get("salt", ""))
    if password != account["hashed_password"]:
        raise AuthError("wrong password")
    new_password = hash_password(new_password, account.get("salt", ""))
    auth.update_password(account["mail"], new_password)
