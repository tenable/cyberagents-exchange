---
name: "SOC-Hunter"
author: "sherlon1"
github_url: "https://github.com/sherlon1/soc-hunter"
description: "Proactive, hypothesis-driven threat hunting using the LOCK pattern across SIEM, EDR, VM, CSPM, CASB, and code search"
license: "MIT"
tier: "contributed"
tags: ["threat-hunting", "lock-pattern", "mitre-attack", "siem", "edr", "secops", "incident-response"]
integrations: ["Splunk", "SentinelOne", "Tenable", "Netskope", "CrowdStrike"]
date_added: 2026-07-08
compatible_platforms: ["Claude Code"]
invocation: "/soc-hunter"
---

SOC-Hunter is a Claude Code skill that brings structured, proactive threat hunting to your IR workstation. Instead of waiting for alerts, you form hypotheses and systematically test them across your entire security data stack using the **LOCK pattern** (Learn, Observe, Check, Keep).

## What it does

- Runs seven hunting modes: `hunt`, `research`, `execute`, `review`, `baseline`, `investigate`, and `lookup`
- Orchestrates queries across SIEM, EDR, Vulnerability Management, CSPM, CASB, Log Analytics, IPAM, and Code Search via MCP — in a structured layered correlation approach
- Maps every hunt to MITRE ATT&CK with live STIX coverage analysis and gap detection
- Maintains persistent hunt memory across sessions (`hunts/`, `research/`, `investigations/`)
- Detects statistical deviations from versioned behavioral baselines (sigma scoring)
- Fully vendor-agnostic — configure your own MCP servers, SIEM indexes, and credentials via `CONFIG.md`

## How it works

Each hunt follows four approval-gated phases: **Learn** (hypothesis + ABLE scoping), **Observe** (define normal vs. suspicious, map to data sources), **Check** (count-first query execution across 7 data source layers), and **Keep** (structured hunt file with TP/FP classification and lessons learned). Lightweight investigations use the **TRACE** pattern (Trigger, Recon, Assess, Conclude, Emit) for quick structured triage without full LOCK overhead. Built-in quality tools — `hunt-similar.py`, `hunt-validate.py`, and `attack-lookup.py` — prevent duplicate work and enforce frontmatter consistency across the hunt library.
