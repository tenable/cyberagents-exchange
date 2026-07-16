---
name: "Purple AI MCP Server"
author: "Sentinel-One"
github_url: "https://github.com/Sentinel-One/purple-mcp"
description: "Read-only MCP server for SentinelOne's Singularity Platform — query Purple AI, alerts, vulnerabilities, misconfigurations, and asset inventory via natural language or PowerQuery."
license: "MIT"
tier: "unreviewed"
tags: ["sentinelone", "purple-ai", "alerts", "vulnerability-management", "asset-inventory", "power-query", "singularity-platform"]
integrations: ["SentinelOne"]
date_added: 2026-07-09
transport: "both"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Desktop", "Claude Code", "Codex", "Cursor"]
tools_exposed:
  - name: "purple_ai"
    description: "Ask security questions and investigate threats using SentinelOne's Purple AI"
  - name: "powerquery"
    description: "Run PowerQuery analytics against events in your SentinelOne data lake"
  - name: "get_alert"
    description: "Get details for a specific alert"
  - name: "list_alerts"
    description: "List recent alerts"
  - name: "search_alerts"
    description: "Search alerts with filters"
  - name: "get_alert_notes"
    description: "Get comments/notes on an alert"
  - name: "get_alert_history"
    description: "View an alert's timeline"
  - name: "get_vulnerability"
    description: "Get details for a specific vulnerability"
  - name: "list_vulnerabilities"
    description: "List recent vulnerabilities"
  - name: "search_vulnerabilities"
    description: "Search CVEs and vulnerability findings with filters"
  - name: "get_vulnerability_notes"
    description: "Get comments on a vulnerability"
  - name: "get_vulnerability_history"
    description: "View a vulnerability's timeline"
  - name: "get_misconfiguration"
    description: "Get details for a specific misconfiguration"
  - name: "list_misconfigurations"
    description: "List recent misconfiguration issues"
  - name: "search_misconfigurations"
    description: "Search misconfigurations by criteria"
  - name: "get_misconfiguration_notes"
    description: "Get comments on a misconfiguration"
  - name: "get_misconfiguration_history"
    description: "View a misconfiguration's timeline"
  - name: "get_inventory_item"
    description: "Get details for a specific asset"
  - name: "list_inventory_items"
    description: "List assets by surface type (endpoints, cloud resources, identities, network devices)"
  - name: "search_inventory_items"
    description: "Search asset inventory with advanced filters"
resources_exposed: []
prompts_exposed: []
---

Purple AI MCP Server gives any MCP-compatible client read-only access to SentinelOne's Singularity Platform: Purple AI natural-language security Q&A, PowerQuery analytics over the data lake, and structured access to alerts, vulnerabilities, misconfigurations, and asset inventory (endpoints, cloud resources, identities, network devices).

## What it does

- **Purple AI Q&A** — ask free-form security questions and investigate threats through SentinelOne's Purple AI.
- **PowerQuery access** — run PowerQuery analytics directly against events in your SentinelOne data lake.
- **Alerts, vulnerabilities, and misconfigurations** — get, list, search, and pull notes/history for each, so an assistant can triage and correlate without leaving the chat.
- **Asset inventory** — query endpoints, cloud resources, identities, and network devices by surface type or filter.
- **Read-only by design** — the server cannot make changes to the account or any objects in it; it is a query/investigation layer only.

## How it works

The server is a Python package (installable via `uv`/`uvx` or Docker) that authenticates to a SentinelOne console using an Account- or Site-scoped service user token (`PURPLEMCP_CONSOLE_TOKEN` + `PURPLEMCP_CONSOLE_BASE_URL`). It supports `stdio`, `sse`, and `streamable-http` transports, so it works with local clients (Claude Desktop, Claude Code, Cursor, Codex, Zed) as well as remote/serverless deployments (Docker, Amazon Bedrock AgentCore, Amazon ECS). The server itself enforces no authentication at the transport layer — for network-exposed deployments, SentinelOne's docs direct you to place it behind a reverse proxy or load balancer. It is maintained by SentinelOne in partnership with the open source community; it is not a formal SentinelOne product.
