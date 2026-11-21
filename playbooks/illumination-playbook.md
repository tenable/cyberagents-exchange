---
playbook_type: "standard"
name: "Illumination Playbook"
author: "smjennings"
github_url: "https://github.com/smjennings/illumination-playbook"
description: "Correlates Tenable VM and Tenable One exposure data with actively exploited CVEs into an evidence-backed weekly brief."
license: "MIT"
tier: "contributed"
tags: ["exposure-management", "cisa-kev", "exploit-intelligence", "vulnerability-prioritization", "identity-security", "claude-code"]
domains: ["vulnerability-management", "threat-intelligence"]
integrations: ["Tenable", "Tenable Hexa AI MCP", "Anthropic"]
agents_used:
  - name: "Illumination Collector"
    role: "Pulls the baseline Tenable VM and Tenable One dataset (hosts, accounts, identities, AI agents, identity findings) through read-only Tenable Hexa MCP calls and normalizes it to JSON"
    type: "github"
    ref: "https://github.com/smjennings/illumination-playbook/blob/main/.claude/agents/illumination-collector.md"
  - name: "Illumination Threat Scout"
    role: "Builds a watchlist of trending exploited vulnerabilities from Tenable Vulnerability Intelligence, CISA KEV additions and public reporting, with a finding regex per threat"
    type: "github"
    ref: "https://github.com/smjennings/illumination-playbook/blob/main/.claude/agents/illumination-threat-scout.md"
  - name: "Illumination Correlator"
    role: "Joins exposure data with the watchlist, runs a deterministic pattern miner, and writes ranked insights backed by record counts"
    type: "github"
    ref: "https://github.com/smjennings/illumination-playbook/blob/main/.claude/agents/illumination-correlator.md"
  - name: "Illumination Briefer"
    role: "Turns the correlations and insights into an HTML exposure brief and a 72-hour action list"
    type: "github"
    ref: "https://github.com/smjennings/illumination-playbook/blob/main/.claude/agents/illumination-briefer.md"
  - name: "Analyst Review"
    role: "Human checkpoint: a security analyst reviews the brief, its stated data gaps and sanity checks before it is shared"
    type: "info"
date_added: 2026-11-20
contribution_agreement_date: 2026-11-21T01:53:59Z
works_with_tenable_hexa_mcp: true
---

Illumination answers one question every week: **which vulnerabilities attackers are actively exploiting right now are present in our environment, and what patterns in our Tenable data make them worse?** It is a Claude Code playbook you run with a single `/illumination-run` command. Every claim in the brief it produces traces back to a record count.

## What it does

- **Collision map:** matches trending threats (CISA KEV additions, Tenable Vulnerability Intelligence trending and in-the-news CVEs, named campaigns) against open findings and installed software, host by host.
- **Patterns a single dashboard misses:** hosts under several live campaigns at once, fixes that rolled back (FIXED then RESURFACED), identity vs software resurfacing rates, golden-image suspects, control-plane hosts in the top 25, and scanner or management accounts among the riskiest identities.
- **Visibility gaps:** zero-finding hosts, unknown operating systems, unscored AI agents, and watchlist products that are present but have no version check.
- **Output:** a ranked HTML brief with an evidence strip for each insight, a 72-hour action list ordered by KEV due date, structural fixes, and a Method and limits section that lists every data cap and failed pull.

## How it works

Four Claude Code subagents, orchestrated by the `/illumination-run` skill. The first two run in parallel:

1. **Collector** pages Tenable VM and Tenable One through read-only Tenable Hexa MCP calls and normalizes the results with `scripts/parse_tenable.py`.
2. **Threat Scout** queries Tenable Vulnerability Intelligence and the public web, then writes `watchlist.json`. It is the only stage with web access, and its queries contain CVE and product names, never environment data.
3. **Correlator** pulls product-specific findings for each threat, runs the pattern miner `scripts/correlate.py`, and adds judgment-based findings such as cross-domain attack chains, partial upgrades and role-implied criticality.
4. **Briefer** renders the brief from a house HTML template.

Each run lives in its own `runs/YYYY-MM-DD/` folder, so later runs can diff week over week. It needs Claude Code, the Tenable Hexa MCP server and web search. The scripts use the Python standard library only. Outbound data flows are documented in the repository README.
