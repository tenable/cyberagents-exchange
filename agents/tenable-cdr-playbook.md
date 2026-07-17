---
name: "Tenable CDR Playbook"
author: "wingchurn-tenable"
github_url: "https://github.com/wingchurn-tenable/cdr-threat-story"
description: "Queries and triages Tenable Cloud Security Threat Stories into prioritized, grounded cloud IR playbooks."
license: "MIT"
tier: "contributed"
tags: [cloud-security, tenable, cdr, cspm, aispm, soc, posture, cnapp]
integrations: ["Tenable", "AWS", "Azure", "GCP"]
date_added: 2026-07-10
contribution_agreement_date: 2026-07-10T14:56:42Z
last_reviewed: 2026-07-16
---

The Tenable CDR Playbook is a security-analyst agent for Cloud Detection & Response.
It reads the live Threat Stories in Tenable Cloud Security (Risk > Threat Stories),
prioritizes them, and turns them into copy-paste-ready incident-response guidance —
without ever guessing. Every field it reports (accounts, ARNs, actor IDs, MITRE IDs,
and the engine's own summary/impact text) is quoted from the query; anything the query
does not return is shown as `<PLACEHOLDER>` so a command is never aimed at the wrong
resource.

## What it does

- **Triages the queue.** Pulls Open/InProgress Threat Stories, ranks them by severity,
  status, and real-world impact (loss of detection capability outranks data impact),
  and labels them P1…Pn.
- **Works three ways.** Interactive (answer a specific question), autonomous (sweep the
  whole queue and build the full playbook), and drill-down (keep asking follow-ups —
  pivot on actor, resource, account, or MITRE technique).
- **Produces deliverables.** A standard Markdown IR playbook (six sections per story:
  Overview, Triage, Containment, Eradication, Recovery, Prevention) or a professional
  HTML report with per-story attack-impact diagrams and a campaign-level map.
- **Read + suggest only.** It queries Tenable read-only and hands you the remediation
  commands to run yourself — it never executes changes against cloud resources.

## How it works

The agent (`threat-story-analyst`) and its bundled skill (`cdr-playbook`) are packaged
as a Claude Code / Cowork plugin. The data source is locked to the `ThreatStory` object
type in the Tenable Cloud Security Explorer (UDM), reached through the Tenable Cloud
Security (`tcs`) MCP connector — Findings, risks, and other object types are never
substituted as the source. The agent ranks the whole queue cheaply, then paces detailed
write-ups in priority blocks (a severity/status tier, or a campaign of related stories
kept together), offering the next block on request. Prevention steps are emitted as
reusable detection policies grounded in each story's specific behavior.

## Requirements

- Tenable Cloud Security with the **Cloud Detection & Response** capability (Threat
  Stories) and the Tenable Cloud Security MCP connector connected.
- Claude Code or Claude Cowork to run the agent/skill (installable from this repo as a
  plugin/marketplace).
