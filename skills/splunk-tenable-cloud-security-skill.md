---
last_reviewed: 2026-08-17
name: "Splunk Tenable Cloud Security Skill"
author: "rrossetti-splunk"
github_url: "https://github.com/rrossetti-splunk/splunk-tenable-cloud-security-skill"
description: "Query and triage Tenable Cloud Security posture findings in Splunk via the official Splunk MCP Server."
license: "Apache-2.0"
tier: "contributed"
tags: ["splunk", "tenable", "cloud-security", "posture", "spl", "mcp"]
integrations: ["Splunk", "Tenable"]
date_added: 2026-08-17
contribution_agreement_date: 2026-08-17T20:30:29Z
compatible_platforms: ["Claude Code", "Claude Desktop", "Cursor", "Codex", "GitHub Copilot"]
invocation: "/splunk-tenable-cloud-security"
---

Query and triage **Tenable Cloud Security posture findings** already ingested in Splunk using production-safe, count-first SPL via the official Splunk MCP Server.

## What it does

- Provides three workflows for finding inventory, cluster/workload triage, and Tenable policy/account exposure
- Enforces count-first SPL guardrails with explicit time bounds and read-only defaults
- Parses `resources{}{}` fields and rolls up findings by cluster, workload, account, and policy
- Routes through Splunk MCP discovery tools with a documented CLI fallback when MCP is unavailable

## How it works

The skill packages routing logic in `SKILL.md` with progressive disclosure into `references/` and `workflows/`. The agent discovers your Splunk environment via MCP, validates Tenable posture field mappings, runs bounded SPL queries, and returns structured triage output. It integrates with upstream Splunk Agent Skills for SPL optimization and CLI fallback without forking their content.
