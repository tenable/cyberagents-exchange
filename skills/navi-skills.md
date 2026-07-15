---
name: "navi-skills"
author: "packetchaos"
github_url: "https://github.com/packetchaos/navi-claude-skills"
description: "A 13-skill Claude skill set for driving the Tenable navi CLI and the navi_* MCP tools."
license: "MIT"
tier: "unreviewed"
tags: [tenable, navi, vulnerability-management, claude-skills, mcp, asset-tagging, exposure-management]
integrations: [Tenable, Anthropic]
date_added: 2026-07-15
compatible_platforms: [Claude Code, Claude Desktop, Claude Cowork]
invocation: "navi"
---

navi-skills is a Claude skill set for the [Tenable **navi**](https://github.com/packetchaos/navi)
CLI and the `navi_*` MCP tools. A router skill plus focused sub-skills cover setup and core
mechanics, asset tagging, data exploration, CSV export, ACR calibration, scan control,
actions, email, remote execution, WAS/DAST, and troubleshooting.

## What it does

The pack teaches an AI assistant how to operate navi correctly and safely: which selector
to use for a given tagging task, how to explore assets/findings, how to export by tag with
ACR/AES, how to calibrate criticality, and how to recover from common failure modes
(db locks, zero chunks, stale data). Write operations follow a propose-then-confirm pattern
gated behind explicit approval.

## How it works

Skill folders live at the repo root with a `.claude-plugin/plugin.json`, matching navi's
established layout. The `navi` router skill directs each request to the right domain skill
(navi-core, navi-enrich, navi-explore, navi-export, navi-acr, navi-scan, navi-action,
navi-was, navi-troubleshooting, navi-mcp). Load it alongside the navi CLI (or the navi-mcp
server) so the assistant has both the domain knowledge and the tool mechanics.
