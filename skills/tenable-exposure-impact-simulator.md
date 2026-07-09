---
name: "Tenable Exposure Impact Simulator"
author: "dpickenstenable"
github_url: "https://github.com/dpickenstenable/tenable-exposure-impact-simulator"
description: "What-if analysis engine for Tenable AES/CES remediation impact prediction with optimization algorithms"
license: "MIT"
tier: "unreviewed"
tags: ["tenable", "simulation", "aes", "ces", "remediation", "prioritization", "optimization"]
integrations: ["Tenable"]
date_added: 2026-06-23
compatible_platforms: ["Claude Code"]
invocation: "/tenable-exposure-impact-simulator"
---

The Tenable Exposure Impact Simulator answers "what if" questions before you remediate. Predict Asset Exposure Score (AES) and Cyber Exposure Score (CES) changes to prioritize vulnerabilities by actual risk reduction, not just severity scores.

## What it does

- **Predict AES/CES Impact** — Know before you patch how much risk reduction you'll achieve on individual assets and across your organization
- **Optimize Remediation Sequences** — Find the fastest path to your target CES using greedy or knapsack algorithms
- **Compare Strategies** — Evaluate crown jewels vs. CISA KEVs vs. top VPR scores side-by-side with ROI metrics
- **Budget-Constrained Planning** — "I have 20 hours this week, maximize my CES reduction" with automatic optimization
- **Crown Jewel Targeting** — Calculate minimum effort to remove crown jewel status (AES < 900) across all high-risk assets
- **Scenario Simulation** — Step through cumulative impact of patching vulnerabilities in any order

## How it works

The skill connects to Tenable VM via MCP Server or Direct API and retrieves current asset AES scores and vulnerability data. It applies a weighted heuristic model that factors in VPR score, severity, exploit availability, vulnerability age, and patch availability to estimate AES reduction for each remediation action. Results are aggregated to organizational CES using tier-weighted averaging (crown jewels weighted 3x, high exposure 2x, medium 1x, low 0.5x). 

The optimization engine uses greedy CES-per-hour or knapsack dynamic programming algorithms to find optimal remediation sequences within time/resource constraints. All predictions include confidence intervals (High ±5%, Medium ±10%, Low ±20%) based on historical data availability and scenario complexity.
