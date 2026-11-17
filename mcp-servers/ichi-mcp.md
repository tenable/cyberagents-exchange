---
name: "ICHI MCP Server"
author: "bernik-bot"
github_url: "https://github.com/bernik-bot/ichi-mcp"
description: "Query the ICHI Internet Cyber Health Index from any MCP client — current threat band, composite score, critical vulnerability alerts, and source health. No key required."
license: "MIT"
tier: "contributed"
tags: ["threat-intelligence", "cyber-health", "internet-threat-index", "vulnerability-alerts", "cisa-kev", "rss", "keyless", "read-only", "daily-barometer"]
domains: ["threat-intelligence", "security-operations"]
integrations: []
date_added: 2026-11-07
contribution_agreement_date: 2026-11-07T13:00:00Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Antigravity", "ChatGPT", "Claude Code", "Claude Desktop", "Cline", "Codex", "Continue", "Cursor", "Gemini CLI", "VS Code Copilot", "Windsurf"]
transport: "stdio"
runtime: "python"
auth_method: "none"
tools_exposed:
  - name: "get_current_index"
    description: "Get the current ICHI score (0-100), threat band (NORMAL/GUARDED/ELEVATED/HIGH/CRITICAL), per-dimension sub-scores, and freshness/impairment metadata. ICHI is an outside-in, internet-wide directional signal — not an organization-specific risk score."
  - name: "get_recent_alerts"
    description: "Get the latest N items (default 5, max 50) from ICHI's critical advisory RSS feed: title, link, published timestamp, category, and description. Covers critical CVEs, actively-exploited vulnerabilities, and significant internet-threat events."
  - name: "get_source_health"
    description: "Summarize ICHI's source health: overall status, confidence level, live/stale/failed feed counts, and which underlying sources contribute to the composite score."
resources_exposed: []
prompts_exposed: []
---

ICHI (Internet Cyber Health Index) measures the overall health of the internet's threat landscape on a 0–100 scale, updated continuously from dozens of authoritative open sources. This MCP server exposes ICHI's public API as three read-only tools — no authentication, no API key, no cost.

## What it does

The server gives any MCP-compatible AI agent direct access to three signals:

- **Current index state**: the composite 0–100 score, the five-band label (NORMAL, GUARDED, ELEVATED, HIGH, CRITICAL), per-dimension sub-scores that show which slice of the threat landscape is driving the reading, and freshness metadata so an agent can tell whether the data is live or temporarily impaired.
- **Critical advisory alerts**: the latest items from ICHI's `/api/alerts` RSS feed — CVEs designated critical by CISA KEV, actively-exploited vulnerabilities, and other significant internet-threat events, with title, link, published time, and category for each item.
- **Source health**: a live summary of which underlying feeds (vulnerability databases, threat-intel sources, internet noise monitors) are healthy, stale, or failed, and the resulting confidence level of the composite score.

## How it works

The server is a thin, stateless Python layer over three ICHI public API endpoints: `/api/current-index`, `/api/alerts` (RSS), and `/api/health`. It runs locally via `uvx --from git+https://github.com/bernik-bot/ichi-mcp ichi-mcp` (stdio transport), or inside a container using the included Dockerfile. All calls are outbound read-only HTTPS; nothing is stored between calls.

ICHI aggregates external signals from public authoritative sources — CISA KEV, NVD, internet scanning platforms, threat-feed aggregators — and normalizes them into a single outside-in directional signal. The methodology is documented at [ichi.global/methodology](https://ichi.global/methodology). The index reflects the internet threat landscape as a whole, not any organization's specific risk posture. It is designed to answer the question "is today a normal day or a high-threat day on the internet?" — a useful morning briefing signal for SOC analysts and a threat-context gate for CI/CD pipelines (see also: `bernik-bot/ichi-threat-level-action`).

## Prerequisites and limits

- Outbound HTTPS to `ichi.global` only. No authentication, no write operations, no data stored.
- Python 3.10+ or the included Dockerfile. Install via `pip install git+https://github.com/bernik-bot/ichi-mcp` then run `ichi-mcp`, or use `uvx --from git+https://github.com/bernik-bot/ichi-mcp ichi-mcp` directly (no install needed). The package is not on PyPI.
- The index is an internet-wide directional signal; it is not a vulnerability scanner, not an org-specific risk score, and not a deterministic forecast.
- Not tested against Tenable Hexa AI's MCP support; `works_with_tenable_hexa_mcp` is false.
