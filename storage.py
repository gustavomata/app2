import boto3
import os
import uuid

s3 = boto3.client(
    "s3",
    region_name=os.environ["AWS_REGION"],
    aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
)

BUCKET = os.environ["S3_BUCKET"]

def upload_to_r2(local_path: str) -> str:
    ext = os.path.splitext(local_path)[1]
    key = f"jobs/{uuid.uuid4()}{ext}"

    s3.upload_file(
        local_path,
        BUCKET,
        key,
        ExtraArgs={"ACL": "private"}  # ou public-read
    )

    url = f"https://{BUCKET}.s3.{os.environ['AWS_REGION']}.amazonaws.com/{key}"
    return url

