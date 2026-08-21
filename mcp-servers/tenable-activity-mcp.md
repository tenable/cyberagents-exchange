---
last_reviewed: 2026-08-19
name: "Tenable Activity MCP"
author: "brendanong95"
github_url: "https://github.com/brendanong95/tenable-activity-mcp"
description: "Turns the Tenable VM audit log into answered questions — per-actor baselines, API-key usage attribution, and explained anomaly findings computed in Python rather than raw events handed to the model."
license: "MIT"
tier: "contributed"
tags: ["audit-log", "anomaly-detection", "insider-threat", "api-key-monitoring", "detection-engineering", "baselining"]
integrations: ["Tenable"]
date_added: 2026-08-19
contribution_agreement_date: 2026-08-19T15:34:46Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop"]
transport: "stdio"
runtime: "python"
auth_method: "api-key"
tools_exposed:
  - name: "list_activity_events"
    description: "Event feed for a date window with actor/action filters; follows the pagination cursor automatically and returns a resumable next_token if the safety cap is hit."
  - name: "summarize_activity"
    description: "Deterministic rollup for a window: counts by actor, action, CRUD type and access type, plus failure and anonymous rates."
  - name: "get_api_key_usage"
    description: "API-key-driven activity only, grouped by actor: action breakdown, distinct source IPs, and first/last seen timestamps."
  - name: "detect_anomalies"
    description: "Compares a window against each actor's stored baseline: new actors, volume spikes, unseen source IPs, failed-event bursts, sustained failure rates, off-hours spikes and never-before-seen actions, each with evidence and a reasoning sentence."
  - name: "get_actor_profile"
    description: "One actor's full picture: best-effort role, all-time action breakdown, access types, and every source IP seen."
  - name: "check_permission_prereqs"
    description: "Pass/fail on whether the configured API keys can actually read the audit log, with plain-language remediation text."
resources_exposed: []
prompts_exposed: []
---

## What it does

> The audit log already knows which API key started behaving differently.
> The problem is that nobody reads 40,000 events.

Tenable's `audit-log/v1/events` endpoint records who did what across a VM tenant —
every login, key use, scan launch, user edit and permission change. Existing MCP
coverage of that endpoint stops at listing events, which leaves the actual work
(counting them, grouping them, deciding what is unusual) to the model. That is the
one job an LLM is worst at: arithmetic over long lists, where a miscount is
invisible and confidently reported.

This server does the analysis in Python and returns finished answers. Tools hand
back `failure_rate_pct`, `by_actor`, and `findings` with evidence attached — not a
pile of events for the model to add up. Ask "what changed this week" and the
numbers in the reply are computed, not estimated.

The detection surface is aimed at credential and insider-threat questions that the
vulnerability data itself cannot answer:

- **`get_api_key_usage`** attributes activity to the API keys that drove it,
  separating scripted access from UI sessions using the event's auth-method field
  with a user-agent-shape fallback. Each actor gets distinct source IPs and a
  first/last-seen window — enough to spot a service-account key being used from a
  laptop, or a key that kept working after its owner left.
- **`detect_anomalies`** runs seven checks against per-actor history: previously
  unseen actor, volume spike, source IP absent from the baseline lookback,
  failed-event burst, sustained high failure rate, off-hours concentration, and
  never-before-seen action. Every finding carries the evidence that triggered it
  and a sentence explaining the reasoning.
- **`check_permission_prereqs`** exists because the audit log needs the
  Administrator role and the failure mode is otherwise a bare HTTP 403. It answers
  "can these keys even see this" in one call, with remediation text.

## How it works

Baselines are **per actor**, held in a local SQLite file. A service account that
legitimately runs 500 scans a day establishes that as its own normal and does not
get flagged for continuing to do it — the comparison is always against that
actor's history, never a tenant-wide average. Baselines older than 12 hours are
recomputed from the period immediately preceding the requested window.

Analysed events are deliberately **not folded back into the baseline**, so
re-running the same window returns the same findings. An investigation that gets
repeated as the analyst narrows the date range does not quietly erode its own
reference point.

Every threshold is a named constant (`SPIKE_MULTIPLIER`, `HIGH_FAILURE_RATE_PCT`,
`OFF_HOURS_RATIO_MULTIPLIER`, …) and each result echoes back the thresholds that
produced it under a `thresholds` key, so a finding can be argued with rather than
merely trusted.

Two safety properties are structural rather than incidental. Field values whose key
names a secret, or whose value has the shape of Tenable key material, are **masked
to their last 4 characters before leaving the server** — including in error paths;
the offline test suite plants secrets in fake responses and asserts they never
surface. Pagination is **capped** at 20 pages / 100k events per call, and hitting
that cap is reported explicitly alongside the cursor needed to resume, so a wide
window degrades into a stated partial answer instead of a silent truncation or a
runaway bill.

Event fetching goes through pyTenable's `TenableIO` session, which keeps auth and
connection handling in the maintained library while leaving the `pagination.next`
cursor visible; an equivalent `requests` transport using the `X-ApiKeys` header
takes over if pyTenable is unavailable. Rate limiting backs off on the
`X-RateLimit-Reset` header, since this endpoint sends no `Retry-After`. Every call
is a GET — the server has no write path to the tenant.

## Known limitations

- Requires the **Administrator** role, or a custom role with explicit audit-log
  read permission, on the user owning the API keys. Anything less returns 403;
  `check_permission_prereqs` reports that in plain language.
- `detect_anomalies` needs history before it is useful. The first run against a
  fresh `state.db` builds baselines from the preceding `baseline_days` and will be
  noisier than later runs.
- Role resolution in `get_actor_profile` is best-effort: if the keys cannot list
  users, the profile is returned without the role label.
- Off-hours detection uses a fixed UTC band (20:00–06:00) and does not adjust for
  the tenant's actual working timezone, so distributed teams will see off-hours
  findings that are simply someone else's morning.
- Baselines are local to the machine running the server; they are not shared
  between installs.
