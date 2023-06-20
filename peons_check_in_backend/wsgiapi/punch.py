from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth, punch


punch_api = Blueprint("punch_api", __name__)


@punch_api.route("/in", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def punch_in():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    punch_id, punch_time = punch.punch_in(user_id)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "punch in success",
        "punch_id": punch_id,
        "punch_time": punch_time,
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/out", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def punch_out():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    punch_time = punch.punch_out(user_id)
    if punch_time is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "not punch in yet",
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "punch out success",
        "punch_time": punch_time,
    }
    return jsonify(ret), ret["status"]
