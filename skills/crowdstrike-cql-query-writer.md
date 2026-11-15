---
name: "CrowdStrike CQL Query Writer"
author: "Nicholas-devsec"
github_url: "https://github.com/Nicholas-devsec/CrowdStrike-CQL-Skill"
description: "Writes and repairs CrowdStrike Falcon LogScale (CQL) queries for Falcon EDR hunting, limited to 67 documented event types and confirmed fields so queries don't use invented schema."
license: "MIT"
tier: "contributed"
tags: ["crowdstrike", "cql", "logscale", "threat-hunting", "mitre-attack", "falcon-edr"]
domains: ["security-operations"]
integrations: ["CrowdStrike"]
date_added: 2026-11-14
contribution_agreement_date: 2026-11-15T01:03:04Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "/crowdstrike-cql-query-writer"
---

A Claude skill for writing CrowdStrike Falcon LogScale (CQL) queries against Falcon EDR telemetry. It keeps Claude to event types and fields that actually exist, so the queries it writes run instead of just looking right.

## What it does

- Generates new CQL queries, repairs broken ones, and explains what an existing query does.
- Covers 67 common `#event_simpleName` values: process, DNS, network, registry, SMB, services, scheduled tasks, drivers, injection, and ransomware-related activity.
- Maps behaviors and telemetry to MITRE ATT&CK techniques and suggests a starter query.
- Includes 17 vetted example queries for common hunts.

## How it works

The skill follows a fixed workflow: identify the target and hunt type, load the relevant reference file, then build the query from confirmed fields. Reference files hold per-event field lists, pivots and join hints, ATT&CK mappings, and example patterns.

If an event is outside the packaged set, it falls back to the closest mapped event, then to a narrow pivot query, and asks for clarification if neither fits. It does not invent fields or events.

## Limits

Only the 67 packaged events are covered. Your environment may expose extra fields, joins may need testing in your tenant, and NG-SIEM parsers vary more than Falcon EDR.
