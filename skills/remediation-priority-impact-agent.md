---
name: "Remediation Priority & Impact Agent"
author: "smjennings"
github_url: "https://github.com/smjennings/Remediation_Priority-Impact_Agent"
description: "Prioritizes daily vulnerability fixes using Tenable exposure data, CISA KEV exploitation, MITRE ATT&CK and attack paths"
license: "MIT"
tier: "unreviewed"
tags: ["vulnerability-management", "exposure-management", "remediation-prioritization", "cisa-kev", "mitre-attack", "attack-path-analysis"]
integrations: ["Tenable"]
date_added: 2026-06-18
compatible_platforms: ["Claude Code"]
invocation: "/fix-today"
---

A Claude Code skill that answers "What should I fix today?" by pulling live data from Tenable (Tenable One / Exposure Management and Vulnerability Management) and producing a prioritized remediation briefing.

## What it does

- **Ranks your most exposed assets** by Tenable's Asset Exposure Score (AES)
- **Confirms real exploited-in-the-wild status** from plugin exploit-intelligence (CISA KEV, exploited-by-malware, in-the-news, exploit frameworks) — not inferred from VPR
- **Layers MITRE ATT&CK and Attack Path Analysis**, sourced from Tenable's own APA where available, then CVE→tactic mapping
- **Scores each remediation** with a composite of AES, confirmed-exploit tier, VPR, asset criticality, attack-path position and blast radius
- **Surfaces the actual fix** — verbatim Tenable remediation (exact KBs, package versions, registry keys) plus interim mitigations
- **Renders an interactive dashboard** (priority table, ATT&CK heatmap, batched remediation groups, risk-reduction forecast) and a "Fix FIRST / NEXT / SOON" plan
- **Generates ready-to-paste change tickets** per host on request

## How it works

Invoked with `/fix-today`, the skill works through gather → confirm-exploitation → ATT&CK/attack-path mapping → prioritize phases, calling the Tenable MCP tools. It treats VPR as a ranking input only, confirming actual exploitation at the plugin level, and queries Tenable's Attack Path Analysis directly to flag the assets that sit on real attack paths (including identity/privilege pivots that patching won't fix). The output leads with what attackers are actually using, on the assets that matter most.
