---
name: "KEV-Pulse"
author: "hatumus"
github_url: "https://github.com/hatumus/kev-pulse"
description: "Correlates new Tenable plugins with CISA KEV entries and launches guardrailed, tag-scoped scans on TVM or Security Center."
license: "MIT"
tier: "contributed"
tags: ["tenable", "vulnerability-management", "kev", "exposure-management", "automated-scanning", "dynamic-tagging"]
domains: ["vulnerability-management", "threat-intelligence"]
integrations: ["Tenable"]
date_added: 2026-09-24
contribution_agreement_date: 2026-09-24T12:28:04Z
transport: "both"
runtime: "python"
auth_method: "api-key"
compatible_clients: ["Claude Desktop", "Claude Code"]
tools_exposed:
  - name: "list_configured_backends"
    description: "List which Tenable backend(s) have credentials configured and which one is primary."
  - name: "list_new_plugins"
    description: "List Tenable plugins created or updated since a given date or the saved watcher cursor."
  - name: "list_kev_deltas"
    description: "List CVE IDs newly added to the CISA KEV catalog that this server has not recorded yet."
  - name: "correlate_exploited_plugins"
    description: "Return the current actionable (plugin, CVE) set: a detection plugin exists AND the CVE is a confirmed KEV entry, above a severity threshold."
  - name: "resolve_affected_tags"
    description: "Resolve which of the customer's existing dynamic tags apply to a given plugin family."
  - name: "propose_scan"
    description: "Build (but do not launch) a scan plan for a CVE/plugin match; returns a scan_plan_id."
  - name: "launch_targeted_scan"
    description: "Launch the scan described by a proposed plan. The only tool that mutates the customer's Tenable backend; gated by dry-run, an auto-scan tag allow-list, and a rate limit."
  - name: "get_scan_status"
    description: "Poll the status of a previously launched scan."
resources_exposed:
  - name: "audit://trigger-history"
    description: "Full history of proposed, launched, rejected, and dry-run scan decisions, with the triggering CVE/plugin and resolved tags."
prompts_exposed: []
---

KEV-Pulse closes a gap in Tenable Security Center and Tenable
Vulnerability Management: neither product will start a scan on its own
just because Tenable Research shipped a new detection plugin, or because a
CVE that plugin covers just showed up in CISA's Known Exploited
Vulnerabilities (KEV) catalog. This server watches both feeds, correlates
them regardless of which arrives first, resolves the customer's own
existing dynamic tags for whatever plugin family is affected, and launches
(or proposes, for human approval) a scan scoped to exactly those tagged
assets.

## What it does

- Polls Tenable's plugin feed and the CISA KEV JSON catalog on a
  configurable interval.
- Persists a durable CVE-to-plugin index and KEV cache in SQLite, so a
  match fires correctly whether the plugin or the KEV entry arrived first.
- Resolves affected assets via the customer's *existing* dynamic tags
  (no new tagging taxonomy is invented) through a pluggable backend
  adapter — Tenable Security Center or Tenable Vulnerability Management,
  auto-detecting whichever has credentials configured (or both).
- Launches a scan scoped to just those tags, subject to a dry-run switch,
  an auto-scan tag allow-list, and a rate limit that applies even to
  human-approved launches.
- Records every proposed, launched, rejected, and dry-run decision to an
  audit log exposed as the `audit://trigger-history` MCP resource.

## How it works

The correlation engine treats a (plugin, CVE) pair as actionable the
moment both directions are satisfied: a plugin newly covering a CVE that
was already in KEV, or a CVE newly added to KEV that an older plugin
already detects. Both directions are checked every cycle against a
persistent index, so nothing is missed and nothing re-fires on repeat
polls. The Tenable Security Center adapter follows the documented
`/rest/token` + `/rest/policy` + `/rest/scan` sequence for launching a
scoped scan; the Tenable Vulnerability Management adapter authenticates
via API key and uses native tag-based scan targeting. Full architecture,
sequence diagrams, and design rationale are in the repository's README
and architecture document.
