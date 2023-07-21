from peons_check_in_backend.db import user
from peons_check_in_backend.lib import project, auth


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
        return ["name", "telephone", "telegram"]


    @staticmethod
    def available_infos_admin():
        return ["name", "telephone", "telegram", "active", "projects"]


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
    is_admin = auth.is_admin(user_id)
    if is_admin:
        raise UserError("Cannot inactivate admin")
    user.update(user_id, {"active": False})


def activate_user(user_id):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    user.update(user_id, {"active": True})


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


def update_user(user_id, info: dict, is_admin=False):
    target_user = user.get(user_id)
    if target_user is None:
        raise UserError("User not found")
    for k in info.keys():
        if not is_admin and k not in User.available_infos():
            continue
        elif is_admin and k not in User.available_infos_admin():
            continue
        target_user[k] = info[k]
    user.update(user_id, target_user)


def get_all_users():
    users = user.get_all()
    for u in users:
        u["is_admin"] = auth.is_admin(u["user_id"])
    return users
