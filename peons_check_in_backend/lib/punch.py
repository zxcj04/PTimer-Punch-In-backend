from datetime import datetime, timezone
from uuid import uuid4

from peons_check_in_backend.db import punch
from peons_check_in_backend.lib import project, user


class PunchError(Exception):
    pass


def get_user_active_punch(user_id):
    records = get_user_punch_list(user_id)
    if len(records) == 0:
        return None
    record = records[0]
    if record is None:
        return None
    elif record.get("punch_out_time", None) is not None:
        return None
    return record


def punch_in(user_id, project_id):
    try:
        is_last_punch_active = get_user_active_punch(user_id) is not None
    except PunchError as e:
        is_last_punch_active = False
    if is_last_punch_active:
        raise PunchError("Last punch is active")

    punch_id = str(uuid4())
    punch_time = datetime.now(timezone.utc)
    punch.insert(
        {
            "punch_id": punch_id,
            "user_id": user_id,
            "punch_in_time": punch_time,
            "record_time": punch_time,
            "project_id": project_id,
        }
    )
    return punch_id, punch_time


def punch_out(user_id):
    punch_time = datetime.now(timezone.utc)
    record = get_user_active_punch(user_id)
    if record is None:
        raise PunchError("No active punch")
    punch.update_punch_out_time(record["punch_id"], punch_time)
    return punch_time


def calc_working_hour(records, start=None, end=None):
    for record in records:
        if "project_id" in record:
            record["project_name"] = project.get_project(record["project_id"]).get("project_name", "")
        if "punch_out_time" in record:
            punch_in_time = record["punch_in_time"]
            punch_out_time = record["punch_out_time"]
            if start and punch_in_time < start:
                punch_in_time = start
            if end and punch_out_time > end:
                punch_out_time = end
            record["working_timer"] = punch_out_time - punch_in_time
            record["working_timer"] = int(record["working_timer"].total_seconds())
    return records


def get_user_punch_list(user_id, start=None, end=None):
    start = datetime.strptime(start, r"%Y-%m-%dT%H:%M:%S.%fZ") if start else None
    end = datetime.strptime(end, r"%Y-%m-%dT%H:%M:%S.%fZ") if end else None
    records = punch.get_user_punch_list(user_id, start, end)
    if len(records) == 0:
        return []
    if not start and not end:
        records[0]["editable"] = True
    records = [record for record in records if record.get("is_delete", False) is False]
    records = calc_working_hour(records, start, end)
    return records


def get_all_punch(start=None, end=None):
    start = datetime.strptime(start, r"%Y-%m-%dT%H:%M:%S.%fZ") if start else None
    end = datetime.strptime(end, r"%Y-%m-%dT%H:%M:%S.%fZ") if end else None
    records = punch.get_all_punch(start, end)
    records = calc_working_hour(records, start, end)
    for record in records:
        if "user_id" not in record:
            continue
        record["user_name"] = user.get_user_name(record["user_id"])
    return records


def update_punch(punch_id, new_record):
    new_punch = {}
    if new_record.get("punch_in_time", None):
        new_punch["punch_in_time"] = datetime.strptime(new_record.get("punch_in_time", None), r"%Y-%m-%dT%H:%M:%S.%fZ")
    if new_record.get("punch_out_time", None):
        new_punch["punch_out_time"] = datetime.strptime(new_record.get("punch_out_time", None), r"%Y-%m-%dT%H:%M:%S.%fZ")
    if new_record.get("project_id", None):
        new_punch["project_id"] = new_record.get("project_id", None)
    punch.update(punch_id, new_punch)


def recover_punch(punch_id):
    punch.recover(punch_id)


def delete_punch(punch_id):
    is_exist = punch.exist(punch_id)
    if not is_exist:
        raise PunchError("Punch not exist")
    punch.virtual_delete(punch_id)
