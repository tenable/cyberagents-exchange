---
last_reviewed: 2026-08-19
name: Tenable Scan to CSV
author: conard0-git
github_url: https://github.com/conard0-git/tenable-scan-to-csv
description: Download latest completed Tenable Security Center scans and emit filtered-column CSVs.
license: MIT
tier: contributed
tags:
  - tenable
  - security-center
  - nessus
  - csv
  - scan-export
integrations:
  - Tenable
date_added: 2026-08-14
contribution_agreement_date: 2026-08-14T18:00:20Z
compatible_platforms:
  - Claude Code
invocation: /tenable-scan-to-csv
---

Download the latest completed instance of each caller-supplied Tenable Security Center scan, extract the `.nessus` XML, and emit filtered-column CSVs to a dated monthly directory. Idempotent by design: skips scans whose latest-dated CSV already exists and prunes older versions on rewrite.

## What it does

- Connects to a Tenable Security Center console using env-var-supplied API keys (read-only: list and download only).
- Reads a caller-supplied scan-name list and a caller-supplied column mapping. There is no baked-in column set; any Nessus field the lookup can resolve is valid.
- For each scan, finds the latest **completed** instance, skips the download if that CSV already exists, otherwise downloads the ZIP, stream-parses the `.nessus` XML, and writes `{scan}_{YYYY-MM-DD}.csv`.
- Falls back to `HOST_END` tags when the API `finishTime` is missing, so filenames always carry a real completion date.

Security Center-specific. Tenable Vulnerability Management (Tenable.io) is not targeted.

## How it works

Uses `pytenable`'s `TenableSC` client to list scan instances and `POST /rest/scanResult/{id}/download` for the ZIP. The `.nessus` XML is parsed with `iterparse` so multi-hundred-megabyte scans stay in flat memory. Each CSV column is resolved in order: ReportItem attribute → child element → host property → namespace-qualified compliance-check field.

Install by cloning into `~/.claude/skills/tenable-scan-to-csv` (or `.claude/skills/` in a project) and invoke with `/tenable-scan-to-csv`.
