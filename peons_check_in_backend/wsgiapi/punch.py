from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth, punch

punch_api = Blueprint("punch_api", __name__)


@punch_api.route("/in", methods=["POST"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def punch_in():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    try:
        punch_id, punch_time = punch.punch_in(user_id)
    except punch.PunchError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "punch in success",
        "punch_id": punch_id,
        "punch_time": punch_time,
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/out", methods=["POST"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def punch_out():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    try:
        punch_time = punch.punch_out(user_id)
    except punch.PunchError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "punch out success",
        "punch_time": punch_time,
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/active", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def get_active_punch():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    try:
        record = punch.get_user_active_punch(user_id)
    except punch.PunchError as e:
        ret = {"status": HTTPStatus.BAD_REQUEST, "msg": str(e)}
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "get active punch success",
        "punch": record,
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/all", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def get_all_punch():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    records = punch.get_user_all_punch(user_id)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "get all punch success",
        "punches": records,
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/admin_all", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["admin"]
)
def admin_get_all_punch():
    records = punch.get_all_punch()
    ret = {
        "status": HTTPStatus.OK,
        "msg": "admin get all punch success",
        "punches": records,
    }
    return jsonify(ret), ret["status"]
