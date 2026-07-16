---
name: "SentinelOne AI Analyst: Claude Skills"
author: "Sentinel-One"
github_url: "https://github.com/Sentinel-One/ai-siem/tree/main/plugins/s1-secops-skills"
description: "A full-stack AI SOC analyst for SentinelOne: seven Claude skills, three bundled MCP servers, and an operating persona (CLAUDE.md) that hunt threats, triage alerts, author detections/dashboards/parsers, and build Hyperautomation workflows from natural language."
license: "AGPL-3.0"
tier: "contributed"
contribution_agreement_date: "2026-07-16T17:02:20Z"
tags: ["sentinelone", "soc", "threat-hunting", "powerquery", "singularity-data-lake", "hyperautomation", "claude-skills"]
integrations: ["SentinelOne"]
date_added: 2026-07-09
compatible_platforms: ["Claude Code", "Claude Desktop", "Claude Cowork", "Windsurf"]
invocation: "No slash command. Install the plugin (or point Claude Code/Cowork at the CLAUDE.md persona) and describe what you want in natural language — the matching skill (mgmt-console-api, powerquery, sdl-api, sdl-dashboard, sdl-log-parser, hyperautomation, or the sdl-solutions orchestrator) is invoked automatically."
---

This bundle turns Claude into a Principal SOC Analyst for SentinelOne's Singularity Platform. `CLAUDE.md` sets the operating persona and session protocol; seven primitive `SKILL.md` skills encode confirmed API schemas and workflows for PowerQuery, dashboards, log parsers, Hyperautomation, the SDL API, and the Management Console; an `sdl-solutions` umbrella skill orchestrates the primitives for whole-solution requests (e.g., onboarding a new log source end to end). The skills reach live SentinelOne APIs through three MCP servers: `s1-secops-mcp` (bundled in this same repository — see the separate MCP server listing), `purple-mcp` (SentinelOne's Purple AI / alerts / vulnerabilities MCP), and a third-party threat-intel MCP (VirusTotal by default) for IOC enrichment.

## What it does

- **Threat hunting and investigation** — writes and runs PowerQuery from natural-language questions, summarizes findings.
- **Alert and threat management** — lists, triages, notes, and updates status on UAM alerts and threats via the Management Console.
- **Dashboard authoring** — generates deployment-ready SDL dashboard JSON from a plain-English panel description.
- **Log parser authoring** — writes and validates SDL parsers with OCSF field mapping from a pasted raw log sample.
- **Automation/response** — generates Hyperautomation workflow JSON from a natural-language playbook description.
- **Behavioral baselining and anomaly detection** — a source-agnostic pipeline (`mgmt-console-api/scripts/baseline_anomaly.py`) that builds day-of-week-stratified statistical baselines per (principal, action) on any ingested log source and surfaces spike/drop/silent/new-behavior anomalies.
- **SOC reporting** — generates structured `.docx` SOC investigation reports (executive summary, IOC table, MITRE mapping, root cause, recommendations).
- **Whole-solution deployment (`sdl-solutions`)** — onboards a raw log source end to end (OCSF parser, asset enrichment, dashboard, MITRE-mapped detections, response workflow) from one prompt.

## How it works

`CLAUDE.md`, placed at the root of a Cowork project or read automatically by Claude Code, establishes an investigation protocol (mandatory threat-intel enrichment on every IOC, cross-source correlation, MITRE ATT&CK mapping) and decides which skill to invoke for a given request. Each primitive skill is a `SKILL.md` file containing procedural knowledge — confirmed field schemas and API call patterns validated against live tenants — so Claude doesn't guess field names. Skills call out to the three MCP servers listed above, which sit outside the Cowork sandbox proxy for direct API access. Distribution is via a `.plugin` bundle (installed through Cowork → Customize → Browse plugins) or a Docker image (`ghcr.io/pmoses-s1/s1-mcps`) that bundles all three MCP servers for a no-host-runtime install path.

**Note on license:** this listing inherits the ai-siem repository's AGPL-3.0 license. AGPL's network-use clause may be a consideration for a "install and point at a customer console" skill bundle — worth reviewing against your intended distribution model before submission.
