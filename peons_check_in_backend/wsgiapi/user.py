from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import auth, user

user_api = Blueprint("user_api", __name__)


@user_api.route("/info", methods=["POST"])
@check_session_auth(authentication=True, authorization=False)
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
