from peons_check_in_backend.lib import punch as punch_lib
from peons_check_in_backend.lib import user as user_lib


def calc_all_working_hour(start, end, users=[]):
    records = []

    for user_id in users:
        records += punch_lib.get_user_punch_list(user_id, start=start, end=end)

    data = {
        "users": {},
        "total": 0,
    }

    for record in records:
        user_id = record.get("user_id")
        working_timer = record.get("working_timer", 0)

        if user_id not in data["users"]:
            data["users"][user_id] = 0

        data["users"][user_id] += working_timer
        data["total"] += working_timer

    for user in users:
        if user not in data["users"]:
            data["users"][user] = 0

    return data


def calc_project_working_hour(start, end, project_id):
    records = []

    records += punch_lib.get_all_punch(start=start, end=end)

    records = [
        record for record in records if record.get("is_delete", False) == False
    ]
    records = [
        record for record in records if record.get("project_id") == project_id
    ]

    data = {
        "users": {},
        "total": 0,
    }

    for record in records:
        user_id = record.get("user_id")
        working_timer = record.get("working_timer", 0)

        if user_id not in data["users"]:
            data["users"][user_id] = 0

        data["users"][user_id] += working_timer
        data["total"] += working_timer

    return data


def calc_user_working_hour(start, end, user_id):
    records = punch_lib.get_user_punch_list(user_id, start=start, end=end)

    data = {
        "punchs": [],
        "total": 0,
    }

    for record in records:
        user_name = user_lib.get_user_name(user_id)
        project_name = record.get("project_name", "")
        working_timer = record.get("working_timer", 0)
        start_time = record.get("punch_in_time", None).strftime(
            r"%Y-%m-%dT%H:%M:%S.%fZ"
        )
        end_time = record.get("punch_out_time", None).strftime(
            r"%Y-%m-%dT%H:%M:%S.%fZ"
        )

        data["punchs"].append(
            {
                "user_name": user_name,
                "project_name": project_name,
                "working_timer": working_timer,
                "start_time": start_time,
                "end_time": end_time,
            }
        )

    return data


def generate_csv(data):
    csv_data = []
    csv_data.append(",".join(data["header"]))
    for row in data["rows"]:
        csv_data.append(",".join([str(x) for x in row]))

    return "\n".join(csv_data)


def generate_csv_all_working_hour(start, end, users=[]):
    data = calc_all_working_hour(start, end, users=users)
    d = {
        "header": ["姓名", "信箱", "電話", "Telegram", "工作時數"],
        "rows": [],
    }

    users = sorted(data["users"].items(), key=lambda x: x[1], reverse=True)
    for user_id, working_timer in users:
        user = user_lib.get_user(user_id)
        user_name = user.get("name")
        user_mail = user.get("mail")
        user_phone = user.get("telephone")
        user_telegram = user.get("telegram")

        working_hour = round(working_timer / 3600, 2)
        d["rows"].append(
            [user_name, user_mail, user_phone, user_telegram, working_hour]
        )

    d["rows"].append(["total", "", "", "", round(data["total"] / 3600, 2)])

    return generate_csv(d)


def generate_csv_project_working_hour(start, end, project_id):
    data = calc_project_working_hour(start, end, project_id)

    d = {
        "header": ["姓名", "信箱", "電話", "Telegram", "工作時數"],
        "rows": [],
    }

    users = sorted(data["users"].items(), key=lambda x: x[1], reverse=True)
    for user_id, working_timer in users:
        user = user_lib.get_user(user_id)
        user_name = user.get("name")
        user_mail = user.get("mail")
        user_phone = user.get("telephone")
        user_telegram = user.get("telegram")
        working_hour = round(working_timer / 3600, 2)
        d["rows"].append(
            [user_name, user_mail, user_phone, user_telegram, working_hour]
        )

    d["rows"].append(["total", "", "", "", round(data["total"] / 3600, 2)])

    return generate_csv(d)


def generate_csv_user_working_hour(start, end, user_id):
    data = calc_user_working_hour(start, end, user_id)

    d = {
        "header": ["工讀生名稱", "專案名稱", "工作時數", "上班時間", "下班時間"],
        "rows": [],
    }

    punchs = sorted(data["punchs"], key=lambda x: x["start_time"])

    for punch in punchs:
        user_name = punch["user_name"]
        project_name = punch["project_name"]
        working_hour = round(punch["working_timer"] / 3600, 2)
        start_time = punch["start_time"]
        end_time = punch["end_time"]
        d["rows"].append(
            [user_name, project_name, working_hour, start_time, end_time]
        )

    return generate_csv(d)
