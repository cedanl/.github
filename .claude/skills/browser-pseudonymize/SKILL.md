---
name: browser-pseudonymize
description: >-
  Encrypt or pseudonymize sensitive columns (BSN, PGN, onderwijsnummer) in the
  user's browser via Pyodide/WebAssembly in a CEDA Streamlit app, so plaintext
  identifiers never reach the server. Use whenever you build or debug in-browser
  encryption of personal data, a Pyodide/WASM Streamlit page, an st_js /
  st_js_blocking / streamlit-js component, or handle BSN/PGN/onderwijsnummer in a
  Streamlit upload — even if the user only pastes a stuck Pyodide page or asks
  "how do we encrypt before upload?".
---

# Browser-side pseudonymization (Pyodide / WebAssembly)

CEDA Streamlit apps that handle personal data (BSN, persoonsgebonden nummer,
onderwijsnummer) encrypt the sensitive column **in the user's browser** before
anything is uploaded — the server only ever sees ciphertext. This is done with
**Pyodide** (CPython compiled to WebAssembly) running the `cryptography` package
client-side, driven from Streamlit via `streamlit_js`. Grounded in `1cijferho`
(`src/frontend/Files/`), which is the clean, refactored version; `1cijfer-config`
has an older inline-HTML generation of the same idea.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/browser-pseudonymize`,
or automatically) when you build or debug in-browser encryption of personal data,
a Pyodide/WASM Streamlit page, an `st_js`/`st_js_blocking` component, or touch
BSN/PGN/onderwijsnummer in a Streamlit upload. It is reference/convention, not a
step-by-step procedure.

## Encrypt vs. pseudonymize — pick the right one

These are **different operations** and mixing them up is a governance error, not a
style choice. Both live in `1cijferho`:

- **Reversible encryption** (browser) — `Fernet` (AES-128-CBC) with a
  password-derived key. The owner can decrypt later with the password. Use when
  the original value must be recoverable (e.g. a controlled re-identification
  flow). File: `src/frontend/Files/js/encrypt_upload.js`.
- **Irreversible pseudonymization** (server-side) — keyed **HMAC-SHA256**. Same
  input + same key → same pseudonym (so longitudinal linking within one
  institution still works), but the original is **not** recoverable. Use for
  analysis datasets where you never need the BSN back. File:
  `src/eencijferho/utils/pseudonymizer.py`.

If the task says "so we can still join across years but never reverse it" →
pseudonymize (HMAC). If it says "the uploader must be able to get the value back"
→ encrypt (Fernet). Never SHA256 a BSN **without a salt or key** — that is a
lookup table waiting to happen (this exact mistake was SURF-flagged in an earlier
1cijferho version).

## The Pyodide-in-Streamlit pattern

The page is a normal Streamlit script; the crypto runs in the browser.

```
src/frontend/Files/
├── Encrypt_Upload.py           # Streamlit page (Python, server-side)
└── js/
    ├── _pyodide_bootstrap.js    # loads Pyodide once/session + micropip install
    ├── encrypt_upload.js        # the browser crypto (runs client-side)
    └── ...                      # decrypt / upload companions
```

**Bootstrap** (`_pyodide_bootstrap.js`) — cache the Pyodide instance on `window`
so it loads once per browser session (the first load is 10–20s), then
`micropip.install('cryptography')`:

```js
if (!window.__pyodidePromise) {
    window.__pyodidePromise = (async () => {
        const { loadPyodide } = await import("https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.mjs");
        const py = await loadPyodide();
        await py.loadPackage(["micropip"]);
        await py.runPythonAsync(`import micropip; await micropip.install('cryptography')`);
        return py;
    })();
}
const py = await window.__pyodidePromise;
```

**JS injection helper** — keep the JS in separate template files (not one giant
inline HTML string — that is the `1cijfer-config` anti-pattern). Inject the
bootstrap and a single base64 JSON payload via placeholders:

```python
def _load_js(name: str, payload_b64: str) -> str:
    template = (_JS_DIR / name).read_text(encoding="utf-8")
    bootstrap = (_JS_DIR / "_pyodide_bootstrap.js").read_text(encoding="utf-8")
    return template.replace("// __PYODIDE_BOOTSTRAP__", bootstrap).replace(
        "__PAYLOAD_B64__", payload_b64)
```

Pass **all** inputs (CSV, password, column) as one base64-encoded JSON blob, not
as string concatenation — this avoids breaking the JS on quotes/newlines in the
data.

**Per-row salt + PBKDF2** — each row gets its own random 16-byte salt, written to
a `salt` column so the value can be decrypted later without a shared,
source-baked salt. Key derivation is PBKDF2HMAC-SHA256, 100 000 iterations; the
column is encrypted with Fernet. Only the ciphertext CSV is returned to Python.

## The async component gotcha (st_js_blocking)

`st_js_blocking` calls `st.stop()` and only returns a result on a **later
rerun**. If you gate the work directly on `st.button()`, the async result is
dropped on the next rerun. **Latch the click in `session_state`:**

```python
if st.button("Versleutelen & opslaan", type="primary"):
    st.session_state["encrypt_upload_running"] = True

if st.session_state.get("encrypt_upload_running"):
    raw = st_js_blocking(js, key="encrypt_upload_js")
    st.session_state["encrypt_upload_running"] = False   # clear so rerun doesn't reprocess
    # raw may be None/incomplete on an intermediate rerun — guard the json.loads
```

Always guard the parse: a `None`/non-JSON `raw` means the component hasn't
returned yet or failed — show an error and `st.stop()`, don't proceed.

## Where the ciphertext goes

After the browser returns the encrypted CSV, the server stores it — in
`1cijferho` to both MinIO and PostgreSQL via the `get_backend(...)` storage
abstraction. Splitting a record across a sensitive table, a regular table, and a
MinIO object (keyed by a derived UUID) is a separate pattern — see
`/identifier-mapping`.

## Important

- **Encrypt (Fernet, reversible) ≠ pseudonymize (HMAC, irreversible)** — choose
  deliberately; it is a governance decision. See the table above.
- **Never SHA256 a BSN without a salt/key** — it is trivially reversible via a
  precomputed table (a SURF-flagged CEDA incident). Per-row salt (encryption) or
  a secret key (HMAC pseudonymization) is mandatory.
- **Keep the HMAC/UUID key server-side** — a client-side key lets anyone forge
  pseudonyms for a known BSN (the BSN space is small and brute-forceable). The
  browser password (Fernet) is fine client-side because it's the user's own.
- **Enforce a strong key** — the server-side pseudonymization key must be
  ≥64 bytes; `load_key()` raises below that. This is a CEDA floor, *not* an HMAC
  requirement: HMAC takes any key length (shorter is zero-padded to the 64-byte
  block size, longer is hashed down to 32 — RFC 2104). What matters is **entropy**,
  so generate with `secrets.token_bytes(64)` — a 64-*character* hex string carries
  only 32 bytes of entropy, and a passphrase far less.
- **Latch `st_js_blocking` in `session_state`** — gating on `st.button()` drops
  the async result; always guard the result parse.
- Keep JS in **separate template files** injected via a helper, not one inline
  HTML blob (the `1cijfer-config` version is the anti-pattern to avoid).
- Governance framing (grondslag, bewaartermijn, who may re-identify) is out of
  scope here — this skill covers the *mechanism*, not the policy.
- Applies to cedanl repos (grounded in `1cijferho`).
