---
name: "SentinelOne MCP Server (s1-secops-mcp)"
author: "Sentinel-One"
github_url: "https://github.com/Sentinel-One/ai-siem/tree/main/mcp/s1-secops-mcp"
description: "Zero-dependency Node.js MCP server orchestrating the SentinelOne Management Console, Singularity Data Lake, UAM Alert Interface, and Hyperautomation APIs — 26 tools over stdio or Streamable HTTP."
license: "MIT"
tier: "contributed"
tags: ["sentinelone", "powerquery", "singularity-data-lake", "soc", "hyperautomation", "uam", "mcp"]
integrations: ["SentinelOne"]
date_added: 2026-07-09
transport: "both"
runtime: "node"
auth_method: "token"
compatible_clients: ["Claude Desktop", "Claude Code"]
tools_exposed:
  - name: "powerquery_enumerate_sources"
    description: "Enumerate live dataSource.name values available in the Singularity Data Lake"
  - name: "powerquery_run"
    description: "Run a PowerQuery against the Singularity Data Lake and return results"
  - name: "powerquery_schema_discover"
    description: "Discover the field schema for a data source before writing a query"
  - name: "purple_ai_alert_summary"
    description: "Get a Purple AI-generated summary for an alert"
  - name: "s1_api_get"
    description: "Generic GET against the SentinelOne Management Console REST API"
  - name: "s1_api_post"
    description: "Generic POST against the SentinelOne Management Console REST API"
  - name: "s1_api_put"
    description: "Generic PUT against the SentinelOne Management Console REST API"
  - name: "s1_api_patch"
    description: "Generic PATCH against the SentinelOne Management Console REST API"
  - name: "s1_api_delete"
    description: "Generic DELETE against the SentinelOne Management Console REST API"
  - name: "uam_add_note"
    description: "Add an analyst note to a UAM alert"
  - name: "uam_get_alert"
    description: "Get full details for a UAM alert"
  - name: "uam_list_alerts"
    description: "List UAM alerts with filtering"
  - name: "uam_set_status"
    description: "Set the status of a UAM alert"
  - name: "sdl_get_file"
    description: "Get a Singularity Data Lake configuration file (parser, dashboard, or lookup)"
  - name: "sdl_list_files"
    description: "List Singularity Data Lake configuration files"
  - name: "sdl_put_file"
    description: "Create or update a Singularity Data Lake configuration file"
  - name: "sdl_delete_file"
    description: "Delete a Singularity Data Lake configuration file"
  - name: "hec_ingest"
    description: "Ingest events into the Singularity Data Lake via HEC"
  - name: "ha_list_workflows"
    description: "List Hyperautomation workflows"
  - name: "ha_get_workflow"
    description: "Get a Hyperautomation workflow's definition"
  - name: "ha_import_workflow"
    description: "Import and deploy a Hyperautomation workflow from JSON"
  - name: "ha_export_workflow"
    description: "Export a Hyperautomation workflow as JSON"
  - name: "ha_delete_workflow"
    description: "Delete a Hyperautomation workflow"
  - name: "uam_ingest_alert"
    description: "Ingest a UAM alert via the HEC alert interface"
  - name: "uam_post_alert"
    description: "Post a UAM alert directly to the Alert Interface"
  - name: "uam_post_indicators"
    description: "Post IOC indicators to a UAM alert"
resources_exposed:
  - name: "sentinelone://soc-context"
    description: "Serves CLAUDE.md, the Principal SOC Analyst operating instructions"
  - name: "sentinelone://credentials-status"
    description: "Reports which credentials are configured and which API surfaces are available"
prompts_exposed:
  - name: "soc_analyst"
    description: "Embeds CLAUDE.md as a system prompt; call at session start"
  - name: "session_init"
    description: "Structured session init: enumerate data sources and triage open alerts in parallel"
---

SentinelOne MCP Server (`s1-secops-mcp`) is a pure Node.js 18+, zero-external-dependency MCP server that orchestrates the SentinelOne Management Console REST API, Singularity Data Lake (SDL), UAM Alert Interface, and Hyperautomation APIs behind a single MCP surface. It's the primary API-access layer for the broader "SentinelOne AI Analyst" skills bundle in this repository, but it also works standalone with any MCP client.

## What it does

- **PowerQuery access** — enumerate data sources, run PowerQuery analytics, and discover field schemas against the Singularity Data Lake.
- **Management Console REST** — generic GET/POST/PUT/PATCH/DELETE verbs against the S1 Mgmt Console API, plus Purple AI alert summaries.
- **UAM alert management** — list, get, note, and set status on UAM alerts; ingest alerts and IOC indicators via HEC.
- **SDL configuration management** — list, get, create/update, and delete SDL config files (parsers, dashboards, lookups).
- **Hyperautomation** — list, get, import/deploy, export, and delete Hyperautomation workflows.
- **Two resources and two prompts** for session bootstrapping: a `soc_analyst` system prompt that loads `CLAUDE.md`, and a `session_init` prompt that enumerates data sources and triages open alerts in parallel.

## How it works

The server supports both `stdio` (for Claude Desktop, Claude Code, and Claude Cowork, launched via `npx`) and Streamable HTTP transports (for shared team deployments on a VM, with per-user bearer tokens, SIGHUP-reloadable token rotation, and structured audit logging). It authenticates to the SentinelOne Management Console via an API token (`S1_CONSOLE_API_TOKEN`) and, for SDL and HEC operations, additional SDL-scoped keys (`SDL_LOG_READ_KEY`, `SDL_CONFIG_READ_KEY`, `SDL_CONFIG_WRITE_KEY`, `S1_HEC_INGEST_URL`). Credentials resolve from environment variables, an explicit credentials file, or several Cowork/CLI-friendly fallback paths, in a documented priority order. In HTTP mode, per-user bearer tokens are optional but strongly recommended outside `127.0.0.1`; the server logs a warning if it starts without one.
