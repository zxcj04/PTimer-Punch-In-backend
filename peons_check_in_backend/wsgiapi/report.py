from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request, Response

from peons_check_in_backend.lib import report

report_api = Blueprint("report_api", __name__)


@report_api.route("/all", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["admin"]
)
def all():
    try:
        users = request.args.getlist("users[]", None)
        start = request.args.get("start", None)
        end = request.args.get("end", None)

        result = report.generate_csv_all_working_hour(start, end, users)
        return Response(result, mimetype='text/csv', headers={"Content-Disposition":"attachment;filename=report.csv"}), HTTPStatus.OK
    except Exception as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]


@report_api.route("/project", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["admin"]
)
def project():
    try:
        project = request.args.get("project", None)
        start = request.args.get("start", None)
        end = request.args.get("end", None)

        result = report.generate_csv_project_working_hour(start, end, project)
        return Response(result, mimetype='text/csv', headers={"Content-Disposition":"attachment;filename=report.csv"}), HTTPStatus.OK
    except Exception as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]


@report_api.route("/user", methods=["GET"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["admin"]
)
def user():
    try:
        user = request.args.get("user", None)
        start = request.args.get("start", None)
        end = request.args.get("end", None)

        result = report.generate_csv_user_working_hour(start, end, user)
        return Response(result, mimetype='text/csv', headers={"Content-Disposition":"attachment;filename=report.csv"}), HTTPStatus.OK
    except Exception as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
