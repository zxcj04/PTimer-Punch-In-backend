from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.db import example

hello_api = Blueprint("hello_api", __name__)


@hello_api.route("")
@check_session_auth(authentication=False, authorization=False)
def hello():
    example.insert()
    ret = {
        "status": HTTPStatus.OK,
        "msg": "hello",
    }
    return jsonify(ret), ret["status"]
