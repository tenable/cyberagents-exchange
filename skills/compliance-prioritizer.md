---
name: "Compliance Prioritizer"
author: "dpickenstenable"
github_url: "https://github.com/dpickenstenable/tenable-compliance-prioritization"
description: "AI-powered risk-based prioritization for Tenable VM compliance benchmark failures"
license: "MIT"
tier: "unreviewed"
tags: ["compliance", "vulnerability-management", "risk-assessment", "tenable", "prioritization", "reporting"]
integrations: ["Tenable"]
date_added: 2026-06-23
compatible_platforms: ["Claude Code"]
invocation: "/compliance-prioritizer"
---

The Compliance Prioritizer skill transforms overwhelming compliance scan results into actionable, risk-ranked remediation plans. When security teams face hundreds or thousands of failed compliance checks, this skill applies intelligent risk scoring to focus effort where it matters most.

## What it does

The skill analyzes Tenable Vulnerability Management compliance scans and generates four comprehensive reports:

- **CSV ranked list** — Sortable spreadsheet of all failures by risk score
- **Detailed markdown report** — Executive summary with statistics, risk distribution charts, and top 20 findings with business context
- **Interactive HTML dashboard** — Visual, browser-based interface with color-coded priorities
- **Remediation roadmap** — Three-phase action plan grouped by complexity (quick wins, short-term, long-term)

Each finding is scored using a weighted formula:
- Business Impact (35%) — What does this control protect?
- Asset Criticality (35%) — How important is the affected system?
- Remediation Ease (20%) — How hard is it to fix?
- Exploitability (10%) — Can this be exploited remotely?

The skill supports three input methods: exported CSV/JSON files (no setup), direct Tenable API connection (real-time), or Tenable MCP server integration (fastest for repeated use).

## How it works

The skill reads compliance scan data, applies context-aware risk scoring based on asset criticality and business impact, categorizes findings by remediation complexity, and generates prioritized reports. It intelligently identifies "quick wins" (often 97%+ of failures can be fixed via Group Policy) versus long-term architectural changes, enabling teams to achieve maximum compliance improvement with focused effort.
