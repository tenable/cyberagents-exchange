---
name: "Tenable MSSP Portal MCP Server"
author: "andrewspearson"
github_url: "https://github.com/andrewspearson/tenable-mcp-mssp"
description: "An MCP server for orchestrating Tenable MSSP child container workflows. Make bulk queries. Take bulk actions."
license: "MIT"
tier: "contributed"
tags: ["mssp", "vulnerability-management", "tenable-vm", "exposure-management", "tenable-one"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-06-23
works_with_tenable_hexa_mcp: true
cta: "T1"
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: ["ChatGPT", "Codex", "Claude Desktop", "Claude Code", "Antigravity"]
tools_exposed:
  - name: "list_mssp_child_accounts"
    description: "List raw MSSP child account objects returned by Tenable, including license data."
  - name: "list_available_tenable_mcp_tools"
    description: "Discover the Tenable Hexa AI MCP Server tool catalog for one child container licensed for `hexa`."
  - name: "get_child_container_scope"
    description: "Show the configured child container allowlist scope for action tools."
  - name: "run_tenable_mcp_tool_for_child"
    description: "Run one Tenable Hexa AI MCP Server tool on one child container licensed for `hexa`."
  - name: "run_tenable_mcp_recipe_for_child"
    description: "Validate a known sequence of Tenable Hexa AI MCP Server tool calls on one child container licensed for `hexa`."
  - name: "run_tenable_mcp_recipe_across_child_containers"
    description: "Run a known working recipe across multiple child containers licensed for `hexa` with controlled fan-out."
  - name: "bulk_vm_cve_query"
    description: "Start a curated direct pyTenable VM export for CVEs across eligible child containers licensed for `vm`. This tool should be used only when explicitly requested by name."
  - name: "get_bulk_vm_cve_query_status"
    description: "Check status for a server-managed `bulk_vm_cve_query` run."
  - name: "get_bulk_vm_cve_query_result"
    description: "Read final summary and artifact paths for a server-managed `bulk_vm_cve_query` run."
resources_exposed: []
prompts_exposed: []
---

## What it does

- Provides an MSSP aware wrapper around the [Tenable Hexa AI MCP Server](https://docs.tenable.com/vulnerability-management/Content/getting-started/hexa-AI-MCP.htm).
- Lets you use Tenable Hexa AI MCP Server tools across MSSP child containers through a scoped orchestration layer.
- Provides a tool, named `bulk_vm_cve_query`, to query a CVE or list of CVEs across eligible in-scope child containers. This tool provides a CSV report of findings in those child containers.
- Queries and actions taken against child containers run concurrently and operate on up to 10 child containers at a time.
- Provides the ability to limit which child containers you perform an action on. 
- Lists all child containers and license information.

## How it works

See the tenable-mcp-mssp [README](https://github.com/andrewspearson/tenable-mcp-mssp/blob/main/README.md).
