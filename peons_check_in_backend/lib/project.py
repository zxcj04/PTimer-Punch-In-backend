from uuid import uuid4

from peons_check_in_backend.db import project


class Project:
    def __init__(self, project_name, project_owner, description):
        self.project_id = str(uuid4())
        self.project_name = project_name
        self.project_owner = project_owner
        self.description = description

    def to_dict(self):
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_owner": self.project_owner,
            "description": self.description,
        }

    @staticmethod
    def available_infos():
        return ["project_name", "project_owner", "description"]


class ProjectError(Exception):
    pass


def get_project(project_id):
    return project.get(project_id)


def list_project():
    return project.listProjects()


def create_project(new_project: Project):
    if exist(new_project.project_id):
        raise ProjectError(f"project {new_project.project_id} already exists")
    project.insert(new_project.to_dict())


def update(project_id, new_project):
    if not exist(project_id):
        raise ProjectError(f"project {project_id} does not exist")
    target_project = {}
    for k in new_project.keys():
        if k not in Project.available_infos():
            continue
        target_project[k] = new_project[k]
    project.update(project_id, target_project)


def exist(project_id):
    return project.exist(project_id)


def recover(project_id):
    if not exist(project_id):
        raise ProjectError(f"project {project_id} does not exist")
    project.recover(project_id)


def delete(project_id):
    if not exist(project_id):
        raise ProjectError(f"project {project_id} does not exist")
    project.virtual_delete(project_id)
