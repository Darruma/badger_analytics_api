from aws_utils import fetch_nfts, last_nft_update
import json
from datetime import datetime

nfts = {}
l_date = datetime.min


def get_nfts():
    global l_date, nfts
    lb_update = last_nft_update()
    if lb_update > l_date:
        l_date = lb_update
        nfts = json.loads(fetch_nfts())
    if len(nfts) > 0:
        return {"success": True, "data": {"nfts": nfts}}
    else:
        return {"success": False, "data": {}}


def get_user_nfts(address):
    nft_data = get_nfts()
    if nft_data["success"]:
        return {"data": nfts[address.lower()], "success": True}
    else:
        return {"data": {}, "success": False}
