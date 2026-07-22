---
name: "PCI ASV Scan Readiness MCP Server"
author: "amcdonnell-dot"
github_url: "https://github.com/amcdonnell-dot/pci-asv-readiness-mcp"
description: "An MCP (Model Context Protocol) server that connects AI assistants to the Tenable Vulnerability Management API to assess how set-up-for-success a PCI Quarterly External scan is before the ASV attestation workflow — with deterministic finding filtering, an advisory readiness score, and dispute-preparation worksheets."
license: "MIT"
tier: "contributed"
tags: ["pci", "asv", "compliance"]
integrations: ["Tenable"]
date_added: 2026-07-22
contribution_agreement_date: 2026-07-22T15:00:00Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop"]
transport: "stdio"
runtime: "python"
auth_method: "api-key"
tools_exposed:
  - name: "tool_name"
    description: "What this tool does"
resources_exposed: []
prompts_exposed: []
---

Optional longer description of your MCP server.

## What it does

Describe the data sources or actions your server exposes.

## How it works

Brief overview of the approach — what APIs it wraps, how it transforms data, etc.
