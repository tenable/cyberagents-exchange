---
name: "Tenable SC AI Analyst"
author: "ayuksel-tenb"
github_url: "https://github.com/ayuksel-tenb/tenablesc-ai-analyst"
description: "An MCP server that turns Tenable Security Center into a conversational vulnerability analyst — query exposure, top risks, remediation, hosts, plugins and feed health in plain language."
license: "MIT"
tier: "contributed"
tags: ["tenable", "security-center", "vulnerability-management", "vulnerability-analysis", "mcp"]
integrations: ["Tenable"]
date_added: 2026-06-18
transport: "stdio"
runtime: "python"
auth_method: "api-key"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor", "Windsurf", "VS Code Copilot"]
tools_exposed:
  - name: "sc_list_vulnerabilities"
    description: "List vulnerability findings (listvuln, or vulndetails for full detail)."
  - name: "sc_vuln_summary_by_host"
    description: "Vulnerability counts grouped by host/IP (sumip)."
  - name: "sc_vuln_summary_by_plugin"
    description: "Vulnerability counts grouped by plugin (sumid)."
  - name: "sc_vuln_summary_by_severity"
    description: "Vulnerability counts grouped by severity (sumseverity)."
  - name: "sc_vuln_summary_by_cve"
    description: "Vulnerability counts grouped by CVE (sumcve)."
  - name: "sc_remediation_summary"
    description: "Remediation rollup — the fixes that clear the most risk (sumremediation)."
  - name: "sc_vuln_trend"
    description: "Vulnerability trend over time (trend)."
  - name: "sc_analysis_query"
    description: "Escape hatch: run an arbitrary /rest/analysis query (raw type/tool/filters)."
  - name: "sc_list_assets"
    description: "List asset lists/groups."
  - name: "sc_get_asset"
    description: "Get one asset list by ID."
  - name: "sc_list_repositories"
    description: "List repositories."
  - name: "sc_list_solutions"
    description: "List solutions via the remediation analysis."
  - name: "sc_get_solution"
    description: "Get the remediation/solution text for a plugin."
  - name: "sc_search_plugins"
    description: "Search the plugin catalog by name keyword."
  - name: "sc_get_plugin"
    description: "Get full detail for one plugin."
  - name: "sc_list_queries"
    description: "List saved queries."
  - name: "sc_run_query"
    description: "Run a saved query by ID."
  - name: "sc_list_scan_results"
    description: "List scan results."
  - name: "sc_get_scan_result"
    description: "Get one scan result by ID."
  - name: "sc_feed_status"
    description: "Report plugin/feed freshness — when each feed was last updated."
  - name: "sc_list_scanners"
    description: "List Nessus scanners and their status."
  - name: "sc_create_accept_risk_rule"
    description: "Write (gated by SC_ENABLE_WRITES): create an Accept Risk rule. Persistent change."
  - name: "sc_create_recast_risk_rule"
    description: "Write (gated by SC_ENABLE_WRITES): create a Recast Risk rule. Persistent change."
  - name: "sc_create_ticket"
    description: "Write (gated by SC_ENABLE_WRITES): create a remediation ticket. Persistent change."
  - name: "sc_launch_scan"
    description: "Write (gated by SC_ENABLE_WRITES): launch a scan. Persistent change."
resources_exposed: []
prompts_exposed: []
---

Connect an AI assistant (Claude Code, OpenCode, or any MCP client) directly to **Tenable Security Center (Tenable.sc)** and investigate your exposure in plain language — the agent calls the right Security Center analysis and answers from live data, no clicking through the console.

## What it does

- Answers natural-language questions via the right `/rest/analysis` query: severity / host / plugin / CVE / remediation summaries, vulnerability trends, or a raw analysis query.
- Surfaces context on demand: assets, repositories, solutions, plugins, saved queries, scan results, scanners, and plugin-feed freshness.
- Authenticates with API keys via the `x-apikey` header (read from the environment) — no session token is ever created.
- Keeps side-effecting actions (accept/recast risk rules, tickets, launch scan) **off by default** behind an explicit `SC_ENABLE_WRITES` flag, each clearly marked as a persistent change.
- Never touches Token / SAML / LDAP / User / Role / Director endpoints.

## How it works

Built on the official MCP SDK's FastMCP (Python 3.12), the server wraps the Tenable.sc REST API — primarily `/rest/analysis` — behind a small set of read-focused tools that share one reusable filter set (severity, plugin, IP, repository, last-seen, exploit-available, CVE) with offset pagination. A single async HTTP client handles auth and error handling for every request. Read tools are always available; the isolated write tools are registered only when writes are explicitly enabled.
