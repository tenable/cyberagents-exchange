---
last_reviewed: 2026-10-22
name: "PHP2Shell Tenable Skill"
author: "securibee"
github_url: "https://github.com/securibee/php2shell-tenable-skill"
description: "Reports PHP2Shell (CVE-2026-109618, CVE-2026-109619) exposure from Tenable data via Hexa AI MCP as HTML, PDF and CSV."
license: "MIT"
tier: "contributed"
tags: ["php2shell", "php", "rce", "cve-2026-109618", "cve-2026-109619", "exposure-report", "web-app-scanning"]
domains: ["vulnerability-management"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-10-22
contribution_agreement_date: 2026-10-22T12:34:48Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code"]
invocation: "/php2shell-tenable"
---

Builds a PHP2Shell exposure report from your own Tenable data. Every asset, version and finding in it comes from a Tenable Hexa AI MCP call made during the run. The output is an HTML page, a PDF and a CSV.

## What it does

- Checks that the Hexa AI MCP tools are loaded, and prints the setup command if they aren't.
- Re-reads the Tenable Research PHP2Shell FAQ for the current CVE list, fixed releases and interim mitigations.
- Asks Tenable's plugin database for every plugin covering those CVEs, across Vulnerability Management, Web App Scanning and cloud or container security.
- Pulls active findings by CVE, plus PHP inventory from the version detection plugins.
- Gives each asset a status against the fixed releases: one of three grades of vulnerable, patched, not affected, or unknown.
- Summarizes counts by status, the ten worst assets and the interim mitigations in chat.

It only reads data. It never launches scans, creates tags or changes anything in Tenable.

## How it works

The skill calls `tenable_one_search_findings` by CVE for vulnerable findings and by detection plugin ID for inventory. For VM plugins it reads PHP versions from `workbenches_get_vulnerability_outputs`. Hexa returns at most 10 distinct outputs per call, so the skill repeats the call across age windows from 7 to 365 days and merges the results by asset.

It writes one row per asset and plugin to `findings.json`, then runs `render.py`, a standard-library Python script. `render.py` compares each version to the fixed releases (8.2.35, 8.3.36, 8.4.27, 8.5.12) and writes the report. The PDF comes from a local headless Chrome, and `render.py` makes no network calls.

Status comes from the PHP version alone, so distro packages with backported fixes can show as vulnerable. Check those against the vendor advisory.
