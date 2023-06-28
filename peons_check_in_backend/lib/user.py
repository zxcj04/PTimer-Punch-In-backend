from peons_check_in_backend.db import user
from peons_check_in_backend.lib import project


class UserError(Exception):
    pass


class User:
    def __init__(self, id: str, info: dict):
        self.user_id = id
        self.active = False
        self.projects = []
        try:
            self.name = info["name"]
            self.mail = info["mail"]
            self.telephone = info.get("telephone", None)
            self.telegram = info.get("telegram", None)
        except KeyError as e:
            raise UserError("User info not complete")

    def to_dict(self):
        ret = {
            "user_id": self.user_id,
            "active": self.active,
            "projects": self.projects,
            "name": self.name,
            "mail": self.mail,
            "telephone": self.telephone,
            "telegram": self.telegram,
        }
        for k in list(ret.keys()):
            if ret[k] is None:
                del ret[k]
        return ret


    @staticmethod
    def available_infos():
        return ["name", "mail", "telephone", "telegram"]


def get_user(user_id):
    return user.get(user_id)


def create_user(new_user: User):
    user.insert(new_user.to_dict())


def get_user_name(user_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    return target_user.get("name", "")


def is_user_active(user_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    return target_user.get("active", False)


def inactivate_user(user_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    target_user["active"] = False
    user.update(target_user)


def activate_user(user_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    target_user["active"] = True
    user.update(target_user)


def get_user_projects(user_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    project_ids = target_user.get("projects", [])
    projects = []
    for project_id in project_ids:
        projects.append(project.get_project(project_id))
    return projects


def add_user_project(user_id, project_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    if project_id not in target_user.get("projects", []):
        target_user["projects"].append(project_id)
        user.update(target_user)


def remove_user_project(user_id, project_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    if project_id in target_user.get("projects", []):
        target_user["projects"].remove(project_id)
        user.update(target_user)


def update_user(user_id, info: dict):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    for k in info.keys():
        if k not in User.available_infos():
            raise UserError("Invalid info")
        target_user[k] = info[k]
    user.update(user_id, target_user)
