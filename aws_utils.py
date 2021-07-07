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
json_bucket = "badger-staging-merkle-proofs"
analytics_bucket = "badger-analytics"

key = "badger-boosts.json"

scores_url = "https://badgerdao.tk/rewards/scores.json"


def fetch_boosts():
    s3_object = s3.get_object(Bucket=json_bucket, Key=key)
    data = s3_object["Body"].read().decode("utf-8")
    return data


def last_boost_update():
    s3_object = s3.get_object(Bucket=json_bucket, Key=key)
    lastMod = s3_object["ResponseMetadata"]["HTTPHeaders"]["last-modified"]
    time_struct = time.strptime(lastMod, "%a, %d %b %Y %H:%M:%S %Z")
    return datetime.fromtimestamp(mktime(time_struct))


def fetch_scores():
    return requests.get(scores_url).json()


def fetch_cycle(cycleNumber):
    key = "logs/{}.json".format(cycleNumber)
    s3_object = s3.get_object(Bucket=analytics_bucket, Key=key)
    return json.loads(s3_object["Body"].read().decode("utf-8"))


def list_all_cycles():
    print("listing all cycles")
    cycles = []
    results = s3.list_objects_v2(
        Bucket=analytics_bucket,
        Prefix="logs/",
    )
    data = results["Contents"]
    for res in data:
        if res["Key"] == "logs/":
            continue
        fileName = res["Key"].split("/")[1]
        cycle = fileName.split(".")[0]
        cycles.append(int(cycle))

    return cycles
