---
name: "MITRE APT Attack Path Analysis"
author: "JHall-19"
github_url: "https://github.com/JHall-19/rf-tenable-attack-path-prioritization"
description: "Pulls your Recorded Future threat map, maps an APT group's MITRE ATT&CK techniques, and cross-references against live Tenable findings to identify which attack path nodes are actively exploitable."
license: "MIT"
tier: "contributed"
tags:
  - attack-path
  - mitre-attack
  - threat-intelligence
  - vulnerability-management
  - apt
  - recorded-future
  - adversary-emulation
integrations:
  - Tenable
  - Tenable Hexa AI MCP
  - Recorded Future
date_added: 2026-07-22
contribution_agreement_date: 2026-07-22T16:11:37Z
works_with_tenable_hexa_mcp: true
compatible_platforms:
  - Claude Code
invocation: "/mitre-apt-attack-path"
---

A Claude Code skill that bridges Recorded Future threat intelligence with Tenable vulnerability data to produce MITRE ATT&CK-grounded attack path analyses. The analyst selects an adversary from their live RF threat map, and the skill maps the actor's confirmed MITRE techniques against active Tenable findings to determine which steps of the attack path are exploitable today.

## What it does

- Pulls the analyst's live Recorded Future threat map and presents ranked adversaries for selection — no actor name required upfront
- Maps the selected APT group's MITRE ATT&CK techniques using RF entity links as the authoritative source
- Cross-references each technique node against live Tenable One findings, labeling each as `ACTIVE`, `PARTIAL`, `NOT DETECTED`, or `NOT APPLICABLE`
- Identifies the critical path — the shortest confirmed-exploitable sequence from initial access to impact
- Produces a formal attack path analysis table, visual node diagram, and recommended Tenable actions per technique
- Supports optional export as `.md` or CSV

## How it works

The skill runs in three phases: first it calls the RF threat map API to surface ranked threat actors and waits for analyst selection; then it retrieves the actor's MitreAttackIdentifier links from RF and fetches Insikt intelligence notes for enrichment; finally it queries Tenable One for each technique to determine live exploitability and assembles the output. All three data sources are required — RF MCP for threat actor intelligence, and Tenable Hexa AI MCP for live vulnerability cross-reference.
