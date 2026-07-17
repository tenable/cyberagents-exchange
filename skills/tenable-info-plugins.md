---
name: "Tenable Info Plugins"
author: "jdavies-pub-git"
github_url: "https://github.com/jdavies-pub-git/tenable-info-skill"
description: "Discover, extract, and analyze Tenable INFO-severity plugin data — processes, software, accounts, hardware, and forensic artifacts — from Tenable VM for inventory, forensics, and threat hunting."
license: "MIT"
tier: "contributed"
tags: ["tenable", "vulnerability-management", "info-plugins", "asset-inventory", "forensics", "threat-hunting"]
integrations: ["Tenable"]
date_added: 2026-07-16
contribution_agreement_date: 2026-07-16T21:03:21Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code", "Claude Desktop", "Claude Cowork"]
invocation: "tenable-info-plugins"
---

## What it does

Tenable scans emit findings at five severities, and the INFO-severity ones aren't
vulnerabilities — they're the detailed host telemetry a credentialed scan already
collected but that mostly goes unused: running processes, installed software and
patches, local and cached domain accounts, the last logged-on user, services and
startup items, network shares, physical hardware (CPU, memory, BIOS/model/serial via
DMI), AV/firewall status, and forensic artifacts like recycle-bin contents.

This skill teaches Claude to turn that data into answers. It handles asset inventory
(single-host profiles and fleet-wide hardware/software inventories), forensic and
threat-hunting snapshots (e.g. processes running from suspicious paths, unexpected
admin accounts, deleted-file artifacts), and a plugin-reference lookup — all from
data that already exists in the customer's Tenable Vulnerability Management deployment,
with no new scan required.

## How it works

Rather than hard-coding plugin IDs, the skill discovers the right INFO plugin at query
time via plugin search and confirms its severity before use. It reads plugin output
with the Tenable VM MCP tools for quick looks and environment-wide mining, and documents
where those tools cap out (the outputs endpoint returns only a limited, truncated set
with no host filter). For complete, untruncated results it ships a bundled Python script
that calls the Tenable.io API directly — trying pyTenable first and falling back to a
dependency-free stdlib REST call so it runs even in locked-down environments. Output is
parsed defensively into readable structures and delivered as tables, host profiles,
hunting snapshots, or CSV/HTML reports. API keys are read only from environment
variables, and CSV output is sanitized against spreadsheet formula injection since the
underlying data originates on scanned (possibly compromised) hosts.
