---
last_reviewed: 2026-09-03
name: "Tenable Auth Failure Tracker"
author: "rafansmpj"
github_url: "https://github.com/rafansmpj/Tenable-Authentication-Failure-Tracker"
description: "Auto-classifies Tenable credentialed scan auth failures by root cause and tracks remediation cases."
license: "MIT"
tier: "contributed"
tags: ["tenable", "authentication", "credentialed-scan", "root-cause-analysis", "case-management", "dashboard"]
domains: ["platform-operations"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-09-02
contribution_agreement_date: 2026-09-02T01:46:22Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code", "Claude Desktop"]
invocation: "/tenable-auth-failure-tracker"
---

The Tenable Auth Failure Tracker is a Claude skill that turns Tenable credentialed scan authentication failures into a triaged, trackable remediation workflow. It targets SOC leads, remediation engineers, vulnerability managers, and IT operations teams who need to close scan coverage gaps caused by failed authentication.

## What it does

- Collects scan authentication health data from Tenable via the Hexa AI MCP connector, using dedicated auth-health plugins (10428, 19506, 21745, 24786, 26917, 91822, 102094, 104410, 110095, 110385, 110695, 110723, 117885, 122502, 122503, 141118, 150799).
- Auto-classifies each failure by root cause: bad password, insufficient privileges, account locked, firewall timeout, port unreachable, credential missing, service unavailable, privilege escalation failure, connection refused, or other.
- Generates a remediation runbook per root cause and maintains a persistent case ledger (open/in-progress/resolved/pending-validation) with SLA thresholds by severity.
- On re-run, detects Fixed/Regressed/New failures and updates case status automatically; exports the case ledger as JSON for downstream ticketing systems.

## How it works

Pulls scan authentication health data from Tenable One via the Hexa AI MCP (read-only), classifies failures with a root-cause heuristic against plugin output, and renders an interactive standalone-HTML dashboard: failure distribution by root cause, an asset table with SLA status, a runbook drawer per root cause, and a case list. The skill never executes remediation actions itself (no password changes, firewall updates, or privilege changes) — those stay manual, guided by the generated runbooks.
