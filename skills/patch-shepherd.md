---
last_reviewed: 2026-08-05
name: "Patch Shepherd"
author: "kstrycharz"
github_url: "https://github.com/kstrycharz/patch-shepherd"
description: "Clusters Tenable vulnerability findings into prioritized, trend-aware remediation campaigns for analysts, managers, and executives."
license: "MIT"
tier: "contributed"
tags: ["vulnerability-management", "remediation", "tenable", "risk-prioritization", "exposure-management", "security-operations"]
integrations: ["Tenable"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T20:24:28Z
compatible_platforms: ["Claude Code"]
invocation: "/patch-shepherd"
---

Patch Shepherd turns raw Tenable vulnerability data into a small number of prioritized, actionable remediation campaigns — instead of a severity-sorted list of thousands of individual findings.

## What it does

- Clusters individual Tenable findings into root-cause remediation campaigns (one shared fix, potentially many affected assets), rather than just re-sorting findings by severity.
- Scores each campaign with a transparent priority formula (VPR × asset criticality, boosted for Critical/High severity) and a one-sentence rationale explaining why it matters.
- Suggests an owning team for each campaign (Linux/Unix, Windows/AD, Database, Network, Container/Platform, OT/ICS, etc.) via keyword-based routing.
- Detects trend over time by comparing each pull against the prior archived snapshot — surfacing newly affected assets and resolved findings per campaign.
- Produces three audience-specific outputs from the same underlying data: an analyst worklist, a manager update (what's fixed / spreading / still open), and an executive summary (exposure trend, critical campaigns, top 5 risks, plain-English narrative).

## How it works

A Python script pulls live asset and finding data directly from the Tenable inventory export API and writes it to CSV. A second script clusters those findings by shared solution text (falling back to finding name when solution text is generic or missing, to avoid conflating unrelated fixes under boilerplate advice), ranks the resulting campaigns, and writes the JSON/CSV/Markdown outputs described above. Each pull is archived so the next run can diff against it for trend detection.
