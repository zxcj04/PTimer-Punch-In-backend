from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth

auth_api = Blueprint("auth_api", __name__)


@auth_api.route("/register", methods=["POST"])
@check_session_auth(authentication=False, authorization=False)
def register():
    data = request.get_json()
    name = data["name"]
    password = data["password"]

    if auth.exist(name):
        return jsonify({"message": "user already exist"}), HTTPStatus.BAD_REQUEST

    auth.register(name, password)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "register",
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/login", methods=["POST"])
@check_session_auth(authentication=False, authorization=False)
def login():
    data = request.get_json()
    name = data["name"]
    password = data["password"]
    session_id = auth.login(name, password)
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
@check_session_auth(authentication=True, authorization=False)
def check_session():
    ret = {
        "status": HTTPStatus.OK,
        "msg": "session is valid",
    }
    return jsonify(ret), ret["status"]


@auth_api.route("/logout", methods=["POST"])
@check_session_auth(authentication=True, authorization=False)
def logout():
    session_id = request.headers.get("SESSION-ID")
    auth.logout(session_id)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "logout",
    }
    return jsonify(ret), ret["status"]
