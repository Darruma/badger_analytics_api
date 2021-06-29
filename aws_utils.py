import boto3
import decouple
from rich.console import Console

s3 = boto3.client(
    "s3",
    aws_access_key_id=decouple.config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=decouple.config("AWS_SECRET_ACCESS_KEY"),
)