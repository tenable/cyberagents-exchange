---
last_reviewed: 2026-08-19
name: "Tenable License Count"
author: "conard0-git"
github_url: "https://github.com/conard0-git/tenable-license-count"
description: "Report Tenable Security Center license utilization — licensed IPs, active IPs, expiration, and rolled-up utilization %."
license: "MIT"
tier: "contributed"
tags: ["tenable", "security-center", "license-management", "license-utilization", "capacity-planning", "compliance-reporting", "utilities"]
integrations: ["Tenable"]
date_added: 2026-08-14
contribution_agreement_date: 2026-08-14T16:39:56Z
compatible_platforms: ["Claude Code"]
invocation: "/tenable-license-count"
---

Summarize **Tenable Security Center** license usage across one or more
consoles. For each configured console the skill queries the system
endpoint for `licensedIPs`, `activeIPs`, and `licenseExpiration`;
optionally reads the latest license history record; then prints a
per-console summary plus a grand-total block and a utilization percentage.
Suitable as a weekly ops posture check, a pre-renewal capacity signal, or
a rolled-up view for multi-console environments where logging into each
console UI to eyeball license headroom isn't practical.

This skill is **Security Center-specific**. Tenable Vulnerability
Management (Tenable.io / cloud) uses a different licensing model and API
surface that this workflow does not target.

## What it does

- **Enumerates configured consoles.** Reads a caller-supplied list of
  `(label, env-prefix)` pairs. Each prefix resolves three env vars
  (`PREFIX_URL`, `PREFIX_ACCESS_KEY`, `PREFIX_SECRET_KEY`) — no config
  files, no hardcoded URLs, no baked-in console names.
- **Queries `/rest/system` for license state.** Reads `licensedIPs`,
  `activeIPs`, and `licenseExpiration` from the response envelope; formats
  the expiration timestamp (unix seconds → UTC `YYYY-MM-DD`).
- **Optionally reads the latest license history record** from
  `/rest/all/licenseInfo` (best-effort; silently skipped if the API key
  lacks permission for that endpoint).
- **Accumulates grand totals** across every reachable console — total
  licensed IPs, total active IPs, and utilization percentage
  (`total_active / total_licensed × 100`).
- **Missing-env graceful.** Consoles with incomplete env vars are skipped
  with a warning, never treated as failures. A single-console setup does
  not fail just because other prefixes aren't set.
- **Per-console failures are non-fatal.** A network timeout or auth error
  on one console logs the failure and continues; the run still produces a
  report for the reachable consoles and correct grand totals over what
  responded.

## How it works

The skill treats each console as an independent (label, prefix) unit. For
every configured pair it issues a `GET /rest/system` with a Security
Center `x-apikey` header (`accesskey=…; secretkey=…`) and a 30-second
timeout, extracts the three license fields, and optionally follows up with
`GET /rest/all/licenseInfo` for a history line — this second call is
never fatal, so a permission-restricted history endpoint doesn't affect
the primary summary. Values are cast defensively (SC returns some numeric
fields as strings across versions), and per-console failures are logged
without aborting the run. The result is a compact per-console block plus
a grand-total block with utilization percentage, printed to stdout.

## Example usage

Bare invocation — query every configured console:

```
/tenable-license-count
```

Restrict to a subset of configured consoles by env-var prefix:

```
/tenable-license-count only the TENABLE_SC_PROD prefix
```

Force the best-effort license-history line even when the endpoint
misbehaves (still degrades gracefully if the permission truly is absent):

```
/tenable-license-count include license history record
```

See `SKILL.md` for the full workflow,
`references/security-center-license-api.md` for the API mechanics
(endpoints, response schema, TLS/timeout handling, and the multi-console
pattern), and the linked repo's README for a full **Known limitations**
section covering Security-Center-only scope, TLS-verify-off default,
history-permission silent fallback, and the point-in-time nature of the
snapshot.
