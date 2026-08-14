---
name: "Tenable VPR MCP"
author: "Sabastiaz"
github_url: "https://github.com/Sabastiaz/tenable-vpr-mcp"
description: "Read-only Tenable.io / Tenable One MCP server with a VPR re-prioritization comparison tool, CISA KEV / EPSS exploitation cross-check, and pentest re-test scan-delta reporting."
license: "MIT"
tier: "contributed"
tags: ["vulnerability-management", "vpr", "pentest", "exposure-management", "kev", "epss"]
integrations: ["Tenable"]
date_added: 2026-08-03
contribution_agreement_date: 2026-08-03T06:30:08Z
last_reviewed: 2026-08-04
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop"]
transport: "stdio"
runtime: "python"
auth_method: "api-key"
tools_exposed:
  - name: "list_scans"
    description: "List scans visible to the authenticated API key, optionally filtered by folder ID."
  - name: "get_scan_details"
    description: "Latest results for a single scan: hosts scanned, per-plugin findings, severity counts."
  - name: "list_assets"
    description: "List assets known to the tenant (hostname, IPs, UUID, last seen, sources)."
  - name: "get_asset_details"
    description: "Full detail for a single asset by UUID, including tags and exposure scores if licensed."
  - name: "search_vulnerabilities"
    description: "Search current findings via the vulnerability workbench, filterable by severity and plugin family."
  - name: "get_plugin_details"
    description: "Full plugin detail: description, solution, CVSS vectors, CVEs, and VPR drivers."
  - name: "list_tags"
    description: "List asset tag categories and values configured in the tenant."
  - name: "list_agents"
    description: "List Nessus Agents with status, platform, and last connect / last scanned timestamps."
  - name: "compare_vpr_reprioritization"
    description: "Before/after comparison of CVSS-based severity vs. VPR-based severity per finding, flagged as escalated / downgraded / unchanged / unrated."
  - name: "check_kev_epss_exposure"
    description: "Cross-references findings' CVEs against the CISA KEV catalog and FIRST.org EPSS scores, independent of Tenable's proprietary VPR."
  - name: "scan_delta"
    description: "Compares a baseline scan against a re-test scan by plugin ID: fixed, still_open, and new_since_baseline, with a remediation-rate percentage."
resources_exposed: []
prompts_exposed: []
---

## What it does

> See which findings VPR actually escalates — and back it with CISA KEV,
> not vendor trust.

Tenable VPR MCP exposes read-only Tenable.io / Tenable One vulnerability
management data (scans, assets, findings, plugins, tags, agents) as MCP
tools, plus three tools built specifically for exposure-management and
pentest reporting workflows rather than raw API access:

- **`compare_vpr_reprioritization`** builds a before/after table showing
  how VPR re-ranks findings against their static CVSS severity, flagging
  escalations and downgrades. This is the exact comparison used in
  Tenable One CTEM proof-of-concept deliverables, where a client needs to
  see concretely what VPR changes about their existing scan data.
- **`check_kev_epss_exposure`** backs that re-prioritization with two
  independent, publicly sourced signals instead of relying on a single
  vendor score: CISA's Known Exploited Vulnerabilities catalog and
  FIRST.org's Exploit Prediction Scoring System.
- **`scan_delta`** compares a baseline scan to a re-test scan and buckets
  findings into fixed / still-open / new, with a remediation-rate
  percentage, for the re-test report every pentest engagement produces.

## How it works

Built on [pyTenable](https://pytenable.readthedocs.io/) for the Tenable.io
API and [FastMCP](https://gofastmcp.com/) for the MCP server layer. CVE
cross-referencing pulls live data from CISA's public KEV JSON feed and the
FIRST.org EPSS API; both calls are isolated from the comparison logic so
the re-prioritization and delta-building functions are independently unit
tested without live network access. The server is read-only: no scan
launch, edit, or delete operations are exposed, so it's safe to point at a
production Tenable.io / Tenable One tenant.

Authentication is via `TIO_ACCESS_KEY` / `TIO_SECRET_KEY` environment
variables only (never CLI arguments), generated in Tenable.io / Tenable
One under Settings > My Account > API Keys.

## Known limitations

- `check_kev_epss_exposure` issues one additional Tenable API call per
  distinct plugin to resolve CVEs, so `limit` should stay modest for
  interactive use.
- `search_vulnerabilities` and `compare_vpr_reprioritization` read from
  the vulnerability workbench (tenant-wide, not scan-scoped); use
  `get_scan_details` / `scan_delta` for scan-specific views.
- No write operations (scan launch/configure, tag assignment, asset
  deletion) are implemented by design.
