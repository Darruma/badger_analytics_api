from aws_utils import fetch_boosts, last_boost_update
import json
from datetime import datetime

badger_boosts = {
    "eth":{},
    "arbitrum":{},
    "polygon":{}
}
l_dates = {
    "eth":datetime.min,
    "arbitrum": datetime.min,
    "polygon": datetime.min
}

def get_boost(chain):
    if chain == "matic":
        chain = "polygon"
    global l_dates, badger_boosts
    lb_update = last_boost_update(chain)
    if lb_update > l_dates[chain]:
        l_date = lb_update
        badger_boosts[chain] = json.loads(fetch_boosts(chain))
    if len(badger_boosts[chain]) > 0:
        return {"success": True, "data": {"boosts": badger_boosts[chain], "date": l_dates[chain]}}
    else:
        return {"success": False, "data": "No Badger Boosts"}
