---
name: "Export Nessus Template"
author: "silee-tenable"
github_url: "https://github.com/silee-tenable/export-nessus-template"
description: "Export scans and policies from Nessus, Tenable.io, or Tenable.sc to Tenable.io, preserving configurations, targets, and schedules"
license: "MIT"
tier: "unreviewed"
tags: ["tenable", "nessus", "vulnerability-scanning", "migration", "scan-automation", "security"]
integrations: ["Tenable"]
date_added: 2026-07-07
compatible_platforms: ["Claude Code"]
invocation: "/export-nessus-template"
---

A Claude Code skill that automates the migration of vulnerability scans and policies between Tenable platforms, preserving all configurations, targets, schedules, and credentials.

## What it does

This skill streamlines the process of migrating vulnerability scans and scan policies across Tenable platforms. It supports:

- **Live system exports** from Nessus Professional/Manager, Tenable.io, and Tenable.sc
- **File-based imports** from `.nessus` XML export files
- **Full configuration preservation** including targets, schedules, credentials, plugin settings, and compliance audits
- **Intelligent API mapping** that handles differences between source platforms

The skill authenticates to your source system, fetches the complete scan or policy configuration via REST API, transforms it to match Tenable.io's format, and recreates it with all settings intact.

## How it works

1. **Authentication** — Connects to the source system using provided credentials or environment variables
2. **Configuration retrieval** — Fetches the complete scan/policy configuration including all advanced settings
3. **Intelligent transformation** — Maps source-specific settings to Tenable.io equivalents:
   - Scan targets and CIDR ranges
   - Schedules (cron/rrules format)
   - Email notifications and scan zones
   - Credentials (SSH, Windows, SNMP, database)
   - Plugin families and individual plugin configurations
   - Compliance audit files and checks
4. **Recreation in Tenable.io** — Uses the Tenable MCP server to create policies and scans with preserved settings
5. **Verification** — Reports the new scan ID, UI link, and any settings requiring manual review

## Use cases

- **Platform migrations** — Moving from Nessus Professional/Manager to Tenable.io
- **Multi-tenant deployments** — Replicating scan templates across Tenable.io containers
- **Scan template library** — Importing standardized scan configurations from `.nessus` files
- **DR/backup recovery** — Restoring scan configurations from exported templates

## Requirements

- Claude Code with Tenable MCP server configured
- Source system credentials (API keys for live systems, or `.nessus` file for offline imports)
- Destination Tenable.io instance with appropriate permissions

## Example usage

**Export from Nessus:**
```
/export-nessus-template https://nessus.example.com:8834 "Weekly Network Scan" --access-key abc123 --secret-key xyz789
```

**Import from file:**
```
/export-nessus-template /path/to/scan-template.nessus
```
