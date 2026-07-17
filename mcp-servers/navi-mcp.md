---
name: "navi-mcp"
author: "packetchaos"
github_url: "https://github.com/packetchaos/navi-mcp"
description: "MCP server exposing the Tenable navi CLI (Tenable VM / Tenable One) as 19 tools, plus companion Claude skills."
license: "MIT"
tier: "contributed"
tags: [tenable, navi, mcp, vulnerability-management, exposure-management, asset-tagging, fastmcp]
integrations: [Tenable, Anthropic]
date_added: 2026-07-15
last_reviewed: 2026-07-17
contribution_agreement_date: 2026-07-15T18:28:10Z
transport: "both"
runtime: "python"
auth_method: "none"
compatible_clients: [Claude Desktop, Claude Code, Cursor]
tools_exposed:
  - name: "navi_config_update"
    description: "Sync navi.db from Tenable (assets, vulns, WAS, etc.)."
  - name: "navi_config"
    description: "Read or set navi configuration values."
  - name: "navi_explore_query"
    description: "Run a raw SQL query against navi.db."
  - name: "navi_explore_data"
    description: "Explore navi data (CVE, exploit, software, ports, routes, assets, and more)."
  - name: "navi_explore_info"
    description: "List environment info (users, scanners, scans, policies, tags, agents, etc.)."
  - name: "navi_explore_api"
    description: "Call an arbitrary Tenable API endpoint."
  - name: "navi_enrich_tag"
    description: "Tag assets by plugin, CVE, CPE, CISA KEV, port, route, group, or query."
  - name: "navi_enrich_acr"
    description: "Adjust Asset Criticality Rating (set/inc/dec) with a change reason."
  - name: "navi_enrich_add"
    description: "Add assets to Tenable from an external source."
  - name: "navi_export"
    description: "Export data to CSV (assets, vulns, compliance, by-tag with ACR/AES, and more)."
  - name: "navi_scan"
    description: "Create, start, stop, or evaluate scans."
  - name: "navi_was"
    description: "Work with Tenable WAS (web application scanning / DAST) data."
  - name: "navi_action_delete"
    description: "Delete tags, users, scans, assets, agents, or exclusions."
  - name: "navi_action_rotate"
    description: "Rotate a user's API keys."
  - name: "navi_action_cancel"
    description: "Cancel a running export."
  - name: "navi_action_encrypt"
    description: "Encrypt a file."
  - name: "navi_action_decrypt"
    description: "Decrypt a file."
  - name: "navi_action_mail"
    description: "Email a report or file (Resend or SMTP)."
  - name: "navi_action_push"
    description: "Push a shell command or file to a remote Linux host (double-gated)."
resources_exposed:
  - name: "navi://workdir"
    description: "The navi working directory and database location."
  - name: "navi://schema/assets"
    description: "Schema for a navi.db table (templated by table name)."
  - name: "navi://skill/navi-core"
    description: "A bundled navi skill's content (templated by skill name)."
prompts_exposed:
  - name: "navi_workflow"
    description: "Guided prompt that suggests a navi workflow for a described task."
---

navi-mcp is a Model Context Protocol server that exposes the [Tenable **navi**
CLI](https://github.com/packetchaos/navi) (Tenable Vulnerability Management / Tenable One)
to AI assistants. It ships alongside 13 companion Claude skills that document how to drive
it well, the result of a full audit and rebuild verified against an authoritative recursive
`navi --help` capture.

## What it does

The server surfaces 19 tools spanning navi's full workflow — config/sync, data exploration
and raw SQL, asset tagging, ACR calibration, CSV export, scan control, WAS/DAST, and gated
actions (delete, key rotation, encrypt/decrypt, email, remote push). It also exposes navi
schema, working directory, and skill content as MCP resources, plus a workflow prompt.
Write and high-risk actions are gated (e.g. `NAVI_MCP_ALLOW_WRITES=1`, plus a second gate
for remote execution and email).

## How it works

Built on FastMCP (Python), the server runs over stdio by default (Claude Desktop / Claude
Code) or streamable HTTP with `--http`. The MCP layer itself requires no auth; navi
authenticates to Tenable out-of-band with API keys. The repo bundles the server, the
13 corrected skills (in `NAVI_SKILL_DIR` layout and as packaged `.skill` files), an install
config generator, and step-by-step install docs.
