---
name: "Tenable + SentinelOne Asset Reconciliation"
author: "jdelong-tenb"
github_url: "https://github.com/jdelong-tenb/tenable-sentinelone-asset-reconciliation"
description: "Cross-references Tenable's asset inventory against SentinelOne's agent inventory to find protection gaps and exposure blind spots — matches on hostname/IP, classifies each host, and can tag unprotected assets in Tenable for follow-up."
license: "MIT"
tier: "contributed"
tags: ["sentinelone", "asset-inventory", "exposure-management", "edr", "coverage-gap"]
integrations: ["Tenable", "SentinelOne"]
date_added: 2026-09-02
contribution_agreement_date: 2026-09-02T00:00:00Z
compatible_platforms: ["Claude Code"]
invocation: "Say things like \"find gaps between our Tenable and SentinelOne coverage,\" \"what's on the network that SentinelOne isn't protecting,\" or \"which SentinelOne-protected assets does Tenable never scan\" — the skill activates automatically."
last_reviewed: 2026-09-02
---

## What it does

Tenable and SentinelOne each independently track "everything on the network" — one from vulnerability/exposure scanning, one from EDR agent telemetry — and nothing automatically checks whether the two agree. This skill pulls both inventories and reconciles them to find Tenable-visible hosts with no SentinelOne agent (protection gaps) and SentinelOne-protected hosts Tenable never scans (exposure blind spots).

This is a community-built skill, not official guidance from Tenable or SentinelOne.

**Scope:** asset-inventory reconciliation only. Does not deploy agents, launch scans, or modify SentinelOne policy.

## How it works

Install the skill with both a Tenable MCP server and SentinelOne's public `purple-mcp` server connected. When invoked, it:

1. Pulls Tenable assets (`workbenches_list_assets` or `tenable_one_search_assets`) and SentinelOne inventory (`list_inventory_items` / `search_inventory_items`, filterable by surface: endpoint, cloud, identity, network-discovery).
2. Matches hosts across vendors on hostname and IP — SentinelOne records have no single canonical hostname or MAC field, so the match key is built from `name`, `ipAddress`, and nested `networkInterfaces[].ip`.
3. Classifies each host as matched, Tenable-only, SentinelOne-only, or ambiguous (IP-only match, no hostname confirmation) — ambiguous matches are flagged, not silently promoted.
4. Reports counts and a host-level table, and — only with confirmation — can tag unprotected hosts in Tenable for remediation tracking.

Includes a utility script (`scripts/match_inventories.py`) that runs the matching logic standalone against exported inventory JSON.
