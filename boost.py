from aws_utils import fetch_boosts, last_boost_update
import json
from datetime import datetime

badger_boost = {}
l_date = datetime.min

def get_boost():
    global l_date,badger_boost
    lb_update = last_boost_update()
    if lb_update > l_date:
        l_date = lb_update
        badger_boost = json.loads(fetch_boosts())
    return badger_boost