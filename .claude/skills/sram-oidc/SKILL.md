---
name: sram-oidc
description: Add SURF SRAM login (OIDC via the SRAM proxy) to a CEDA app — the authlib OAuth2 flow, the OIDC_* config, and the auth-disabled-by-default fallback used in the CEDA Streamlit apps. Use when wiring SRAM authentication, editing OIDC config, or debugging an SRAM login flow.
---

# sram-oidc

CEDA apps authenticate users against **SURF SRAM** using standard **OIDC**
through the SRAM proxy. Grounded in `text-analysis/src/auth.py` +
`text-analysis/manifests/*/config.yaml`.

## Config (env / ConfigMap)
```
OIDC_PROVIDER: SRAM
OIDC_DISCOVERY_URL: https://proxy.sram.surf.nl/.well-known/openid-configuration
SERVER_URL: https://<app>.<env>.sdp.surf.nl
SERVER_REDIRECT:            # optional path appended to SERVER_URL for the callback
CLIENT_ID / CLIENT_SECRET   # the SRAM OIDC client creds (secret — SOPS)
```
- Discovery URL is the SRAM proxy's well-known endpoint; the app reads
  `authorization_endpoint`, `token_endpoint`, `userinfo_endpoint` from it.
- `REDIRECT_URI` = `SERVER_URL` + optional `SERVER_REDIRECT`.
- Scopes: `openid email profile`.
- `CLIENT_ID`/`CLIENT_SECRET` are **secrets** — store via SOPS
  ([[sdp-secrets-management]]), never in the ConfigMap or git.

## Flow (authlib + Streamlit)
Uses `authlib.integrations.requests_client.OAuth2Session`:
1. **Login page**: fetch discovery, `create_authorization_url(authorization_endpoint, state=…)`,
   render a "Login with SRAM" link (`target="_self"`).
2. **Callback** (`?code=…&state=…`): `session.fetch_token(token_endpoint, code=…)`,
   then GET `userinfo_endpoint` with the bearer token to get the user.
3. **Session**: user info is packed into a base64 token kept in
   `st.session_state` and mirrored to a `?session=` query param so it survives
   refreshes (default 24h). *Note: this token is not signed — it's session
   continuity, not a security boundary. Don't treat it as tamper-proof.*

## The key convention: auth is opt-in
`is_auth_enabled()` returns true only when `OIDC_PROVIDER` is set. So:
- **Local dev / no config → no login** (app runs open). Nothing to stub.
- Deployed envs set `OIDC_PROVIDER: SRAM` to require login.
Gate the whole app with one call at the top of `main.py`:
```python
from auth import require_authentication
require_authentication()   # st.stop()s on the login page if not authed
```

## Debugging
- "Failed to load OIDC config" → discovery URL unreachable (VPN? typo?).
- Login loops / no callback → `REDIRECT_URI` must match the client's registered
  redirect exactly (`SERVER_URL` + `SERVER_REDIRECT`).
- "not configured properly" → `CLIENT_ID`/`CLIENT_SECRET` missing from env.

## Related
Lives in the Streamlit frontend ([[streamlit]]); creds via [[sdp-secrets-management]];
URLs/ingress via [[sdp-onboard]].
