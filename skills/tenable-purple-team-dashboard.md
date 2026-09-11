---
name: "Tenable Purple Team Dashboard"
author: "rafansmpj"
github_url: "https://github.com/rafansmpj/tenable-purple-team-dashboard"
description: "Joins Tenable pentest/attack-path findings against Blue Team remediation to compute residual risk and an ATT&CK coverage heatmap."
license: "MIT"
tier: "contributed"
tags: ["purple-team", "red-team", "blue-team", "mitre-attack", "residual-risk", "vulnerability-management", "dashboard"]
integrations: ["Tenable"]
date_added: 2026-09-11
contribution_agreement_date: 2026-09-11T14:55:28Z
compatible_platforms: ["Claude Code", "Claude Desktop", "Claude Cowork"]
invocation: "/tenable-purple-team-dashboard"
---

The Tenable Purple Team Dashboard skill joins Red Team attack findings (pentest / attack-path results tagged with MITRE ATT&CK techniques) against Blue Team remediation and compliance evidence, answering the question two separate silos can't: given what Blue actually fixed, what can Red still do?

## What it does

Pulls findings, asset exposure, finding state, and compliance/IoE data live from the Tenable MCP (Tenable One / VM / Identity Exposure / ASM), optionally overlaid with uploaded pentest evidence, ticket exports, or GRC mappings. Produces a single standalone HTML dashboard with a scorecard (Red findings next to Blue mitigations), an ATT&CK technique heatmap, a validation scoreboard for re-tested mitigations, a residual-risk rollup, a data-quality tab, and a run-over-run changes tab.

## How it works

`scripts/purple_join.py` normalizes and joins the three Tenable entities plus any overlays on finding ID or shared ATT&CK technique ID, then scores residual risk as unmitigated finding × severity × exploitability × exposure × asset criticality — a closed-but-unvalidated ticket keeps 40% of its risk by default, only a Red-confirmed retest drops it to zero. `scripts/render_dashboard.py` renders the scored state into a standalone HTML file (inline CSS/JS, no CDN) with the state embedded so the previous run alone is enough to compute the next delta. It's read-only: nothing is written back to Tenable, ticketing, or GRC systems.
