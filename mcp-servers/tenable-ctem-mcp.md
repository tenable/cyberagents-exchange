---
name: "Tenable CTEM MCP"
author: "mrovere1"
github_url: "https://github.com/mrovere1/tenable-ctem-mcp"
description: "Local MCP server delivering 19 CTEM maturity indicators already aggregated, plus MTTR, with evidence per number"
license: "MIT"
tier: "contributed"
tags: ["ctem", "exposure-management", "vulnerability-management", "maturity-assessment", "security-posture"]
integrations: ["Tenable"]
date_added: 2026-09-04
contribution_agreement_date: 2026-09-04T17:46:23Z
transport: "stdio"
runtime: "python"
auth_method: "api-key"
compatible_clients: ["Claude Code", "Claude Desktop"]
tools_exposed:
  - name: "ctem_discover_tenant"
    description: "Tag categories and values, asset counts by class, exposure surfaces present, scans with history, agents — in one cached call"
  - name: "ctem_preflight"
    description: "Tests every filter the assessment uses live against the tenant, with discriminant pairs, and returns the deny-list with measured proof"
  - name: "ctem_scoping"
    description: "Stage 1 indicators S1–S4: tag coverage, criticality and owner coverage, declared crown jewels"
  - name: "ctem_discovery"
    description: "Stage 2 indicators D1–D4: time since last assessment, licensed surface coverage, agent coverage, authenticated detection share"
  - name: "ctem_prioritization"
    description: "Stage 3 indicators P1–P3 plus the three compared prioritisation queues (CVSS, VPR, overlap)"
  - name: "ctem_validation"
    description: "Stage 4 indicators V1–V4: exploit availability, KEV exposure age, recurrence rate, out-of-support software"
  - name: "ctem_mobilization"
    description: "Stage 5 indicators M1–M4: assessment cadence, largest gap, fix availability age, and MTTR with the cadence guard applied"
  - name: "plugin_details_batch"
    description: "Detail for many plugins in one call, with five fields only — the project's largest token saving"
  - name: "plugin_census"
    description: "Sampling frame: every plugin of a severity with detection count, VPR and family. Cached"
  - name: "scan_cadence"
    description: "Collapses scan runs into distinct assessment days, and always returns the uncollapsed median alongside for contrast"
  - name: "mttr_collect"
    description: "MTTR through the vulnerability export API with polling and chunked download. Never blocks: returns a resumable ticket on timeout"
  - name: "mttr_cadence_guard"
    description: "Detects when an MTTR is really measuring the interval between scans rather than time to fix"
  - name: "ctem_diagnostics"
    description: "Whether the server can reach the tenant. Separates a missing credential from an invalid one from intercepted TLS. Never prints the key"
resources_exposed: []
prompts_exposed: []
---

A local stdio MCP server that moves the aggregation of a CTEM maturity assessment to the server, so
the client receives finished numbers instead of raw pages to add up. Every indicator arrives with the
literal filter that produced it, the sample size, the collection timestamp and a preflight verdict.

## What it does

Returns the 19 indicators of a CTEM maturity assessment across the five stages — Scoping, Discovery,
Prioritization, Validation, Mobilization — in roughly seven tool calls. Time-to-fix is included, which
the inventory API alone cannot reach: the fields that make MTTR computable live behind an export
endpoint with polling and chunked download, wrapped here in a single tool.

A query that fails never becomes a number. It becomes a declared gap with a named cause, and the
indicator leaves the calculation. A silent partial number is treated as the central failure mode to
prevent, because a wrong number that looks right carries no signal that it happened.

The server is read-only. It issues no write to the tenant, and credentials are read only from the
environment — never as a tool parameter, never written to a config file or a log. Certificate
verification cannot be disabled; networks that inspect TLS point at their own CA bundle instead.

## How it works

Three design decisions carry the project, and each came from a problem measured in a real tenant.

**Aggregation on the server.** The raw runs of a recurring scan gave a median assessment cadence of
1.42 days; collapsed into distinct assessment days, 21 — two maturity stages apart, with nothing in
the output signalling the difference. Logic that lives on the client gets re-implemented slightly
differently each time; here it lives in one place and has a regression test.

**Only the fields that are used.** A plugin's full detail is ~8,200 characters across 97 attributes;
the assessment uses five. Returning five is what makes a census of every critical plugin affordable,
and a census removes the confidence interval, the weighting base and the allocation bias a sample
forces you to manage.

**A filter deny-list with measured proof.** The API accepts some filters it does not apply and
returns no error — the query looks filtered and returns the whole corpus. Those are rejected before
the request leaves, each with the discriminant pair that proved it, and `ctem_preflight` re-tests
everything live rather than trusting a recorded verdict.
