---
name: "Tenable + SentinelOne Attack Path Interruption"
author: "jdelong-tenb"
github_url: "https://github.com/jdelong-tenb/tenable-sentinelone-attack-path-interruption"
description: "Cross-references a live Tenable One Attack Path Analysis toxic path against SentinelOne's real-time alert stream, and — with explicit confirmation — triggers SentinelOne network isolation on a path host showing active lateral-movement behavior."
license: "MIT"
tier: "contributed"
tags: ["sentinelone", "attack-path-analysis", "edr", "lateral-movement", "containment"]
integrations: ["Tenable", "Tenable Hexa AI MCP", "SentinelOne"]
date_added: 2026-09-02
contribution_agreement_date: 2026-09-02T00:00:00Z
compatible_platforms: ["Claude Code"]
invocation: "Say things like \"is anything actually happening on this attack path right now,\" \"check SentinelOne for activity on these exposed hosts,\" or \"isolate this host, it's on a toxic path\" — the skill activates automatically."
last_reviewed: 2026-09-02
works_with_tenable_hexa_mcp: true
---

## What it does

Tenable One's Attack Path Analysis (APA) maps toxic combinations an attacker could walk across the environment; SentinelOne's EDR sees attacker behavior live but has no path context. This skill overlays the two: it pulls a toxic path, checks each hop for active SentinelOne alerts (and deeper telemetry correlation via PowerQuery when alert-level data isn't enough), and — only with explicit user confirmation — isolates a specific host via SentinelOne's Management Console API.

This is a community-built skill, not official guidance from Tenable or SentinelOne.

**Scope:** attack-path-aware alert triage and confirmed manual containment. It does not auto-isolate, and it does not build attack paths itself — it requires Tenable's APA domain to already be enabled.

## How it works

Install with Tenable's Hexa MCP (APA domain enabled) and SentinelOne's public `purple-mcp` both connected. When invoked, it:

1. Retrieves a toxic path's node list from the Hexa MCP APA-domain tool.
2. For each path host, resolves it to a SentinelOne asset (`search_inventory_items`) and checks for active alerts (`search_alerts`), then optionally runs a `purple_ai()`-generated PowerQuery for deeper cross-hop telemetry correlation.
3. States the combined risk explicitly — path position plus live SentinelOne activity — rather than reporting either signal alone.
4. Only after naming the host and getting explicit confirmation, calls SentinelOne's Management Console REST API directly to isolate it (`purple-mcp` is read-only and has no write tools), then verifies the isolation actually took effect.

`scripts/isolate_agent.py` is the containment call used in step 4 — see the repo's Known Limitations: the exact endpoint has not been called live in building this skill, and should be confirmed against SentinelOne's current API reference before real use. (SentinelOne's own [`s1-secops-mcp`](https://github.com/Sentinel-One/ai-siem/tree/main/mcp/s1-secops-mcp) server exposes a more robust write-capable alternative for environments that have it configured, but this skill does not integrate with it.)
