---
name: sram-oidc
description: Add SURF SRAM login (OIDC via the SRAM proxy) to a CEDA app — the authlib OAuth2 flow, the OIDC_* config, and the auth-disabled-by-default fallback used in the CEDA Streamlit apps. Use when wiring SRAM authentication, editing OIDC config, or debugging an SRAM login flow.
---

# sram-oidc

CEDA apps authenticate users against **SURF SRAM** using standard **OIDC**
through the SRAM proxy. Grounded in `text-analysis/src/auth.py` +
`text-analysis/manifests/*/config.yaml`.

## When this applies

This is a **knowledge skill** — it loads (explicitly via `/sram-oidc`, or
automatically) when you wire SRAM authentication, edit `OIDC_*` config, or debug
an SRAM login flow. It is reference/convention.

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
- Scopes: `openid email profile eduperson_entitlement voperson_external_affiliation`.
- `CLIENT_ID`/`CLIENT_SECRET` are **secrets** — store via SOPS
  (/sdp-secrets-management), never in the ConfigMap or git.

## Scopes and user attributes

SRAM releases attributes per scope. Ask explicitly for the two extra scopes
below or you can't show the user's organisation/institution:

| Scope | Attribute(s) | Use |
|---|---|---|
| `openid` | `sub` (`…@sram.surf.nl`) | stable user id |
| `profile` | `name`, `given_name`, `family_name` | display name |
| `email` | `email` | username/contact |
| `eduperson_entitlement` | memberships `urn:mace:surf.nl:sram:group:<org>:<co>:<group>` | **org** |
| `voperson_external_affiliation` | `role@domain` | **institution** |

Deriving org and institution (the trick): org comes from the *entitlement
URN*, not the email domain or `sub`; institution from the affiliation's
`@domain`. Both attributes may be a single string **or a list** — normalize
to a list first:

```python
def org_from_entitlements(ents):
    for e in (ents if isinstance(ents, list) else [ents]):
        if "sram:group:" in e:
            parts = e.split(":")
            if len(parts) >= 6:
                return parts[5]  # orgname

def institution_from_affiliations(affs):
    for a in (affs if isinstance(affs, list) else [affs]):
        if "@" in a:
            return a.split("@")[1]  # domain
```

## Flow (authlib + Streamlit)
Uses `authlib.integrations.requests_client.OAuth2Session`. App-level OIDC
(authlib, authorization-code flow, no oauth2-proxy sidecar) is the proven
CEDA pattern on SDP: the platform only offers Basic Auth at the ingress
level, and ingress-level OIDC/access-filtering is still a platform TODO —
the app handles login itself. Benefits confirmed in practice: no extra proxy
hop, the app gets the raw SRAM `userinfo`, and SRAM login can share the same
application token as the local password login (the rest of the app can't
tell where the token came from).
1. **Login page**: fetch discovery, `create_authorization_url(authorization_endpoint, state=…)`,
   render a "Login with SRAM" link (`target="_self"`).
2. **Callback** (`?code=…&state=…`): `session.fetch_token(token_endpoint, code=…)`,
   then GET `userinfo_endpoint` with the bearer token to get the user.
3. **Session**: user info is packed into a base64 token kept in
   `st.session_state` and mirrored to a `?session=` query param so it survives
   refreshes (default 24h). *Note: this token is not signed — it's session
   continuity, not a security boundary. Don't treat it as tamper-proof.*

## Requesting a client: get CLIENT_ID / CLIENT_SECRET from SRAM

There is no self-service API — you must **request an application on SRAM**
to receive a `CLIENT_ID` and `CLIENT_SECRET`. The process is two separate,
sequential steps, both in the SRAM web UI, and the credentials are granted
by humans:

1. **Collaboration (CO)** — `sram.surf.nl/collaborations-overview`. Pick
   the CO your app belongs to (e.g. for CEDA: `CEDA-AI-HUB` or `Analytics
   Platform Onderwijs`). This is a product decision, not something to guess.
2. **Application/service registration** — `sram.surf.nl/new-service-request`
   (or `acc.sram.surf.nl/new-service-request` for the acceptance/test
   environment). This is what actually issues the `CLIENT_ID`/`CLIENT_SECRET`
   and the redirect URI registration.

Facts about the form (`new-service-request`):

- Credential approval is **human-mediated**: the request goes to SURF for
  review, then they follow up (no fixed SLA). `sram-support@surf.nl` is the
  fallback.
- There is a single **"Login URL for users"** field — no separate
  `redirect_uri` field. The exact OIDC wiring (redirect URI, scopes) is
  worked out *after* the request, so put your desired callback explicitly in
  the free-text "Additional comments", e.g.
  `https://<app>.test.sdp.surf.nl/api/auth/oidc/callback`.
- Required fields: **administrative contact**, **security contact** (real
  people — don't guess) and a **logo file**. The name shown on SRAM's
  login/consent screen is the *product* name, not the repo name.
- One open question worth asking SURF up front: whether one client can cover
  several SDP environments (test/development/staging against SRAM
  acceptance) with a separate client only for production (against SRAM
  production).
- Reuse before re-requesting: CEDA already has a working SRAM-OIDC setup in
  `text-analysis` (authlib, discovery URL, SOPS-encrypted credentials) —
  ask whoever ran that flow first.

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
- App never reaches the provider → egress missing. The pod must be able to
  reach `proxy.sram.surf.nl:443` (discovery/token/userinfo). SDP is not
  egress-open: open SRAM (and SurfDrive if used) in the tenant network
  policy in `kubernetes-clusters`.
- App crashes at startup with auth enabled → **a session/signing secret is
  unset.** Enabling OIDC without the signing secret (`CHAT_SECRET` or
  equivalent) hard-fails the app into CrashLoopBackOff; set the secret
  whenever auth is turned on.
- Login works but shows the wrong org → scope mismatch: `eduperson_entitlement`
  and `voperson_external_affiliation` weren't requested/approved, so those
  attributes are absent from `userinfo`.

## Important
- **`CLIENT_ID`/`CLIENT_SECRET` are secrets** — store via SOPS
  (/sdp-secrets-management), never in the ConfigMap or git.
- **Requesting the app is out-of-band and human-mediated** — you must submit a
  service request to SRAM to receive a `CLIENT_ID`/`CLIENT_SECRET`; budget
  for review time, and include the redirect URI in the request comments.
- **App-level OIDC (authlib) is the proven route on SDP** — the platform's
  ingress-level OIDC is not available yet; an oauth2-proxy sidecar is a
  different use case (third-party apps you can't change).
- Ask explicitly for `eduperson_entitlement` + `voperson_external_affiliation`
  or you can't show org/institution.
- The session token is **not signed** — it's session continuity, not a security
  boundary; don't treat it as tamper-proof.
- **Auth enabled → set the session/signing secret**, or the app
  CrashLoopBackOffs at startup.
- **Egress to `proxy.sram.surf.nl:443` must be opened** in the tenant network
  policy; SDP is not egress-open.
- Keep `values.yaml` comments accurate — a "credentials pending registration"
  comment stays misleading after real credentials land.
- Auth is **opt-in**: no `OIDC_PROVIDER` → app runs open, so local dev needs no
  login and nothing to stub.
- `REDIRECT_URI` must exactly match the client's registered redirect.
- Lives in the Streamlit frontend (/streamlit); URLs/ingress via /sdp-onboard.
- Applies to cedanl repos.
