import os
import boto3
from botocore.config import Config

BUCKET = os.getenv("UPLOAD_BUCKET", "uploads")
ENDPOINT = os.getenv("AWS_ENDPOINT_URL")

_kwargs = dict(
    endpoint_url=ENDPOINT,
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    config=Config(s3={"addressing_style": "path"}),
)

# Only for the local emulator; on real AWS leave credentials to the role
if ENDPOINT:
    _kwargs["aws_access_key_id"] = os.getenv("LOCAL_AWS_ACCESS_KEY_ID", "test")
    _kwargs["aws_secret_access_key"] = os.getenv("LOCAL_AWS_SECRET_ACCESS_KEY", "test")

s3 = boto3.client("s3", **_kwargs)