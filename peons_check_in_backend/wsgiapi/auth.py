from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/register", methods=["POST"])
@check_session_auth(authentication=False, authorization=False)
def register():
    data: dict = request.get_json()
    if data is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    mail = data.get("mail", None)
    password = data.get("password", None)
    info = data.get("info", None)

    if mail is None or password is None or info is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    if auth.exist(mail):
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "mail already exist",
        }
        return jsonify(ret), ret["status"]

    try:
        user_id = auth.register(mail, password, info)
    except auth.AuthError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]

    ret = {
        "status": HTTPStatus.OK,
        "msg": "register",
        "user_id": user_id,
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/login", methods=["POST"])
@check_session_auth(authentication=False, authorization=False)
def login():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    mail = data.get("mail", None)
    password = data.get("password", None)

    if mail is None or password is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    try:
        session_id = auth.login(mail, password)
    except auth.AuthNotActiveError as e:
        ret = {
            "status": HTTPStatus.UNAUTHORIZED,
            "msg": "User not active",
        }
        return jsonify(ret), ret["status"]
    except auth.AuthError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "login failed",
        }
        return jsonify(ret), ret["status"]

    if session_id is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "login failed",
        }
    else:
        ret = {
            "status": HTTPStatus.OK,
            "msg": "login success",
            "session_id": session_id,
        }
    return jsonify(ret), ret["status"]


@auth_api.route("/check_session", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def check_session():
    ret = {
        "status": HTTPStatus.OK,
        "msg": "session is valid",
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/check_admin", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["admin"])
def check_admin():
    ret = {
        "status": HTTPStatus.OK,
        "msg": "admin is valid",
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/logout", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def logout():
    session_id = request.headers.get("SESSION-ID")
    auth.logout(session_id)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "logout",
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/change_password", methods=["POST"])
@check_session_auth(authentication=True, authorization=False)
def change_password():
    session_id = request.headers.get("SESSION-ID")
    data = request.get_json()
    if data is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    old_password = data.get("old_password", None)
    new_password = data.get("new_password", None)

    if old_password is None or new_password is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    try:
        auth.change_password(session_id, old_password, new_password)
    except auth.AuthError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]

    ret = {
        "status": HTTPStatus.OK,
        "msg": "change password success",
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/administer", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["admin"])
def administer():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    user_id = data.get("user_id", None)

    if user_id is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    try:
        auth.administer(user_id)
    except auth.AuthError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]

    ret = {
        "status": HTTPStatus.OK,
        "msg": "administer",
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/revoke_admin", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["admin"])
def revoke_admin():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    user_id = data.get("user_id", None)

    if user_id is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    try:
        auth.revoke_admin(user_id)
    except auth.AuthError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]

    ret = {
        "status": HTTPStatus.OK,
        "msg": "administer",
    }
    return jsonify(ret), ret["status"]
