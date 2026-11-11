---
name: "Tenable One Attack Path Firewall Validation"
author: "arnzg"
github_url: "https://github.com/arnzg/tenable-attack-path-firewall"
description: "Validates Tenable One attack paths against your firewall rulebase and surfaces the paths that actually survive."
license: "MIT"
tier: "contributed"
tags: ["attack-path-analysis", "firewall", "network-security", "fortinet", "exposure-management", "remediation", "risk-prioritisation"]
domains: ["network-security", "vulnerability-management"]
integrations: ["Tenable", "Fortinet"]
date_added: 2026-11-06
contribution_agreement_date: 2026-11-06T00:00:00Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "/tenable-attack-path-firewall"
---

Attack-path analysis tells you what an attacker *could* do. Firewall policy decides what they
*can actually reach*. This skill joins the two and produces a prioritised, SOC-ready
dashboard of the attack paths that survive your rulebase — plus the policy changes that
cut them.

## What it does

- Pulls attack paths from Tenable One (Exposure Management) and evaluates every
  network-relevant hop against a firewall rulebase using first-match-wins / default-deny
  semantics (FortiGate reference implementation; vendor-neutral model for Palo Alto,
  Check Point and others).
- Classifies paths as **live** (every hop passes a named allow rule), **blocked**
  (overstated risk — the firewall already cuts them), or **possible exposure** (the
  exploit's port is unknown; verify before acting). Unknown-port hops are never counted
  as live without evidence.
- Overlays EDR presence from the tenant's third-party connector sources and exploit
  data from CISA KEV, and resolves exploit ports using the target's own scan evidence
  (via the supported `/vulns/export` endpoint).
- Runs a **remediation what-if simulator**: every candidate policy change is replayed
  through the full correlation, with computed deltas ("this deny rule cuts 149 paths").
- Emits a triage queue, ranked callouts, per-hop remediation options (firewall change /
  containment / patch) and ready-to-file remediation tickets.

## How it works

1. Fetches the APA topology (`top-attack-paths/search`), extracts network-relevant hops
   and maps the technique families to protocol/ports.
2. Normalizes the firewall rulebase (vendor MCP server, imported `--rules` JSON, or an
   explicitly confirmed simulation) and evaluates each hop through the policy chain.
3. Correlates results into path verdicts, then renders a single self-contained HTML
   dashboard — no external dependencies, safe to share.

## Requirements

- A Tenable One / Exposure Management MCP server with populated Attack Path Analysis.
- A firewall source: a vendor MCP server exposing policies/interfaces/zones (Fortinet,
  Palo Alto, Check Point, Cisco), an exported rulebase JSON, or the bundled simulator
  (demo mode, clearly labeled).
- Python 3.9+ (stdlib only). The topology fetch is the only direct API call (no MCP tool
  exists for it); keys are read in-process from the MCP server configuration or supplied
  via `TIO_ACCESS_KEY` / `TIO_SECRET_KEY` environment variables and are never printed.
