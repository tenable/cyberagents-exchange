---
name: "security-intel-brief"
author: "pramseier-tenb"
github_url: "https://github.com/pramseier-tenb/security-intel-brief"
description: "Build a leadership-ready security intelligence brief (PDF) for selected vendors and software products, down to specific versions"
license: "MIT"
tier: "unreviewed"
tags: ["vulnerability-research", "cve", "security-reporting", "threat-intelligence", "pdf-reports"]
integrations: ["NVD"]
date_added: 2026-06-15
compatible_platforms: ["Claude Code"]
invocation: "/security-intel-brief"
---

A Claude Code skill that produces leadership-ready security intelligence briefings in PDF format. Target specific vendors, products, and versions to get comprehensive vulnerability assessments with risk ratings and actionable recommendations.

## What it does

Collects live security intelligence for the software you specify:

- **CVE data** from NVD API with exact-version matching via CPE
- **CISA KEV status** to identify known exploited vulnerabilities confirmed in the wild
- **Version and EOL tracking** from endoflife.date to flag outdated or unsupported software
- **Vendor advisories and security news** via web search for the most recent threat landscape
- **Risk ratings** (Critical/High/Medium/Low) per product with stated rationale
- **Polished PDF reports** with executive summary, risk overview table, recommended actions, and detailed per-product sections

All data is fetched at runtime from live sources — nothing comes from model memory, ensuring accuracy and currency.

## How it works

The skill uses an interactive form (or chat prompts) to collect target vendors, products, and versions. It then researches each target in parallel using the NVD CVE API, CISA KEV data, endoflife.date, and web search for advisories. After assigning risk ratings based on exposure and exploitability, it generates a structured JSON report and renders it to a branded PDF using the included Python script. The result is a concise, leadership-ready briefing that leads with risk and recommended actions.

Perfect for security teams preparing briefings for leadership, compliance reviews, or patch prioritization meetings.
