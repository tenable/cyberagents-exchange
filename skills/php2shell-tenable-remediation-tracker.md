---
last_reviewed: 2026-10-26
name: "PHP2Shell Tenable Remediation Tracker"
author: "rafansmpj"
github_url: "https://github.com/rafansmpj/php2shell-tenable-remediation-tracker"
description: "Tracks PHP2Shell and Node2Shell remediation from Tenable data with SLA tracking, VPR and run-to-run comparison."
license: "MIT"
tier: "contributed"
tags: ["php2shell", "node2shell", "cve-2026-109618", "cve-2026-109619", "cve-2026-111497", "remediation-tracking", "sla"]
domains: ["vulnerability-management"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-10-26
contribution_agreement_date: 2026-10-26T02:38:58Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code", "Claude Desktop", "Claude Cowork"]
invocation: "/php2shell-tenable-remediation-tracker"
---

Tracks exposure to and remediation of PHP2Shell, the pre-auth PHP remote code execution disclosed on 2026-10-21 (CVE-2026-109618, CVE-2026-109619), using live data from the Tenable Hexa AI MCP. It also tracks the related Node2Shell Brotli decoder RCE (CVE-2026-111497: Node.js, libbrotli, Python Brotli) in a separate section that is kept out of the PHP2Shell numbers. Every run produces an HTML, PDF and CSV report and adds to an execution history, so each new report shows what changed since the last one. The skill is read-only and never launches scans or changes anything in Tenable.

## What it does

- Asks up front whether this is the first run, which language the report should use (English, Portuguese-BR, Spanish or a custom translation) and which remediation SLA to measure against (7 days by default).
- Searches Tenable for every plugin mapped to each CVE on every run (WAS, VM and Cloud/container), so new distro and container checks are picked up automatically instead of relying on a fixed plugin list.
- Collects vulnerable (ACTIVE/RESURFACED) and fixed (FIXED) findings per plugin. Each finding comes with its first-seen and fixed dates, the installed version, the plugin's VPR, and the asset's ACR and AES.
- Tracks every finding against the SLA: due date, days open, and whether the SLA was met or missed.
- Compares the run with any earlier one. It shows new, remediated, regressed, still-open and no-longer-reported findings, KPI deltas and a trend chart across the full history.
- Produces a CISO-ready report with one section per vulnerability (PHP2Shell and Node2Shell). Each section has:
  - a posture label (CRITICAL / HIGH / GUARDED / CONTROLLED), an executive summary and business-risk asks
  - KPIs and an assets-by-version-status breakdown, where any figure can be clicked to list the assets behind it
  - a per-plugin drill-down with affected assets, target version, remediation steps and interim mitigations
- Includes an in-report export menu for the HTML and the JSON execution history.

## How it works

Claude follows `SKILL.md` to query Tenable through the Hexa AI MCP and check fixed releases against the Tenable Research PHP2Shell FAQ. It then writes the findings and plugin catalog for each vulnerability as JSON. A bundled Python renderer (`scripts/render.py`, standard library only, with optional Playwright for the PDF) turns them into timestamped report files. It also updates a rolling `history.json` ledger that the next run reads to build its comparison. Every finding is keyed on asset + plugin ID, and each report embeds the full history. Either the stamped `history_<stamp>.json` or `report_<stamp>.html` is enough to continue tracking in a later session.
