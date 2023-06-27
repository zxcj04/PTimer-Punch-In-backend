from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/register", methods=["POST"])
@check_session_auth(authentication=False, authorization=False)
def register():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    mail = data.get("mail", None)
    name = data.get("name", None)
    password = data.get("password", None)

    if mail is None or name is None or password is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST

    if auth.exist(mail):
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "login failed",
        }
        return jsonify(ret), ret["status"]

    auth.register(mail, name, password)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "register",
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
    except auth.AuthError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "login failed",
        }
        return jsonify(ret), ret["status"]

    if session_id is None:
        ret = {
            "status": HTTPStatus.UNAUTHORIZED,
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
