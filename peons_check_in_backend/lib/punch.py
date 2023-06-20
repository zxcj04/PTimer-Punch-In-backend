from uuid import uuid4
from datetime import datetime

from peons_check_in_backend.db import punch


class PunchError(Exception):
    pass


def get_user_active_punch(user_id):
    records = punch.get_user_all_punch(user_id)
    if len(records) == 0:
        raise PunchError("No punch")
    record = records[0]
    if record is None:
        raise PunchError("No punch")
    elif record.get("punch_out_time", None) is not None:
        raise PunchError("No active punch")
    return record


def punch_in(user_id):
    try:
        is_last_punch_active = get_user_active_punch(user_id) is not None
    except PunchError as e:
        is_last_punch_active = False
    if is_last_punch_active:
        raise PunchError("Last punch is active")

    punch_id = str(uuid4())
    punch_time = datetime.now()
    punch.insert({
        "punch_id": punch_id,
        "user_id": user_id,
        "punch_in_time": punch_time,
    })
    return punch_id, punch_time


def punch_out(user_id):
    punch_time = datetime.now()
    record = get_user_active_punch(user_id)
    if record is None:
        raise PunchError("No active punch")
    punch.update_punch_out_time(record["punch_id"], punch_time)
    return punch_time


def get_user_all_punch(user_id):
    records = punch.get_user_all_punch(user_id)
    return records


def get_all_punch():
    records = punch.get_all_punch()
    return records
