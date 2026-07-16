---
name: gate
description: Decode and fix a failing SonarCloud or CodeQL quality gate on a PR. Pulls the actual issues via API, separates real defects from metric artifacts, fixes the cheap and legitimate ones, and reports remaining items as an explicit judgment call. Use when a Sonar/CodeQL gate is red.
---

# gate

A failing quality gate usually mixes real issues with metric artifacts. Decode it
before touching code, and never game a metric silently.

## Auth
Prefix `gh` with `unset GITHUB_TOKEN &&` (an invalid token may shadow the login).
SonarCloud has a public API for public projects — no token needed for reads.

## Steps
1. Get the gate status and per-condition breakdown:
   `curl -s "https://sonarcloud.io/api/qualitygates/project_status?projectKey={KEY}&pullRequest={N}"`
2. Pull the ACTUAL issues, don't reason from ratings alone:
   - Bugs/vulns: `curl -s "https://sonarcloud.io/api/issues/search?componentKeys={KEY}&pullRequest={N}&types=BUG,VULNERABILITY&resolved=false"`
   - Hotspots: `curl -s "https://sonarcloud.io/api/hotspots/search?projectKey={KEY}&pullRequest={N}&status=TO_REVIEW"`
   - Smells: same issues endpoint with `types=CODE_SMELL`
3. Triage each into: real defect / metric artifact / false positive. Common artifacts:
   - **Coverage 0%**: no report uploaded, or the code is genuinely untestable
     (UI/frontend/JS). Fix by generating real coverage for testable code AND
     excluding untestable code via `sonar.coverage.exclusions`.
   - **Duplication**: often shared boilerplate — extract it.
   - **JS "expected assignment/expression"**: a template placeholder Sonar parses
     as raw JS. Make placeholders comments.
   - **"prefer top-level await"**: false positive when code runs in an injected
     async wrapper (e.g. streamlit-js).
4. Fix the cheap, legitimate ones. For coverage gaps in DB/integration code, add
   integration tests with real service containers rather than excluding.
5. Push, wait for the rescan (`gh run watch`), re-query the gate to CONFIRM green.
6. Report any remaining red condition as an explicit judgment call to the user —
   don't over-exclude to force a pass.

## Principle
Distinguish "real security/correctness problem" from "metric hygiene". Report the
distinction honestly; fix what's genuinely worth fixing.
