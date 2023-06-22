from peons_check_in_backend.db import user

def get_user(user_id):
    return user.get(user_id)
