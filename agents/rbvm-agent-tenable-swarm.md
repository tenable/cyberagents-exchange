---
name: "RBVM Agent"
author: "Team Triple R (Rennier Mazuco, Rafael Codeceira and Rebeca Ribeiro)"
github_url: "https://github.com/SadyBeca/RBVM-Agent_TenableSWARM"
description: "Claude-based RBVM agent: groups Tenable findings by policy, stores them in SQLite, manages Azure DevOps cards."
license: "MIT"
tier: "contributed"
tags: ["rbvm", "vulnerability-management", "prioritization", "azure-devops", "sqlite", "hexa-ai", "claude-skills", "remediation-tracking"]
domains: ["vulnerability-management"]
integrations: ["Tenable", "Tenable Hexa AI MCP", "Azure", "Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T15:48:00Z
works_with_tenable_hexa_mcp: true
---

A Risk-Based Vulnerability Management (RBVM) agent that runs the vulnerability management lifecycle with Claude, four `[VM]` skills and three MCP servers. It collects prioritized findings from Tenable, groups them into actionable cards per team, tracks them in a local SQLite database, opens and closes Azure DevOps work items, and reports progress on an HTML dashboard. The code, skills and setup guide live in the GitHub repository.

## What it does

- **Policy-based grouping:** uses Hexa AI in Tenable Vulnerability Management to list the most important findings from company-defined queries, then groups findings that share a remediation and a `CORE_TEAM` tag into one card, with severity, remediation deadline and suggested compensating controls.
- **Local persistence:** saves each grouping to a SQLite database (one table per policy query) and deduplicates on `FindingID`, so later runs only add new groupings.
- **Azure DevOps sync:** creates *Vulnerability* work items for new records and, for existing ones, reactivates, replaces or closes cards using a documented decision tree.
- **Analytics dashboard:** builds an HTML dashboard from Azure DevOps Analytics (OData) and the database, with trends, KPIs, breakdowns by team and severity, and a searchable table.

## How it works

Four Claude skills run in sequence (grouping, save to database, Azure DevOps orchestration, dashboard). They talk to the Tenable MCP server (with Hexa AI), a local SQLite MCP server included in the repo, and the Azure DevOps MCP server. Company-specific policy lives in editable context files (queries, severity map, SLAs, mitigations, team map), so behaviour changes without editing the skills. All outbound data flows are documented in the repository README.
