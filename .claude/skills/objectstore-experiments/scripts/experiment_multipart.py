"""Hands-on experiment: multipart upload against SURF Object Store.

Mirrors the repo's multipart-upload notebook: create a multipart upload, upload
parts against the upload ID tracking (PartNumber, ETag), then complete it.
Credentials come from a named AWS profile ("object-store").

Beyond the notebook, this experiment also verifies integrity end to end by
comparing a hash of the reassembled object against the source, and demonstrates
that an in-progress upload can be listed and aborted.

Run with:
    uv run --with boto3 python3 experiment_multipart.py
"""

import hashlib
import os
import sys

import boto3

PROFILE = "object-store"
BUCKET = "caspar-multipart-experiment"
KEY = "multipart.bin"

# 40 MiB total, 8 MiB parts -> 5 parts. Small enough to run fast, large enough
# that parts are genuine (S3 requires all but the last part be >= 5 MiB).
TOTAL_BYTES = 40 * 1024 ** 2
PART_SIZE = 8 * 1024 ** 2


def client():
    return boto3.Session(profile_name=PROFILE).client("s3")


def ensure_bucket(c):
    names = [b["Name"] for b in c.list_buckets()["Buckets"]]
    if BUCKET not in names:
        print(f"[setup] creating bucket {BUCKET}")
        c.create_bucket(Bucket=BUCKET)


def parts_of(data, size):
    for i in range(0, len(data), size):
        yield data[i:i + size]


def upload_multipart(c, data):
    upload_id = c.create_multipart_upload(Bucket=BUCKET, Key=KEY)["UploadId"]
    print(f"[mpu] started upload_id={upload_id}")
    print(f"[mpu] uploading {len(data)} bytes in {PART_SIZE}-byte parts")

    # Show that the in-progress upload is visible before completion.
    in_progress = c.list_multipart_uploads(Bucket=BUCKET).get("Uploads", [])
    print(f"[mpu] in-progress uploads visible: {len(in_progress)}")

    parts = []
    for n, chunk in enumerate(parts_of(data, PART_SIZE), 1):
        etag = c.upload_part(
            Bucket=BUCKET, Key=KEY, Body=chunk, PartNumber=n, UploadId=upload_id
        )["ETag"]
        parts.append({"PartNumber": n, "ETag": etag})
        print(f"[mpu] part {n}: {len(chunk)} bytes, ETag={etag}")

    c.complete_multipart_upload(
        Bucket=BUCKET, Key=KEY, UploadId=upload_id,
        MultipartUpload={"Parts": parts},
    )
    print(f"[mpu] completed {len(parts)} parts")
    return len(parts)


def verify(c, data, n_parts):
    obj = next(
        o for o in c.list_objects_v2(Bucket=BUCKET)["Contents"] if o["Key"] == KEY
    )
    assert obj["Size"] == len(data), f"size {obj['Size']} != {len(data)}"
    print(f"[verify] stored size matches source: {obj['Size']} bytes")

    # Multipart ETags are of the form "<md5-of-md5s>-<numparts>" on S3/Ceph.
    etag = obj["ETag"].strip('"')
    print(f"[verify] object ETag: {etag}")
    if etag.endswith(f"-{n_parts}"):
        print(f"[verify] ETag reports {n_parts} parts (multipart marker present)")

    # Full round-trip integrity: download and compare content hash.
    downloaded = c.get_object(Bucket=BUCKET, Key=KEY)["Body"].read()
    src_hash = hashlib.sha256(data).hexdigest()
    dl_hash = hashlib.sha256(downloaded).hexdigest()
    assert src_hash == dl_hash, "content hash mismatch!"
    print(f"[verify] sha256 matches end to end: {src_hash[:16]}...")


def demo_abort(c):
    """Start an upload and abort it, showing cleanup of orphaned parts."""
    upload_id = c.create_multipart_upload(Bucket=BUCKET, Key="aborted.bin")["UploadId"]
    c.upload_part(
        Bucket=BUCKET, Key="aborted.bin", Body=os.urandom(5 * 1024 ** 2),
        PartNumber=1, UploadId=upload_id,
    )
    print(f"[abort] started and uploaded 1 part for upload_id={upload_id}")
    c.abort_multipart_upload(Bucket=BUCKET, Key="aborted.bin", UploadId=upload_id)
    remaining = c.list_multipart_uploads(Bucket=BUCKET).get("Uploads", [])
    print(f"[abort] aborted; in-progress uploads now: {len(remaining)}")


def cleanup(c):
    for o in c.list_objects_v2(Bucket=BUCKET).get("Contents", []):
        c.delete_object(Bucket=BUCKET, Key=o["Key"])
    c.delete_bucket(Bucket=BUCKET)
    print(f"[cleanup] removed bucket {BUCKET}")


def main() -> int:
    c = client()
    ensure_bucket(c)

    print("\n== generate source data ==")
    data = os.urandom(TOTAL_BYTES)
    print(f"[data] generated {len(data)} random bytes")

    print("\n== multipart upload ==")
    n_parts = upload_multipart(c, data)

    print("\n== verify ==")
    verify(c, data, n_parts)

    print("\n== abort demo ==")
    demo_abort(c)

    print("\n== cleanup ==")
    cleanup(c)
    print("\nAll assertions passed. Experiment complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
