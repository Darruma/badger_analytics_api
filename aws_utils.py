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
dynamodb = boto3.resource(
        "dynamodb",
        region_name="us-west-1",
        aws_access_key_id=decouple.config("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=decouple.config("AWS_SECRET_ACCESS_KEY"),
)
json_bucket = "badger-merkle-proofs"
key = "badger-boosts.json"

chain_to_id = {
    "ethereum":1,
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

def get_metadata_table():
    return "metadata-staging"

def get_claimable_table():
    return "unclaimed-snapshots-staging"