---
name: "Navi"
author: "packetchaos"
github_url: "https://github.com/packetchaos/navi"
description: "Command-line Swiss Army knife for Tenable Vulnerability Management that automates cyber exposure tasks via the Tenable.io API."
license: "GPL-3.0-only"
tier: "unreviewed"
tags: [tenable, vulnerability-management, cli, tenable-io, cyber-exposure, automation, reporting]
integrations: [Tenable]
date_added: 2026-07-15
---

Navi is a command-line tool that leverages the Tenable.io API to automate common
Vulnerability Management and Cyber Exposure workflows. It pulls your Tenable data into a
local SQLite database (`navi.db`) and exposes a rich set of subcommands for exploring,
tagging, exporting, scanning, and reporting on assets and findings.

## What it does

Navi turns repetitive Tenable.io operations into one-line commands: sync assets and
vulnerabilities locally, tag assets by plugin/CVE/CPE/CISA-KEV/port/route, calibrate Asset
Criticality Ratings, export CSVs (assets, vulns, compliance, SLA breaches, by-tag with
ACR/AES), control and evaluate scans, work with WAS/DAST data, and email reports (via
Resend or classic SMTP). Threaded downloads pull assets in 50-asset chunks across
10 threads for speed at scale.

## How it works

Navi is a Python CLI (installable via `setup.py`/`requirements.txt` or Docker). It
authenticates to Tenable.io with API keys, caches results in `navi.db` for fast local
querying, and drives all write operations (tags, ACR, scans) through the Tenable API. It
underpins the companion navi skills and the navi-mcp server, which expose the same
capabilities to AI assistants.
