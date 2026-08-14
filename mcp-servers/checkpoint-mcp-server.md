---
name: "Check Point Management Write-Path MCP Server"
author: "tarhou"
github_url: "https://github.com/tarhou/checkpoint-mcp-server"
description: "Draft/publish/install access-rule lifecycle for compensating-control workflows -- the write path Check Point's official read-only MCP does not expose."
license: "MIT"
tier: "contributed"
tags: ["firewall", "compensating-controls", "check-point", "network-security", "python"]
integrations: ["Check Point"]
date_added: 2026-07-29
contribution_agreement_date: 2026-07-29T07:48:29Z
last_reviewed: 2026-07-31
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop"]
tools_exposed:
  - name: "checkpoint_list_access_rules"
    description: "List current rules in an access layer"
  - name: "checkpoint_add_access_rule"
    description: "Add a rule in the current session (status: draft until published)"
  - name: "checkpoint_publish_session"
    description: "Commit drafted rules to the management server (draft to published)"
  - name: "checkpoint_install_policy"
    description: "Push published rules to gateways (published to installed -- the rule actually enforces)"
resources_exposed: []
prompts_exposed: []
---

An MCP server for **Check Point Management** write-path workflows: draft an access rule, publish the session, install policy — the full compensating-control lifecycle as typed MCP tools. Originally built for a live orchestration demo at Tenable EXPOSURE 2026 (Boston), where an AI agent deployed a compensating firewall control for an unpatchable industrial asset under human supervision.

## What it does

Check Point's official MCP bundle (`@chkp/quantum-management-mcp`) is read-only by design. But the classic vulnerability-management move for an asset you cannot patch — block traffic to it — needs `add-access-rule`, `publish`, and `install-policy`. This server fills that write-side gap with the three-stage lifecycle (draft → published → installed) matching the real Management API state machine, so an AI agent's audit trail reads exactly like a human operator's, and a supervising human gets two natural gates before anything enforces.

## How it works

FastMCP v3 server whose tool surface mirrors Check Point's Management API (`add-access-rule`, `publish`, `install-policy`, `show-access-rulebase`). The backend is deliberately in-memory — safe for demos, agent development, and workflow testing with zero credentials — and the interfaces are designed so the official `cp_mgmt_api_python_sdk` slots in for production against Smart-1 Cloud or on-prem without changing tool signatures or response shapes. All outputs are Markdown rule tables and lifecycle status summaries.
