---
name: "Tenable Identity Exposure MCP Server"
author: "knethteo"
github_url: "https://github.com/knethteo/tenable-identity-exposure-mcp"
description: "MCP server exposing the Tenable Identity Exposure (TIE) API as tools for LLM clients."
license: "MIT"
tier: "contributed"
tags: ["tenable", "identity-exposure", "active-directory", "ioe", "ioa", "security"]
integrations: ["Tenable"]
date_added: 2026-07-08
transport: "both"
runtime: "python"
auth_method: "api-key"
compatible_clients: ["Claude Desktop", "Claude Code"]
tools_exposed:
  - name: "tie_catalog"
    description: "List available resources (flat + nested) — call this first."
  - name: "tie_request"
    description: "Raw HTTP call to any endpoint (method, path, params, body)."
  - name: "tie_resource_action"
    description: "Generic CRUD (list/get/create/update/delete) on flat resources."
  - name: "tie_recent_activity"
    description: "Unified IoE+IoA timeline for the last N hours in one call."
  - name: "tie_profiles"
    description: "List security profiles (IoE/IoA data is profile-scoped)."
  - name: "tie_scores"
    description: "Per-directory security scores for a profile."
  - name: "tie_topology"
    description: "AD topology (domains, forests, trusts) for a profile."
  - name: "tie_attacks"
    description: "IoA attack instances (requires resource_type + resource_value)."
  - name: "tie_alerts"
    description: "Alerts for a profile."
  - name: "tie_deviances"
    description: "IoE deviant AD objects for a checker within a time window."
  - name: "tie_deviances_by_checker"
    description: "Full IoE deviances for a checker (no date filter)."
  - name: "tie_deviances_by_directory"
    description: "Full IoE deviances for a directory (no date filter)."
  - name: "tie_search_events"
    description: "Search AD security events in a date range."
  - name: "tie_search_ad_objects"
    description: "Search AD objects (users/computers/groups/OUs)."
  - name: "tie_whoami"
    description: "Current user identity, roles, and permissions."
resources_exposed: []
prompts_exposed: []
---

An [MCP](https://modelcontextprotocol.io) server exposing the **Tenable Identity Exposure** (TIE, formerly Tenable.ad) REST API as tools for LLM clients. Built on `FastMCP` from the official `mcp` SDK and verified end-to-end against a live TIE SaaS instance.

> This is not an officially supported Tenable project. Validate responses against the Tenable console before acting on them.

## What it does

Turns the Tenable Identity Exposure API into 15 LLM-callable tools spanning both Indicators of Exposure (IoE) and Indicators of Attack (IoA). Highlights:

- **Unified activity timeline** — `tie_recent_activity` merges IoE deviances and IoA attacks for the last N hours in a single call.
- **Security posture** — list security profiles, per-directory security scores, and AD topology (domains, forests, trusts).
- **Deviance investigation** — pull IoE deviances by time window, checker, or directory, with rendered descriptions and slimmed payloads to conserve token budget.
- **AD search** — query AD objects (users, computers, groups, OUs) and security events over a date range.
- **Escape hatches** — `tie_catalog` for resource discovery, `tie_request` for raw calls to any endpoint, and `tie_resource_action` for generic CRUD.

## How it works

The server wraps the TIE REST API and authenticates with the `X-API-Key` header (`TIE_URL` / `TIE_API_KEY` via environment or CLI flags). It runs over stdio for Claude Desktop / Claude Code, or as an SSE/HTTP network service. Time-aware tools accept a relative `hours=N` window or explicit UTC `date_start`/`date_end`. IoE/IoA data is profile-scoped, so tools take an explicit `profile_id`. By default, deviance and object results are slimmed (descriptions rendered from templates, oversized attribute values dropped); pass `verbose=true` for the full raw payload.
