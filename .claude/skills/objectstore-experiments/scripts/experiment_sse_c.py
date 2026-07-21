"""Hands-on experiment: SSE-C (customer-provided keys) against SURF Object Store.

The README flags SSE-C as SURF Object Store's only encryption option exposed via
the API (no service-managed keys like Amazon's SSE-S3). This experiment mirrors
the repo's sse notebook (put/get with SSECustomerKey) and additionally proves the
security property that makes SSE-C meaningful:

  1. PUT an object encrypted with a customer key (AES256)
  2. Confirm the server returns the key's MD5 (proof it used our key)
  3. GET with the correct key -> plaintext returned
  4. GET WITHOUT the key           -> must fail (400)
  5. GET with the WRONG key         -> must fail (403)
  6. For contrast, show that service-managed encryption (SSE-S3 / aws:kms) is
     NOT offered by SURF Object Store, per the README.

Credentials come from a named AWS profile ("object-store").

Run with:
    uv run --with boto3 python3 experiment_sse_c.py
"""

import os
import sys
from base64 import b64encode
from hashlib import md5

import boto3
from botocore.exceptions import ClientError

PROFILE = "object-store"
BUCKET = "caspar-sse-experiment"
KEY = "secret.bin"

CUSTOMER_KEY = os.urandom(32)   # 256-bit key; os.urandom fine for a demo
WRONG_KEY = os.urandom(32)
PLAINTEXT = b"top secret: encrypted with a customer-provided key on SURF Object Store\n"


def client():
    return boto3.Session(profile_name=PROFILE).client("s3")


def ensure_bucket(c):
    names = [b["Name"] for b in c.list_buckets()["Buckets"]]
    if BUCKET not in names:
        print(f"[setup] creating bucket {BUCKET}")
        c.create_bucket(Bucket=BUCKET)


def put_encrypted(c):
    resp = c.put_object(
        Bucket=BUCKET, Key=KEY, Body=PLAINTEXT,
        SSECustomerKey=CUSTOMER_KEY, SSECustomerAlgorithm="AES256",
    )
    returned_md5 = resp.get("SSECustomerKeyMD5")
    expected_md5 = b64encode(md5(CUSTOMER_KEY).digest()).decode("ascii")
    print(f"[put] stored encrypted; server SSECustomerKeyMD5={returned_md5}")
    assert returned_md5 == expected_md5, "server key MD5 does not match our key"
    print("[put] server confirms it used OUR key (MD5 matches)")


def get_with_correct_key(c):
    body = c.get_object(
        Bucket=BUCKET, Key=KEY,
        SSECustomerKey=CUSTOMER_KEY, SSECustomerAlgorithm="AES256",
    )["Body"].read()
    assert body == PLAINTEXT, "decrypted content mismatch"
    print(f"[get+key] correct key -> plaintext returned: {body!r}")


def get_without_key(c):
    try:
        c.get_object(Bucket=BUCKET, Key=KEY)
        print("[get-nokey] UNEXPECTED: object returned without the key!")
        return False
    except ClientError as e:
        code = e.response["Error"]["Code"]
        status = e.response["ResponseMetadata"]["HTTPStatusCode"]
        print(f"[get-nokey] correctly denied: HTTP {status} {code}")
        return True


def get_with_wrong_key(c):
    try:
        c.get_object(
            Bucket=BUCKET, Key=KEY,
            SSECustomerKey=WRONG_KEY, SSECustomerAlgorithm="AES256",
        )
        print("[get-wrongkey] UNEXPECTED: wrong key decrypted the object!")
        return False
    except ClientError as e:
        code = e.response["Error"]["Code"]
        status = e.response["ResponseMetadata"]["HTTPStatusCode"]
        print(f"[get-wrongkey] correctly denied: HTTP {status} {code}")
        return True


def probe_service_managed(c):
    """The README says SURF offers no service-managed keys. Probe aws:kms."""
    try:
        c.put_object(
            Bucket=BUCKET, Key="kms-probe.bin", Body=b"x",
            ServerSideEncryption="aws:kms",
        )
        print("[sse-s3] aws:kms PUT accepted (service-managed encryption available?)")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        status = e.response["ResponseMetadata"]["HTTPStatusCode"]
        print(f"[sse-s3] aws:kms rejected: HTTP {status} {code} "
              "(consistent with README: no service-managed keys)")


def cleanup(c):
    for o in c.list_objects_v2(Bucket=BUCKET).get("Contents", []):
        c.delete_object(Bucket=BUCKET, Key=o["Key"])
    c.delete_bucket(Bucket=BUCKET)
    print(f"[cleanup] removed bucket {BUCKET}")


def main() -> int:
    c = client()
    ensure_bucket(c)

    print("\n== PUT with customer key ==")
    put_encrypted(c)

    print("\n== GET with correct key ==")
    get_with_correct_key(c)

    print("\n== security checks: GET must fail without/with wrong key ==")
    ok_nokey = get_without_key(c)
    ok_wrong = get_with_wrong_key(c)

    print("\n== probe for service-managed encryption (expected: unavailable) ==")
    probe_service_managed(c)

    print("\n== cleanup ==")
    cleanup(c)

    assert ok_nokey and ok_wrong, "SSE-C did not enforce key requirement!"
    print("\nAll assertions passed. SSE-C enforces the customer key. Experiment complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
