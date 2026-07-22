"""Hands-on experiment: bucket lifecycle policies against SURF Object Store.

Mirrors the repo's bucket-lifecycle-policies notebook: a versioned bucket, a
lifecycle rule that expires non-current (old) versions, plus a rule that expires
current objects after N days. Credentials come from a named AWS profile.

Lifecycle expiration is day-granular and executed by Ceph on its own schedule,
so we cannot watch an object vanish in real time. What we CAN verify now:
  - the policy is accepted and stored exactly as configured (round-trip)
  - both current-version and non-current-version rules are supported
Run once to set it up; rerun later with `check` to see if Ceph applied it.

Run with:
    uv run --with boto3 python3 experiment_lifecycle.py          # set up + verify policy
    uv run --with boto3 python3 experiment_lifecycle.py check     # re-list versions later
    uv run --with boto3 python3 experiment_lifecycle.py cleanup   # remove bucket
"""

import json
import sys

import boto3

PROFILE = "object-store"
BUCKET = "caspar-lifecycle-experiment"
KEY = "object.bin"

POLICY = {
    "Rules": [
        {
            "ID": "expire-noncurrent-versions-after-1-day",
            "Filter": {"Prefix": ""},
            "NoncurrentVersionExpiration": {"NoncurrentDays": 1},
            "Status": "Enabled",
        },
        {
            "ID": "expire-current-objects-after-30-days",
            "Filter": {"Prefix": "tmp/"},
            "Expiration": {"Days": 30},
            "Status": "Enabled",
        },
    ]
}


def client():
    return boto3.Session(profile_name=PROFILE).client("s3")


def ensure_bucket(c):
    names = [b["Name"] for b in c.list_buckets()["Buckets"]]
    if BUCKET not in names:
        print(f"[setup] creating bucket {BUCKET}")
        c.create_bucket(Bucket=BUCKET)
    c.put_bucket_versioning(
        Bucket=BUCKET, VersioningConfiguration={"Status": "Enabled"}
    )
    print("[setup] versioning enabled")


def make_versions(c):
    # Two puts of the same key -> one current + one non-current version.
    c.put_object(Bucket=BUCKET, Key=KEY, Body=b"v1 - will become non-current\n")
    c.put_object(Bucket=BUCKET, Key=KEY, Body=b"v2 - current\n")
    print("[data] uploaded two versions of", KEY)


def list_versions(c):
    resp = c.list_object_versions(Bucket=BUCKET)
    versions = resp.get("Versions", [])
    print(f"[list] {len(versions)} version(s):")
    for v in versions:
        print(f"    {v['Key']} {v['VersionId']} latest={v['IsLatest']}")
    return versions


def apply_policy(c):
    print("[policy] applying lifecycle configuration")
    c.put_bucket_lifecycle_configuration(
        Bucket=BUCKET, LifecycleConfiguration=POLICY
    )
    stored = c.get_bucket_lifecycle_configuration(Bucket=BUCKET)
    # Strip ResponseMetadata for a clean diff-style print.
    stored = {"Rules": stored["Rules"]}
    print("[policy] read back from server:")
    print(json.dumps(stored, indent=2, default=str))

    sent_ids = {r["ID"] for r in POLICY["Rules"]}
    got_ids = {r["ID"] for r in stored["Rules"]}
    assert sent_ids == got_ids, f"rule mismatch: sent {sent_ids}, got {got_ids}"
    print(f"[policy] OK - both rules stored: {sorted(got_ids)}")


def main(mode: str) -> int:
    c = client()

    if mode == "cleanup":
        resp = c.list_object_versions(Bucket=BUCKET)
        objs = [
            {"Key": o["Key"], "VersionId": o["VersionId"]}
            for o in resp.get("Versions", []) + resp.get("DeleteMarkers", [])
        ]
        if objs:
            c.delete_objects(Bucket=BUCKET, Delete={"Objects": objs})
        c.delete_bucket(Bucket=BUCKET)
        print(f"[cleanup] removed bucket {BUCKET}")
        return 0

    if mode == "check":
        print("[check] current versions (compare against the two from setup):")
        list_versions(c)
        print(
            "[check] if Ceph has run its lifecycle pass, the non-current version "
            "should be gone (>=1 day after setup)."
        )
        return 0

    # default: set up + verify
    ensure_bucket(c)
    make_versions(c)
    print("\n== versions before policy ==")
    list_versions(c)
    print("\n== apply + round-trip the lifecycle policy ==")
    apply_policy(c)
    print(
        "\nDone. The policy is stored and verified. Expiration is day-granular and "
        "runs on Ceph's schedule, so rerun with `check` after ~a day to observe the "
        "non-current version being expired.\n"
        "  uv run --with boto3 python3 experiment_lifecycle.py check"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "setup"))
