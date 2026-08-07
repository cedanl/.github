---
name: identifier-mapping
description: >-
  Split a record with a sensitive identifier (BSN, PGN, onderwijsnummer) into a
  derived UUID plus a dual PostgreSQL table + MinIO object store in a CEDA app,
  so the sensitive value and the analysis data live apart. Use when building or
  debugging the personal-data upload/store/read/delete flow, the
  secret_sensitive / secret_regular tables, UUID derivation from a BSN, or the
  init.sql schema for personal data in 1cijferho / 1cijfer-config.
---

# Identifier mapping (UUID + dual Postgres table + MinIO)

CEDA personal-data apps store an uploaded record **split across three
destinations**, keyed by a UUID derived from the sensitive identifier — so the
sensitive columns, the demographic columns, and the bulk data never sit together.
Grounded in `1cijferho` (`src/eencijferho/io/personal_data.py`, `init.sql`), with
an earlier FastAPI variant in `1cijfer-config` (`src/api/routers/upload.py`).

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/identifier-mapping`,
or automatically) when you build or debug the personal-data upload/store/read/
delete flow, the `secret_sensitive`/`secret_regular` tables, UUID derivation from
a BSN/PGN, or the personal-data `init.sql`. It is reference/convention, not a
step-by-step procedure.

## The three destinations

```
uploaded record  ──derive_uuid(PGN)──►  uuid  (the join key everywhere)
                                         │
   ┌─────────────────────────────────────┼─────────────────────────────────────┐
   ▼                                      ▼                                       ▼
secret_sensitive (Postgres)      secret_regular (Postgres)            MinIO JSON object
 uuid + encrypted IDs + salt      uuid + demographics                  uuid + everything else
                                  FK → secret_sensitive
                                  ON DELETE CASCADE
```

The UUID is the only thing shared across all three. `secret_regular` has a
foreign key to `secret_sensitive` with `ON DELETE CASCADE`, so deleting the
sensitive row removes the demographic row automatically; the code deletes the
MinIO object explicitly alongside it.

## UUID derivation — keyed HMAC, server-side

The UUID is derived from the plaintext identifier (persoonsgebonden nummer) via
**keyed HMAC-SHA256**, formatted as a UUID string:

```python
def derive_uuid(source: str) -> str:
    h = hmac.new(_uuid_key(), str(source).encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"
```

Why keyed, and why server-side: the same PGN always maps to the same UUID (so
records for the same person link up), but the key stays on the server so the
mapping can't be recomputed by a client — the BSN/PGN search space is small
enough to brute-force a keyless hash. The plaintext `__uuid_source` is used to
compute the UUID and then **dropped — never stored**. See the encryption side in
`/browser-pseudonymize`.

> **1cijfer-config variant:** the older FastAPI version instead assigns a random
> `uuid.uuid4()` and stores the `(uuid, bsn)` pair in a `sensitive` mapping table,
> uploading the de-identified CSV to a `processed` bucket and the original to an
> `original` bucket. That's a mapping table (reversible via the DB) rather than a
> derived pseudonym — a different trade-off. Prefer the `1cijferho` HMAC-derived
> approach for new work unless you specifically need a stored reverse map.

## Read-back at three resolution levels

`view_file(filename, mode=...)` joins progressively more back in — grant the least
that answers the question:

| mode | returns | joins |
|---|---|---|
| `raw` | MinIO object only (uuid + extra fields) | none |
| `with_regular` | + demographics | `secret_regular` |
| `with_encrypted` | + still-encrypted sensitive fields | both tables |

Note `with_encrypted` returns the sensitive columns **still encrypted** (plus the
`salt`) — the join never decrypts; decryption is the browser's job.

## Schema (init.sql)

`secret_sensitive` (uuid PK, the identifier columns, a per-row `salt`,
`created_at`) and `secret_regular` (uuid PK + FK, demographic VARCHARs,
`created_at`). Loaded by the Postgres container via `docker-entrypoint-initdb.d`.
The code's `ensure_schema()` also creates the tables if missing, and `get_schema()`
reads the live column list from `information_schema` (falling back to defaults),
so the flow adapts to schema changes without hardcoding column lists.

## Not yet implemented (don't claim otherwise)

`corneel_notes.txt` lists these as intended, but they are **not** in the code as
of this writing — flag them as design intent, not fact, if asked:

- **A restricted DB user** with rights only on the mapping tables — not created;
  the app uses the default `POSTGRES_USER`. `CREATE ROLE ... GRANT` is TODO.
- **PL/pgSQL stored procedures** — none; all logic is Python.
- **Constraints** INT(9) / unique-BSN / unique-HASH — not enforced; identifiers
  are stored as TEXT/VARCHAR with uniqueness only via the uuid primary key.

If a task asks to "finish" this pattern, these three are the real gaps.

## Important

- **Derive the UUID with a server-side keyed HMAC** — never a keyless hash of a
  BSN (brute-forceable; a SURF-flagged CEDA incident). Key never reaches the
  client. See `/browser-pseudonymize`.
- **The plaintext identifier is used then dropped** — `__uuid_source` is never
  written to any store.
- **Deletion must hit all three stores** — the FK cascades Postgres, but the
  MinIO object is deleted explicitly; dropping only one leaves orphaned personal
  data.
- **Grant the least resolution** that answers the question (`raw` <
  `with_regular` < `with_encrypted`); the sensitive join returns ciphertext, not
  plaintext.
- Restricted DB user, stored procedures, and INT-9/unique constraints are
  **design intent, not implemented** — say so.
- Storage goes through the `get_backend(...)` abstraction (Postgres + MinIO) —
  see `/etl-pipeline` and `/sdp-secrets-management` for how those backends get
  their config in deployed environments.
- Applies to cedanl repos (grounded in `1cijferho`, older variant in
  `1cijfer-config`).
