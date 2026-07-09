---
name: "Tenable SC Fixed Vulnerability Trend Builder"
author: "byadler"
github_url: "https://github.com/byadler/tenable-sc-fixed-trend"
description: "Generate weekly/monthly Fixed Vulnerability Trend reports directly from Tenable Security Center — no dependencies, works offline."
license: "MIT"
tier: "unreviewed"
tags: ["tenable-sc", "vulnerability-management", "reporting", "remediation", "trend-analysis"]
integrations: ["Tenable"]
date_added: 2026-06-21
compatible_platforms: ["Claude Code"]
invocation: "py sc_trend.py"
---

Prove your remediation program is working — with a single command.

Security teams spend enormous effort fixing vulnerabilities, yet struggle to show the trend over time. This tool connects directly to your Tenable Security Center and generates a fully visual, standalone HTML report in minutes — showing exactly how many vulnerabilities your team has fixed, week by week, with zero setup and no internet dependency after the first run.

## What it does

- Pulls **Fixed (Patched)** vulnerability data week by week from Tenable SC via REST API
- Generates a standalone HTML report with interactive Chart.js charts:
  - Stacked bar chart by severity (Critical / High / Medium / Low) across up to 52 weeks
  - Trend line with 4-week moving average
  - Period comparison — Last Week / Last Month / Last Quarter / Last Year
  - Full exportable data table
- Supports filtering by Repository and Asset Tag
- Two modes: CLI script (`sc_trend.py`) and Web UI server (`report_builder.py`)

## How it works

Authenticates to Tenable SC using the REST API (`/rest/token`), then queries `/rest/analysis` with `sourceType: "patched"` and the `lastMitigated` filter using the days-based format (`"0:7"` = last 7 days). Iterates week by week for the selected time range and aggregates severity counts using `tool: "sumseverity"`. Generates a self-contained HTML file with inlined Chart.js for offline viewing.

**Key discovery:** Tenable SC's `lastMitigated` filter uses days (not Unix timestamps) — `"0:7"` means mitigated in the last 7 days.

## Requirements

- Python 3.6+
- Network access to Tenable Security Center
- No pip installs required — Python stdlib only
