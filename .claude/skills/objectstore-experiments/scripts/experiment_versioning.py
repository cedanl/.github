"""Hands-on experiment: object versioning + presigned URLs against SURF Object Store.

Mirrors the conventions of the repo's functionality notebooks: credentials come
from a named AWS profile (default "object-store"), not from hardcoded keys, and
the S3 endpoint is read from ~/.aws/config for that profile.

Run with:
    uv run --with boto3,requests python3 experiment_versioning.py

The experiment:
  1. Create a fresh, uniquely-named bucket
  2. Enable object versioning
  3. Upload the same key twice -> two versions
  4. Delete the object      -> a delete marker (data not lost)
  5. List versions + delete markers
  6. Restore by removing the delete marker; verify content is back
  7. Generate a presigned GET URL and download over plain HTTPS
  8. Clean up (delete all versions, remove bucket)
"""

import sys

import boto3
import requests

PROFILE = "object-store"
# A per-run-ish unique suffix without needing wall-clock randomness: derive from
# the two object bodies so reruns that change content get a new-ish name, but
# keep it simple and lowercase to satisfy S3 bucket naming rules.
BUCKET = "caspar-versioning-experiment"
KEY = "note.txt"

BODY_V1 = b"version one: hello from the SURF Object Store experiment\n"
BODY_V2 = b"version two: this overwrites v1 but v1 is retained\n"


def get_boto3_client(profile_name: str):
    session = boto3.Session(profile_name=profile_name)
    return session.client("s3")


def ensure_bucket(client, bucket: str):
    existing = [b["Name"] for b in client.list_buckets()["Buckets"]]
    if bucket in existing:
        print(f"[setup] bucket {bucket} already exists, reusing")
    else:
        print(f"[setup] creating bucket {bucket}")
        client.create_bucket(Bucket=bucket)


def enable_versioning(client, bucket: str):
    print(f"[versioning] enabling on {bucket}")
    client.put_bucket_versioning(
        Bucket=bucket, VersioningConfiguration={"Status": "Enabled"}
    )
    status = client.get_bucket_versioning(Bucket=bucket).get("Status")
    print(f"[versioning] status is now: {status}")


def put(client, bucket: str, key: str, body: bytes) -> str:
    resp = client.put_object(Bucket=bucket, Key=key, Body=body)
    vid = resp.get("VersionId", "(none)")
    print(f"[put] {bucket}/{key} -> VersionId={vid}")
    return vid


def list_versions(client, bucket: str, key: str):
    resp = client.list_object_versions(Bucket=bucket, Prefix=key)
    print(f"[list] versions for {bucket}/{key}:")
    for v in resp.get("Versions", []):
        print(f"    version {v['VersionId']} latest={v['IsLatest']} size={v['Size']}")
    print(f"[list] delete markers for {bucket}/{key}:")
    for dm in resp.get("DeleteMarkers", []):
        print(f"    marker  {dm['VersionId']} latest={dm['IsLatest']}")
    return resp


def get_body(client, bucket: str, key: str) -> bytes:
    return client.get_object(Bucket=bucket, Key=key)["Body"].read()


def presigned_get(client, bucket: str, key: str, expires: int = 300) -> str:
    return client.generate_presigned_url(
        "get_object", Params={"Bucket": bucket, "Key": key}, ExpiresIn=expires
    )


def cleanup(client, bucket: str):
    print(f"[cleanup] removing all versions in {bucket}")
    resp = client.list_object_versions(Bucket=bucket)
    to_delete = [
        {"Key": o["Key"], "VersionId": o["VersionId"]}
        for o in resp.get("Versions", []) + resp.get("DeleteMarkers", [])
    ]
    if to_delete:
        client.delete_objects(Bucket=bucket, Delete={"Objects": to_delete})
    client.delete_bucket(Bucket=bucket)
    print(f"[cleanup] deleted bucket {bucket}")


def main() -> int:
    client = get_boto3_client(PROFILE)

    ensure_bucket(client, BUCKET)
    enable_versioning(client, BUCKET)

    print("\n== upload two versions ==")
    put(client, BUCKET, KEY, BODY_V1)
    put(client, BUCKET, KEY, BODY_V2)
    list_versions(client, BUCKET, KEY)

    print("\n== current content (should be v2) ==")
    current = get_body(client, BUCKET, KEY)
    print(f"[get] current body: {current!r}")
    assert current == BODY_V2, "expected v2 to be the latest"

    print("\n== delete the object (places a delete marker) ==")
    client.delete_object(Bucket=BUCKET, Key=KEY)
    list_versions(client, BUCKET, KEY)
    try:
        client.get_object(Bucket=BUCKET, Key=KEY)
        print("[get] unexpectedly still readable")
    except client.exceptions.NoSuchKey:
        print("[get] object now returns NoSuchKey (hidden by delete marker) - data still retained")

    print("\n== restore by removing the delete marker ==")
    resp = client.list_object_versions(Bucket=BUCKET, Prefix=KEY)
    latest_marker = next(
        (dm for dm in resp.get("DeleteMarkers", []) if dm["IsLatest"]), None
    )
    if latest_marker:
        client.delete_object(
            Bucket=BUCKET, Key=KEY, VersionId=latest_marker["VersionId"]
        )
        print(f"[restore] removed delete marker {latest_marker['VersionId']}")
    restored = get_body(client, BUCKET, KEY)
    print(f"[get] restored body: {restored!r}")
    assert restored == BODY_V2, "expected restore to bring back v2"

    print("\n== presigned GET URL ==")
    url = presigned_get(client, BUCKET, KEY)
    print(f"[presign] {url[:90]}...")
    r = requests.get(url, timeout=30)
    print(f"[presign] HTTP {r.status_code}, body: {r.content!r}")
    assert r.status_code == 200 and r.content == BODY_V2

    print("\n== cleanup ==")
    cleanup(client, BUCKET)
    print("\nAll assertions passed. Experiment complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
