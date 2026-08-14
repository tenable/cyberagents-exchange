---
name: "Tenable Plugin Lookup"
author: "conard0-git"
github_url: "https://github.com/conard0-git/tenable-plugin-lookup"
description: "Query Tenable Security Center by plugin ID — deep per-host lookup for one plugin, or bulk present/not-found check across many plugins. Read-only."
license: "MIT"
tier: "contributed"
tags: ["tenable", "security-center", "plugin-lookup", "vulnerability-lookup", "poam", "audit-qc", "aws", "ec2"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-07
contribution_agreement_date: 2026-08-06T20:32:58Z
compatible_platforms: ["Claude Code"]
invocation: "/tenable-plugin-lookup"
---

Two modes over one primitive — querying **Tenable Security Center** by
plugin ID via the `analysis.vulns` API, filtered by repository. Pick the
mode by intent: **host lookup** answers "who is affected by this
plugin/CVE?" and **presence check** answers "are these plugins detected at
all?" — the everyday POA&M / audit QC question. Both modes are read-only
against Tenable and only optionally read AWS for enrichment; nothing is
ever modified.

## What it does

- **Host lookup — one plugin, deep.** Run an `analysis.vulns` query with
  `tool = "vulndetails"` filtered by `repositoryIDs` and `pluginID`,
  sorted by last-seen descending. Collect per-host detail (IP, plugin
  name, severity, DNS/NetBIOS, last seen, cleaned plugin output) and
  de-duplicate by (Tenable instance, IP) keeping the most recent record —
  a host in multiple repos on one console merges to a single row.
- **Optional AWS enrichment (host lookup).** For each host IP, resolve
  the matching EC2 instance and attach owning-team tag, instance Name,
  profile, region, VPC, and instance ID. Flag anomalies: instance not
  running, not found in AWS (likely decommissioned), or **possible IP
  reuse** when the instance's launch time is *after* the plugin's last-
  seen date. Rows without a cloud match are tagged Tenable-only.
- **Presence check — many plugins, shallow.** For each plugin ID × each
  repository, run `analysis.vulns` with `tool = "sumip"` — a lightweight
  summary-by-IP query that returns a host count without pulling every
  finding. Aggregate present-yes-if-found-anywhere, total host count, and
  repositories-found for each plugin.
- **CSV + console output.** Host-lookup produces a triage-ordered CSV
  (alerts and anomalous hosts first, then by team, name, IP) plus a
  console table. Presence check produces a CSV matrix
  (`plugin_id, present, host_count, repos_found, plugin_name`) plus a
  console summary.

## How it works

The skill's guarantee is that both modes are **read-only** — no writes to
Tenable, no changes to hosts or agents, ever. Mode choice is driven by
the right query tool: `vulndetails` when you need per-host detail,
`sumip` when you only need presence and counts (much lighter on the API).
Per-repository failures are non-fatal — one unreachable source logs a
warning and the run continues so a partial answer is still returned.
Configuration is entirely environment-variable driven — Security Center
URL + keys, repository IDs, optional AWS credentials/region — with no
config files, hardcoded secrets, hostnames, or repository IDs. See
`SKILL.md` for the full workflow, `references/host-lookup.md` for the
Mode 1 query mechanics + enrichment logic, and
`references/presence-check.md` for the Mode 2 aggregation logic.
