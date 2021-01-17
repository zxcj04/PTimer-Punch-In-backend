from flask import Blueprint, request, jsonify
from http import HTTPStatus
from aclaaa.decorator import check_session_auth
from template.db import example
from acloplog.decorator import api_log

hello_api = Blueprint("hello_api", __name__)


@hello_api.route("")
@check_session_auth(authentication=False, authorization=False)
@api_log(dev=False)
def hello():
    example.insert()
    ret = {
        "status": HTTPStatus.OK,
        "msg": "hello",
    }
    return jsonify(ret), ret["status"]
