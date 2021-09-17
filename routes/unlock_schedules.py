from aws_utils import fetch_schedules, last_schedule_update
import json
from datetime import datetime

schedules = {}
l_date = datetime.min


def get_schedules(chain: str):
    global l_date, schedules
    lb_update = last_schedule_update(chain)
    if lb_update > l_date:
        l_date = lb_update
        schedules = json.loads(fetch_schedules(chain))
    if len(schedules) > 0:
        return {"success": True, "data": {"schedules": schedules, "date": l_date}}
    else:
        return {"success": False, "data": "No Schedules"}
