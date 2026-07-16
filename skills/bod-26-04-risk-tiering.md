---
name: "BOD 26-04 Risk Tiering"
author: "itschrisyo"
github_url: "https://github.com/itschrisyo/bod-26-04-risk-tiering"
description: "Computes CISA BOD 26-04 remediation tiers for Tenable vulnerability findings using the directive's 4-variable model."
license: "MIT"
tier: "contributed"
tags: ["bod-26-04", "cisa", "vulnerability-management", "compliance", "risk-tiering", "kev", "tenable"]
integrations: ["Tenable"]
date_added: 2026-07-16
contribution_agreement_date: 2026-07-16T16:40:40Z
compatible_platforms: ["Claude Code"]
invocation: "/bod-26-04-risk-tiering"
---

This skill automates CISA BOD 26-04 compliance for federal agencies and organizations managing Tenable vulnerability data. It computes remediation tiers using the directive's four-variable risk model: Publicly Exposed × In KEV × Automatable × Technical Impact.

## What it does

Takes Tenable One/TVM vulnerability findings and produces BOD 26-04-compliant remediation tiers with specific deadlines:
- **3-day + forensic triage** (actively exploited KEV on public-facing assets)
- **3-day** (high-risk KEV)
- **14-day** (medium-risk KEV)
- **60-day** (lower-risk)
- **Fix-on-upgrade** (maintenance window)

Pulls data directly from Tenable via Hexa MCP, enriches with CISA Vulnrichment for automation/impact assessments, applies Table 1 logic, and generates action queues with countdown timers from first-seen dates.

## How it works

The skill extracts KEV dates from Tenable Workbench, handles Windows patch bundles by extracting individual CVEs, fetches CISA SSVC assessments via Vulnrichment API, computes tiers using BOD 26-04's 16-row lookup table, and outputs multiple report formats (JSON for automation, CSV for leadership, text for humans). Includes forensic triage flags for potential active breaches and coverage statistics showing CISA data availability.

Production-tested on 500 assets with 539 KEV vulnerabilities, achieving 64.3% CISA coverage. Zero external dependencies (Python stdlib only). 21 unit tests covering all Table 1 rows and edge cases.
