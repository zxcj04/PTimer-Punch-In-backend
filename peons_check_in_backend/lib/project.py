from peons_check_in_backend.db import project


class Project:
    def __init__(self, project_id, project_name, project_owner, description):
        self.project_id = project_id
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


def exist(project_id):
    return project.exist(project_id)
