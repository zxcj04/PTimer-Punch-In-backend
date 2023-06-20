from uuid import uuid4
from datetime import datetime

from peons_check_in_backend.db import punch


def punch_in(user_id):
    punch_id = str(uuid4())
    punch_time = datetime.now()
    punch.insert({
        "id": punch_id,
        "user_id": user_id,
        "punch_in_time": punch_time,
    })
    return punch_id, punch_time


def punch_out(user_id):
    punch_time = datetime.now()
    record = punch.get_user_active_punch(user_id)
    if record is None:
        return None
    punch.update_punch_out_time(record["id"], punch_time)
    return punch_time
