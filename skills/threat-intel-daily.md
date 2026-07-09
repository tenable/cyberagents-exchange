---
name: "Daily Threat Intelligence Briefing"
author: "smjennings"
github_url: "https://github.com/smjennings/threat-intel-daily"
description: "A daily, fully-sourced cyber threat intelligence briefing for CISOs, correlated against your Tenable environment."
license: "MIT"
tier: "unreviewed"
tags: ["threat-intelligence", "ciso", "cti", "vulnerability-management", "tenable", "security-automation"]
integrations: ["Tenable", "Anthropic"]
date_added: 2026-06-18
compatible_platforms: ["Claude Code"]
invocation: "/threat-intel-daily"
---

A Claude Code skill that builds a daily cyber threat intelligence briefing for a CISO from open-source intelligence, then correlates it against your own Tenable vulnerability-management environment — turning "industry news" into "your problem."

## What it does

- Answers four daily questions: what's in the news from a threat perspective, what new exploits to care about, what CISOs need to know, and how to brief the board.
- Produces three sectioned views: by industry, by tech stack (led by what you actually run), and a general CISO briefing with board talking points.
- Correlates the day's top exploited CVEs against your Tenable inventory and labels each item exposed / possibly-exposed / not-in-inventory.
- Enforces strict sourcing — every claim carries a dated, tiered citation — and a recency gate (72h default window).
- Renders an interactive HTML dashboard and writes a dated report file.

## How it works

Phased: set the lookback window, gather sourced intel via web search across tiered sources (CISA/vendor PSIRTs → vendor research → reputable press), rank exploits by real-world risk (KEV/EPSS over raw CVSS), correlate against Tenable software inventory and findings, then assemble the three-section report with board talking points and a full Sources appendix.
