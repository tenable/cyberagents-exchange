---
name: "Auth Failure Analyzer"
author: "nsolimini"
github_url: "https://github.com/nsolimini/auth-failure-skill"
description: "Diagnoses Tenable Nessus authentication failures by analyzing plugin output from scan results or live MCP lookups, identifying root causes and providing actionable remediation steps."
license: "MIT"
tier: "contributed"
tags: ["authentication", "nessus", "credentialed-scanning", "troubleshooting", "windows", "smb", "wmi", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-07-11
contribution_agreement_date: 2026-07-11T15:22:16Z
compatible_platforms: ["Claude Code", "Claude Desktop"]
invocation: "analyze auth failures on [hostname/IP/asset ID/scan ID]"
---

A skill for diagnosing why Tenable Nessus credentialed scans succeed or fail on a given host. Provide a hostname, IP address, asset ID, scan ID, CSV scan results, or paste plugin information directly — the skill identifies all auth-relevant plugins, classifies the overall authentication status, pinpoints the root cause, and gives numbered remediation steps.

## What it does

- Accepts a hostname, IP, asset ID, scan ID, CSV scan results, or pasted plugin information as input
- Identifies authentication-relevant Nessus plugins (success signals: 141118, 110095, 10394, 10400, 20811; failure signals: 110723, 104410, 21745, and others)
- Classifies overall auth status as ✅ Success, ❌ Failed, or ⚠️ Partial
- Checks plugin 19506 (Nessus Scan Information) as ground truth for `Credentialed checks: yes/no`
- Diagnoses root cause in plain English and provides actionable remediation steps
- Distinguishes Windows (SMB/WMI) vs Linux (SSH) authentication paths and flags mismatches

## How it works

The skill follows a structured lookup strategy:

1. **Live MCP lookup** — if a hostname, IP, or asset ID is provided and the Tenable MCP server is connected, it queries `workbenches_list_assets` → `workbenches_get_asset_vulnerabilities` → `workbenches_get_asset_vulnerability_details` for auth-relevant plugins
2. **Scan ID lookup** — uses `scan_results` and `scan_host_details` to retrieve plugin data for a specific scan run
3. **CSV or pasted plugin information** — if plugin data is provided directly, analysis proceeds immediately without any MCP calls

Results are presented in a structured table with root cause explanation and prioritized fix steps.