from http import HTTPStatus

from aclaaa.decorator import check_session_auth
from flask import Blueprint, jsonify, request

from peons_check_in_backend.lib import project, user


project_api = Blueprint("project_api", __name__)


@project_api.route("/info/<project_id>", methods=["GET"])
@check_session_auth(authentication=True, authorization=True, permissions=["worker"])
def info(project_id: str):
    try:
        target = project.get_project(project_id)
        target["project_owner_name"] = user.get_user_name(target.get("project_owner", None))
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
        project_name = request.json["project_name"]
        project_owner = request.json["project_owner"]
        description = request.json["description"]
    except KeyError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": f"missing key: {str(e)}",
        }
        return jsonify(ret), ret["status"]
    try:
        new_project = project.Project(project_name, project_owner, description)
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
        for i in ret:
            i["project_owner_name"] = user.get_user_name(i.get("project_owner", None))
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


@project_api.route("/update", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["admin"])
def update():
    try:
        project_id = request.json["project_id"]
        new_project = request.json["project"]
    except KeyError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": f"missing key: {str(e)}",
        }
        return jsonify(ret), ret["status"]
    try:
        project.update(project_id, new_project)
    except project.ProjectError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "update project success",
    }
    return jsonify(ret), ret["status"]


@project_api.route("/recover", methods=["POST"])
@check_session_auth(
    authentication=True, authorization=True, permissions=["admin"]
)
def recover_project():
    data = request.get_json()
    project_id = data.get("project_id", None)
    if project_id is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "missing key: project_id",
        }
        return jsonify(ret), ret["status"]
    try:
        project.recover(project_id)
    except project.ProjectError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "recover project success",
    }
    return jsonify(ret), ret["status"]


@project_api.route("/delete", methods=["POST"])
@check_session_auth(authentication=True, authorization=True, permissions=["admin"])
def delete():
    data = request.get_json()
    project_id = data.get("project_id", None)
    if project_id is None:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": "missing key: project_id",
        }
        return jsonify(ret), ret["status"]
    try:
        project.delete(project_id)
    except project.ProjectError as e:
        ret = {
            "status": HTTPStatus.BAD_REQUEST,
            "msg": str(e),
        }
        return jsonify(ret), ret["status"]
    ret = {
        "status": HTTPStatus.OK,
        "msg": "delete project success",
    }
    return jsonify(ret), ret["status"]
