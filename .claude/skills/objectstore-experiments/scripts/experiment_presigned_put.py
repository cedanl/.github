"""Hands-on experiment: presigned PUT + SigV4 against SURF Object Store.

The repo's presigned-urls notebook demonstrates presigned GET and PUT. This
experiment focuses on two extra angles:

  1. A presigned PUT URL: a client with NO credentials uploads an object using
     only the URL (via plain requests.put), then we verify it landed.
  2. Signature versions: Boto3's default against this endpoint produces a legacy
     SigV2 URL (?AWSAccessKeyId=...&Signature=...). We also generate an explicit
     SigV4 URL (?X-Amz-Algorithm=AWS4-HMAC-SHA256...) and confirm both work.

Credentials come from a named AWS profile ("object-store").

Run with:
    uv run --with boto3,requests python3 experiment_presigned_put.py
"""

import sys

import boto3
import requests
from botocore.config import Config

PROFILE = "object-store"
BUCKET = "caspar-presigned-experiment"
KEY = "uploaded-via-url.txt"
BODY = b"this object was uploaded through a presigned PUT URL, no creds on the client\n"


def make_client(sig_version=None):
    session = boto3.Session(profile_name=PROFILE)
    cfg = Config(signature_version=sig_version) if sig_version else None
    return session.client("s3", config=cfg)


def ensure_bucket(c):
    names = [b["Name"] for b in c.list_buckets()["Buckets"]]
    if BUCKET not in names:
        print(f"[setup] creating bucket {BUCKET}")
        c.create_bucket(Bucket=BUCKET)


def classify(url: str) -> str:
    if "X-Amz-Algorithm=AWS4-HMAC-SHA256" in url:
        return "SigV4"
    if "AWSAccessKeyId=" in url:
        return "SigV2"
    return "unknown"


def presigned_put_roundtrip(c, label, key):
    url = c.generate_presigned_url(
        "put_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=300
    )
    print(f"[{label}] PUT url style: {classify(url)}")
    # A credential-less client uploads using only the URL.
    r = requests.put(url, data=BODY, timeout=30)
    print(f"[{label}] upload HTTP {r.status_code}")
    assert r.status_code == 200, f"presigned PUT failed: {r.status_code} {r.text[:200]}"

    # Verify via authenticated GET that the bytes really landed.
    stored = c.get_object(Bucket=BUCKET, Key=key)["Body"].read()
    assert stored == BODY, "stored bytes differ from what we PUT"
    print(f"[{label}] verified stored content matches ({len(stored)} bytes)")

    # And a presigned GET should return it too.
    get_url = c.generate_presigned_url(
        "get_object", Params={"Bucket": BUCKET, "Key": key}, ExpiresIn=300
    )
    g = requests.get(get_url, timeout=30)
    print(f"[{label}] presigned GET ({classify(get_url)}) HTTP {g.status_code}")
    assert g.status_code == 200 and g.content == BODY


def cleanup(c):
    for o in c.list_objects_v2(Bucket=BUCKET).get("Contents", []):
        c.delete_object(Bucket=BUCKET, Key=o["Key"])
    c.delete_bucket(Bucket=BUCKET)
    print(f"[cleanup] removed bucket {BUCKET}")


def main() -> int:
    default_client = make_client()
    ensure_bucket(default_client)

    print("\n== presigned PUT with Boto3 default signing ==")
    presigned_put_roundtrip(default_client, "default", KEY)

    print("\n== presigned PUT with explicit SigV4 signing ==")
    v4_client = make_client(sig_version="s3v4")
    presigned_put_roundtrip(v4_client, "sigv4", "uploaded-via-sigv4.txt")

    print("\n== cleanup ==")
    cleanup(default_client)
    print("\nAll assertions passed. Presigned PUT works with both signature styles. "
          "Experiment complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
