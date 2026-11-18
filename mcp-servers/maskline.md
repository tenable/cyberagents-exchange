---
last_reviewed: 2026-11-04
name: "maskline"
author: "EngineeringErgonomics"
github_url: "https://github.com/EngineeringErgonomics/maskline"
description: "An MCP server that scans AI agent transcripts and build logs for leaked secrets, including shell-trace lines, and returns a redacted copy with a plain report."
license: "MIT"
tier: "contributed"
tags: ["secrets-detection", "log-redaction", "agent-transcripts", "python"]
domains: ["data-security", "ai-security"]
integrations: []
date_added: 2026-11-03
contribution_agreement_date: 2026-11-01T15:33:43Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: []
tools_exposed:
  - name: "scan_text"
    description: "Scan a text string for leaked secrets and return the findings with a redacted copy."
  - name: "scan_file"
    description: "Scan a file for leaked secrets and return the findings with a redacted copy."
resources_exposed: []
prompts_exposed: []
---

maskline is an MCP server for one step in the agent workflow: check text before you share it. It scans AI agent transcripts and build logs for leaked secrets, including shell-trace lines, and returns a redacted copy with a plain report.

## What it does

The server exposes two tools. `scan_text` takes a text string. `scan_file` takes a file. Each tool returns the findings, by line and rule name, and a redacted copy of the input. A reviewer can share the redacted copy in place of the raw log and does not search the log by hand first.

## How it works

The scan core uses named patterns and runs in Python with the standard library only. The patterns cover PEM header lines, token prefixes, `KEY=value` lines, shell-trace lines such as `+ export KEY=...`, and high-entropy runs. The server runs over MCP stdio and needs no network access and no model call for the core scan. A plain demo mode (`python3 server.py --demo`) scans the bundled synthetic example files, so a first run needs no secret and no service.

This is a first-pass scanner. It can miss secrets (false negatives) and it can flag text that is not a secret, such as long hashes (false positives). Treat a clean report as a check, not a guarantee.
