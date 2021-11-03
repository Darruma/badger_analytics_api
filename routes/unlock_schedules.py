from aws_utils import fetch_schedules, last_schedule_update
import json
from datetime import date, datetime

schedules = {"ethereum": {}, "arbitrum": {}, "polygon": {}}

l_date = {"ethereum": datetime.min, "arbitrum": datetime.min, "polygon": datetime.min}


def get_schedules(chain: str):
    if chain == "matic":
        chain = "polygon"
    global l_date, schedules
    lb_update = last_schedule_update(chain)
    if lb_update > l_date[chain]:
        l_date[chain] = lb_update
        schedules[chain] = fetch_schedules(chain)
        print(schedules[chain])
    if len(schedules[chain]) > 0:
        return {"success": True, "data": {"schedules": schedules[chain], "date": l_date}}
    else:
        return {"success": False, "data": "No Schedules"}
