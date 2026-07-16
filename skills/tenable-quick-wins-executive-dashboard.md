---
name: "Tenable Quick Wins Executive Dashboard"
author: "rafansmpj"
github_url: "https://github.com/rafansmpj/Tenable-CloudeDesktop-QUICK-WINS"
description: "Executive dashboard that prioritizes remediation to cut Tenable One Exposure Score by 10-50% in phases."
license: "MIT"
tier: "contributed"
tags: ["tenable-one", "exposure-management", "executive-dashboard", "quick-wins", "vulnerability-prioritization", "ciso"]
integrations: ["Tenable", "Tenable Hexa AI MCP", "Anthropic"]
date_added: 2026-06-30
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Desktop"]
invocation: "/tenable-quick-wins-dashboard"
---

A Claude Desktop skill that turns live Tenable One exposure data into a board-ready remediation
roadmap. Instead of a flat vulnerability list, it ranks remediation actions by a Quick Win
Score — high VPR, breadth of affected assets, and low patch effort, with bonus weight for
Crown Jewel assets and attack path chokepoints — and groups them into five cumulative phases
that walk the Exposure Score down from its current value toward a 50% reduction.

## What it does

Generates an interactive executive dashboard for prioritizing vulnerability remediation to
reduce the Tenable One Exposure Score across five cumulative phases (10% → 20% → 30% → 40% →
50%). The dashboard includes a score gauge, clickable phase cards, a score-progression chart,
an industry peer benchmark, and a board-ready executive summary. Supports both English and
Portuguese output.

Use it whenever someone asks for quick wins, a phased risk-reduction plan, a remediation
roadmap, where to start on vulnerability remediation, or an executive-level prioritization
view of exposure data.

## How it works

The skill connects to a Tenable One MCP server and pulls live Exposure View, Findings,
Crown Jewels, and Attack Path data. It computes a Quick Win Score for each candidate
remediation action as `(avg_VPR × affected_assets × breadth_factor) / relative_effort`, with
additional weight added when a Crown Jewel asset or an attack path chokepoint is involved.
Actions are then bucketed into five cumulative phases so the highest-impact, lowest-effort
fixes appear first, and the result is rendered as an interactive dashboard artifact. If no
MCP connection is available, it falls back to a clearly labeled demo dataset.
