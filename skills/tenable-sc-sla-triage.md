---
name: Tenable SC SLA Triage
author: drmodo
github_url: https://github.com/drmodo/tenable-sc-sla-triage
description: An Agent Skill that analyzes a Tenable Security Center instance for remediation SLA compliance and produces a VPR-prioritized remediation queue with CISA KEV cross-referencing. Use when working with Tenable.sc vulnerability data, SLA aging, or remediation prioritization.
license: MIT
tier: contributed
tags:
  - tenable
  - vulnerability-management
  - sla
  - vpr
  - kev
  - security-center
integrations:
  - Tenable
date_added: 2026-07-18
compatible_platforms:
  - Claude Code
invocation: /tenable-sc-sla-triage
---

A read-only Agent Skill that connects to Tenable Security Center (Tenable.sc), ages open findings against remediation SLAs, and produces a risk-prioritized remediation queue.

## What it does
- Pulls cumulative (open) findings from Tenable.sc via the API
- Ages each finding from its Vulnerability Discovered date — the correct SLA clock, not "last seen"
- Prioritizes by VPR rather than static CVSS, and flags CISA KEV findings as top priority
- Outputs an executive summary, an approaching-breach watchlist, and a ranked remediation queue (CSV)

## How it works
Install the skill into your agent's skills directory and point it at a Tenable.sc instance (API access + secret keys). It queries the cumulative vulnerability database, computes SLA aging by VPR tier, cross-references the CISA Known Exploited Vulnerabilities catalog, and writes a prioritized report. Read-only by design — it never launches scans or modifies the instance. Bundles a query-syntax reference and a pyTenable script.
