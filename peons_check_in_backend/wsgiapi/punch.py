from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth, punch, project

punch_api = Blueprint("punch_api", __name__)


@punch_api.route("/in", methods=["POST"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def punch_in():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "invalid request"}), HTTPStatus.BAD_REQUEST
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    project_id = data.get("project_id", None)
    if project_id is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "missing key: project_id",
        }
        return jsonify(ret), ret["status"]
    if not project.exist(project_id):
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "project not found",
        }
        return jsonify(ret), ret["status"]
    try:
        punch_id, punch_time = punch.punch_in(user_id, project_id)
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


@punch_api.route("/list", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def get_all_punch():
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    start = request.args.get("start", None)
    end = request.args.get("end", None)
    records = punch.get_user_punch_list(user_id, start, end)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "get all punch success",
        "punches": records,
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/update", methods=["POST"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def update_punch():
    data = request.get_json()
    session_id = request.headers.get("SESSION-ID", None)
    user_id = auth.get_user_id(session_id)
    punch_id = data.get("punch_id", None)
    new_punch = data.get("punch", None)
    if punch_id is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "missing key: punch_id",
        }
        return jsonify(ret), ret["status"]
    if new_punch is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "missing key: punch",
        }
        return jsonify(ret), ret["status"]
    try:
        punch.update_punch(punch_id, new_punch)
    except punch.PunchError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "update punch success",
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/delete", methods=["POST"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["worker"]
)
def delete_punch():
    data = request.get_json()
    punch_id = data.get("punch_id", None)
    if punch_id is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "missing key: punch_id",
        }
        return jsonify(ret), ret["status"]
    try:
        punch.delete_punch(punch_id)
    except punch.PunchError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "delete punch success",
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/admin/recover", methods=["POST"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["admin"]
)
def admin_recover_punch():
    data = request.get_json()
    punch_id = data.get("punch_id", None)
    if punch_id is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "missing key: punch_id",
        }
        return jsonify(ret), ret["status"]
    try:
        punch.recover_punch(punch_id)
    except punch.PunchError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "recover punch success",
    }
    return jsonify(ret), ret["status"]


@punch_api.route("/admin/list", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["admin"]
)
def admin_get_all_punch():
    start = request.args.get("start", None)
    end = request.args.get("end", None)
    records = punch.get_all_punch(start, end)
    ret = {
        "status": HTTPStatus.OK,
        "msg": "admin get all punch success",
        "punches": records,
    }
    return jsonify(ret), ret["status"]
