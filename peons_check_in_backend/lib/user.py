from peons_check_in_backend.db import user


class User:
    def __init__(self, id, name, email, avatar=""):
        self.name = name
        self.email = email
        self.avatar = avatar
        self.user_id = id

    def to_dict(self):
        return {
            "name": self.name,
            "user_id": self.user_id,
            "email": self.email,
            "avatar": self.avatar,
        }


def get_user(user_id):
    return user.get(user_id)


def create_user(new_user: User):
    user.insert(new_user.to_dict())
