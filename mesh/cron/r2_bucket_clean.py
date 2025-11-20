import os
from datetime import datetime, timedelta, timezone

import boto3
from dotenv import load_dotenv

load_dotenv()


def clean_old_files(dry_run=False):
    r2_endpoint = os.getenv("R2_ENDPOINT")
    r2_access_key = os.getenv("R2_ACCESS_KEY")
    r2_secret_key = os.getenv("R2_SECRET_KEY")
    r2_bucket = os.getenv("R2_BUCKET_WAN_VIDEO_AGENT")

    if not all([r2_endpoint, r2_access_key, r2_secret_key, r2_bucket]):
        raise ValueError("R2 credentials (R2_ENDPOINT, R2_ACCESS_KEY, R2_SECRET_KEY, R2_BUCKET_WAN_VIDEO_AGENT) required")

    s3_client = boto3.client(
        "s3",
        endpoint_url=r2_endpoint,
        aws_access_key_id=r2_access_key,
        aws_secret_access_key=r2_secret_key,
        region_name="auto",
    )

    cutoff_time = datetime.now(timezone.utc) - timedelta(days=3)
    deleted_count = 0
    total_size = 0

    mode = "DRY RUN" if dry_run else "LIVE"
    print(f"[{mode}] Cleaning files older than {cutoff_time.isoformat()} from bucket: {r2_bucket}")

    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=r2_bucket):
        if "Contents" not in page:
            continue

        for obj in page["Contents"]:
            if obj["LastModified"] < cutoff_time:
                action = "Would delete" if dry_run else "Deleting"
                print(f"{action}: {obj['Key']} (modified: {obj['LastModified']}, size: {obj['Size']} bytes)")
                if not dry_run:
                    s3_client.delete_object(Bucket=r2_bucket, Key=obj["Key"])
                deleted_count += 1
                total_size += obj["Size"]

    print(f"\nDeleted {deleted_count} files, freed {total_size / (1024 * 1024):.2f} MB")


if __name__ == "__main__":
    import sys
    dry_run = "--dry-run" in sys.argv
    clean_old_files(dry_run=dry_run)
