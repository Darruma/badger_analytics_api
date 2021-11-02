import boto3
import decouple
from rich.console import Console
import requests
import json
import time
from time import mktime
from datetime import datetime

s3 = boto3.client(
    "s3",
    aws_access_key_id=decouple.config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=decouple.config("AWS_SECRET_ACCESS_KEY"),
)
json_bucket = "badger-merkle-proofs"
analytics_bucket = "badger-analytics"

key = "badger-boosts.json"
scores_url = "https://badgerdao.tk/rewards/scores.json"

chain_to_id = {
    "eth":1,
    "arbitrum": 42161,
    "polygon": 137
}

def fetch_aws_data(bucket, key):
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    data = s3_object["Body"].read().decode("utf-8")
    return data


def last_aws_update(bucket, key):
    s3_object = s3.get_object(Bucket=bucket, Key=key)
    lastMod = s3_object["ResponseMetadata"]["HTTPHeaders"]["last-modified"]
    time_struct = time.strptime(lastMod, "%a, %d %b %Y %H:%M:%S %Z")
    return datetime.fromtimestamp(mktime(time_struct))


def fetch_boosts(chain):
    return fetch_aws_data(json_bucket, f"badger-boosts-{chain_to_id[chain]}.json")


def last_boost_update(chain):
    return last_aws_update(json_bucket, f"badger-boosts-{chain_to_id[chain]}.json")


def fetch_schedules(chain):
    return fetch_aws_data(analytics_bucket, f"schedules-{chain}.json")


def last_schedule_update(chain):
    return last_aws_update(analytics_bucket, f"schedules-{chain}.json")


def fetch_nfts():
    return fetch_aws_data(json_bucket, "nft_scores.json")


def last_nft_update():
    return last_aws_update(json_bucket, "nft_scores.json")


def fetch_scores():
    return requests.get(scores_url).json()


def fetch_cycle(cycle: int, chain: str):
    key = f"logs/{chain}/{cycle}.json"
    s3_object = s3.get_object(Bucket=analytics_bucket, Key=key)
    return json.loads(s3_object["Body"].read().decode("utf-8"))


def list_all_cycles(chain: str):
    print("listing all cycles")
    cycles = []
    print("list_objects_v2")
    results = s3.list_objects_v2(
        Bucket=analytics_bucket,
        Prefix=f"logs/{chain}"
    )
    data = results["Contents"]
    for res in data:
        if res["Key"] == f"logs/{chain}/":
            continue
        fileName = res["Key"].split("/")[2]
        cycle = fileName.split(".")[0]
        cycles.append(int(cycle))
    print(cycles)
    print("listed all")
    return cycles
