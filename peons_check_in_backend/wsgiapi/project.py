from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import project


project_api = Blueprint("project_api", __name__)


@project_api.route("/info/<project_id>", methods=["GET"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def info(project_id: str):
    try:
        target = project.get_project(project_id)
    except project.ProjectError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "get project info success",
        "project_info": target,
    }
    return jsonify(ret), ret["status"]


@project_api.route("/create", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["admin"])
def create():
    try:
        project_id = request.json["id"]
        project_name = request.json["name"]
        project_owner = request.json["owner"]
        description = request.json["description"]
    except KeyError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": f"missing key: {str(e)}",
        }
        return jsonify(ret), ret["status"]
    try:
        new_project = project.Project(project_id, project_name, project_owner, description)
        project.create_project(new_project)
    except project.ProjectError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "create project success",
    }
    return jsonify(ret), ret["status"]


@project_api.route("/exist/<project_id>", methods=["GET"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def exist(project_id: str):
    try:
        ret = project.exist(project_id)
    except project.ProjectError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "check project exist success",
        "exist": ret,
    }
    return jsonify(ret), ret["status"]


@project_api.route("/list", methods=["GET"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def list():
    try:
        ret = project.list_project()
    except project.ProjectError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "list project success",
        "projects": ret,
    }
    return jsonify(ret), ret["status"]
