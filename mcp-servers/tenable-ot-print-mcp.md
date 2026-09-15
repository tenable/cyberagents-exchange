---
last_reviewed: 2026-09-01
name: "Tenable One OT Exposure Management Report Generator"
author: "Dominic Storey"
github_url: "https://github.com/dpstorey/EM-PRINT"
description: "MCP server that generates themed Markdown/HTML print reports (asset inventory, vulnerability findings, policy findings, risk profile) from Tenable One OT Exposure Enterprise Manager data, writing output straight to a mounted filestore instead of the model's context window."
license: "Apache-2.0"
tier: "contributed"
tags: ["tenable", "ot-security", "reporting", "ics", "risk-management"]
domains: ["ot-iot-security", "platform-operations"]
integrations: ["Tenable"]
date_added: 2026-08-31
contribution_agreement_date: 2026-08-31T18:19:08Z
transport: "http"
runtime: "python"
auth_method: "token"
compatible_clients: ["Claude Desktop", "Claude Code", "Cursor", "Windsurf", "ChatGPT", "VS Code Copilot"]
tools_exposed:
  - name: "list_report_types"
    description: "List available report types"
  - name: "list_available_columns"
    description: "List available report columns"
  - name: "list_themes"
    description: "List available themes"
  - name: "list_recent_report_jobs"
    description: "List recent report jobs"
  - name: "submit_report_job"
    description: "Generate a print report"
  - name: "save_risk_grade_scale"
    description: "Save a named risk-grade scale table"
  - name: "list_risk_grade_scales"
    description: "List saved risk-grade scale tables"
  - name: "set_report_retention_policy"
    description: "Set report retention policy"
  - name: "get_report_retention_policy"
    description: "Get report retention policy"
  - name: "purge_reports"
    description: "Purge old reports"
resources_exposed: []
prompts_exposed: []
---

An open-source [Model Context Protocol](https://modelcontextprotocol.io) server that turns Tenable One OT Exposure Enterprise Manager data into print-ready reports, without routing the rendered content back through the calling model's context window. Sibling project to the `tenable-ot-mcp-em-edition` listing (same EM-connection pattern) — use that server for interactive querying, and this one when the output is a report someone will actually read: asset inventory, vulnerability findings, policy findings, or a themed risk profile.

## What it does

Exposes 10 MCP tools across four areas: report-module discovery (`list_report_types`, `list_available_columns`, `list_themes`, `list_recent_report_jobs`), report generation (`submit_report_job` — the single generation tool, covering four modules: `asset_inventory`, `vulnerability_findings`, `policy_findings`, `risk_profile`), risk-grade scale management (`save_risk_grade_scale`, `list_risk_grade_scales`) for reusable risk-grading tables on `risk_profile` reports, and retention (`set_report_retention_policy`, `get_report_retention_policy`, `purge_reports`, defaulting to `dry_run=true`).

`submit_report_job` runs synchronously — confirmed live against a real Enterprise Manager on an unfiltered ~3,464-asset `asset_inventory` report in about 20 seconds — and writes a themed Markdown + HTML pair to `MCP_OUTPUT_DIR` (typically a mounted SharePoint/filestore volume), returning only file paths and a short summary to the caller, never the rendered report content.

### What's intentionally not here yet

- **Async job queue** — fine for the workloads tested so far; not guaranteed for a much larger, unbounded fetch with no cancel/poll.
- **Multi-ICP fan-out** — every module queries a single ICP/EM connection; EM-MCP's bounded-concurrency multi-site pattern isn't wired in here.
- **PDF output** — WeasyPrint is an optional dependency, not yet wired into the renderer; Markdown + HTML ship today.

## How it works

A stateless container built on the same FastMCP / Streamable HTTP + bearer-token pattern as EM-MCP: a setup wizard issues a static token that gates the `/mcp` endpoint. Each report module introspects its own `manifest.yaml` for parameters, columns, and output formats; `submit_report_job` renders the requested module through Jinja2 templates into themed Markdown and HTML, writes both to the output directory, and appends a JSON-line audit record. Two themes ship today: `default` and `dark-banner`.
