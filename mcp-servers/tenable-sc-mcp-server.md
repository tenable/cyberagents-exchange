---
name: "Tenable.sc MCP Server"
author: "Ahmad Jaber (ABMJ)"
github_url: "https://github.com/ABMJ/tenable-sc-mcp-server"
description: "Production MCP bridge to Tenable Security Center with intelligent tools for vulnerability management and asset discovery"
license: "GPL-3.0-only"
tier: "unreviewed"
tags: ["security", "vulnerability-management", "tenable", "security-center", "vulnerability-scanning", "t.sc", "t.sc+", "tenable-security-center-plus-mcp"]
integrations: ["Tenable"]
date_added: 2026-06-19
transport: "both"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Desktop", "Claude Code"]
tools_exposed:
  - name: "tsc_catalog"
    description: "Browse 100+ available Tenable.sc resources"
  - name: "tsc_current_user"
    description: "Verify API user identity and permissions"
  - name: "tsc_resource_action"
    description: "Unified CRUD interface (list, get, create, update, delete)"
  - name: "tsc_request"
    description: "Direct access to any Tenable.sc endpoint"
  - name: "tsc_analyze"
    description: "Run analysis queries with caching"
  - name: "tsc_download"
    description: "Binary/text download helper"
  - name: "tsc_upload_file"
    description: "Multipart file upload helper"
  - name: "tsc_cache_stats"
    description: "View cache performance metrics"
  - name: "tsc_cache_clear"
    description: "Clear cache entries by pattern"
  - name: "tsc_profile_ip_efficient"
    description: "Complete security profile for single IP"
  - name: "tsc_list_vulns_by_ip_summary"
    description: "Quick vulnerability counts by severity"
  - name: "tsc_list_vulns_by_ip_full"
    description: "Complete vulnerability records with metadata"
  - name: "tsc_list_ips"
    description: "List all IPs with filtering"
  - name: "tsc_list_vulns_by_cve"
    description: "Search for CVE across infrastructure"
  - name: "tsc_resource_docs"
    description: "Returns docs metadata for Tenable.sc resource"
resources_exposed:
  - name: "tenable-sc://catalog"
    description: "Human-readable API catalog"
  - name: "tenable-sc://filters/format-reference"
    description: "Comprehensive filter format guide"
  - name: "tenable-sc://filters/reference"
    description: "Auto-generated filter reference"
prompts_exposed: []
---

The Tenable.sc MCP Server provides AI assistants with direct access to Tenable Security Center's comprehensive vulnerability management platform. It exposes 100+ Tenable.sc API resources through a production-ready Model Context Protocol interface.

## What it does

This MCP server enables AI-powered security workflows by providing:
- **Comprehensive vulnerability queries** - Search CVEs across your infrastructure, list vulnerabilities by IP/severity, and get detailed remediation guidance
- **Asset profiling and discovery** - Profile individual IPs with complete security context, discover assets by criticality, and map asset group membership
- **Intelligent caching** - Built-in Redis/in-memory caching reduces API load and enables 1000x faster repeated queries
- **Generic resource access** - Direct CRUD operations on all Tenable.sc resources (scans, policies, credentials, users, reports)
- **Analysis engine** - Run complex analysis queries with 55+ filters (VPR score, asset criticality, exploit availability, CVSS)

## How it works

The server acts as a stateless proxy between MCP clients and Tenable.sc's REST API. It authenticates using your Tenable.sc API keys and enforces all RBAC permissions from your Security Center instance. The architecture includes:
- Multi-tier caching (in-memory + Redis) with smart TTLs based on data volatility
- 15 core MCP tools including convenience tools for common security workflows
- 3 self-documenting resources with filter format references for complex queries
- Docker Compose deployment with Redis included for production use
- Support for both stdio (Claude Desktop) and HTTP (remote clients) transports

Built with Python 3.11+ and the official MCP SDK.
