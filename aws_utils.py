import boto3
import decouple
from rich.console import Console
import time
from time import mktime
from datetime import datetime
s3 = boto3.client(
    "s3",
    aws_access_key_id=decouple.config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=decouple.config("AWS_SECRET_ACCESS_KEY"),
)
json_bucket = "badger-staging-merkle-proofs"
key = "badger-boosts.json"


def fetch_boosts():
    s3_object = s3.get_object(Bucket=json_bucket,Key=key)
    data = s3_object["Body"].read().decode("utf-8")
    return data

def last_boost_update():
    s3_object = s3.get_object(Bucket=json_bucket,Key=key)
    lastMod = s3_object['ResponseMetadata']['HTTPHeaders']['last-modified']
    time_struct = time.strptime(lastMod, '%a, %d %b %Y %H:%M:%S %Z')
    return datetime.fromtimestamp(mktime(time_struct))
