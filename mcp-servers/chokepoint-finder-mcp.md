---
last_reviewed: 2026-08-05
name: "Chokepoint Finder MCP Server"
author: "tarhou"
github_url: "https://github.com/tarhou/chokepoint-finder-mcp"
description: "A FastMCP server that collapses findings into shared fixes, ranks them by marginal risk coverage, gates unsafe changes on fail-closed evidence, and verifies outcomes against the authoritative source."
license: "MIT"
tier: "contributed"
tags: ["vuln-management", "exposure-management", "remediation", "prioritization", "attack-path-analysis", "set-cover", "fail-closed", "mcp-server"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T02:04:27Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop"]
transport: "stdio"
runtime: "python"
auth_method: "api-key"
tools_exposed:
  - name: "chokepoint_setup"
    description: "Reports what is configured, tests each connection, and names the exact missing variable rather than failing vaguely."
  - name: "chokepoint_ingest"
    description: "Loads findings, assets and attack paths from a source and builds the engine baseline."
  - name: "chokepoint_rank"
    description: "Greedy weighted max-coverage over synthesized actions; returns the ordered shortlist with marginal risk."
  - name: "chokepoint_preflight"
    description: "Evidence gates before acting: EDR silence, change freeze, and blast radius."
  - name: "chokepoint_supply_evidence"
    description: "Relays gate evidence in from an MCP server you already have connected, with provenance retained."
  - name: "chokepoint_payload"
    description: "Ticket-ready remediation payload for a chokepoint: summary, justification, targets and rollback."
  - name: "chokepoint_plan"
    description: "Typed, ordered execution workflow with per-site waves and a canonical SHA-256 plan hash."
  - name: "chokepoint_mark_executed"
    description: "Records that approved steps were executed elsewhere, bound to the plan hash, wave and a one-time receipt."
  - name: "chokepoint_verify"
    description: "Re-queries the authoritative source and diffs against the baseline, returning a structured proof receipt."
  - name: "chokepoint_demo"
    description: "Runs the whole wave-aware loop on a deterministic simulated estate with no credentials."
resources_exposed: []
prompts_exposed: []
---

The engine behind the Chokepoint Finder method, exposed as ten typed MCP tools. It runs
end to end with **zero credentials** against a deterministic simulated estate, so the
mechanics can be inspected before any real tenant is connected.

## What it does

Most tooling ranks findings individually. That is the wrong unit of work: one patch
rolled out fleet-wide, one base image rebuilt, one IAM role scoped, or one security
group closed retires hundreds of findings at once. This server groups findings by the
fix they share, then solves for the shortest ordered list of actions that removes the
most weighted risk — reporting, for each action, what it retires *given everything above
it is already done*.

It also carries the parts that usually get hand-waved: pre-flight refusal on evidence,
approval binding, and verification against the source of truth rather than against its
own memory of what it asked for.

## How it works

**Ranking.** Greedy weighted maximum coverage over an action-to-findings coverage
matrix. Marginal value means overlap is credited exactly once, so coverage sums to the
total instead of past it. Under a pure cardinality constraint this is the classical
greedy carrying the (1 − 1/e) guarantee; the README states plainly which configuration
options preserve that bound and which are heuristics that forfeit it.

**Fail-closed evidence.** Gates read typed evidence carrying source, collection time and
completeness. Anything unconfigured, failed, partial, truncated or stale resolves to
`UNKNOWN`, and `UNKNOWN` produces `HOLD`. An empty result from a healthy feed is
`ABSENT` — a genuinely different state — and does clear the gate. Misconfiguration can
therefore only make the server more cautious, never less.

**Composable evidence.** The server holds no EDR, SIEM or ITSM credentials and never
will. Telemetry arrives through `chokepoint_supply_evidence`, relayed from MCP servers
the operator already runs, with provenance preserved so a relayed third-party detection
is never filed as if the server had observed it directly. Because a relaying agent could
in principle understate risk, evidence that would *widen* permission is surfaced to a
human with a payload digest and requires a recent one-time confirmation, while evidence
that can only make the outcome more cautious is accepted directly.

**Verification.** `chokepoint_verify` re-queries the authoritative source and diffs
against the recorded baseline, returning counts for retired, reappeared and remaining
findings. Simulated runs are labelled as such and can never be presented as closure
evidence for a real change record.

Transport is stdio by default; an HTTP mode exists for local development and refuses to
bind anywhere but loopback. Tenable and AWS collectors are read-only. The safety
properties above are asserted by the test suite rather than promised in prose, including
tests that inject drift and assert the checks fail.
