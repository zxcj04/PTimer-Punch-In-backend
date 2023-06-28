from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth, user

user_api = Blueprint("user_api", __name__)


@user_api.route("/info", methods=["GET"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def info():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    user_info = user.get_user(user_id)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "get user info success",
        "user_info": user_info,
    }
    return jsonify(ret), ret["status"]


@user_api.route("/projects", methods=["GET"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def projects():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    projects = user.get_user_projects(user_id)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "get user projects success",
        "projects": projects,
    }
    return jsonify(ret), ret["status"]


@user_api.route("/update", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def update():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    data = request.get_json()
    user_info = data.get("user_info", None)
    if user_info is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "invalid request",
        }
        return jsonify(ret), ret["status"]
    try:
        user.update_user(user_id, user_info)
    except user.UserError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "update user info success",
    }
    return jsonify(ret), ret["status"]
