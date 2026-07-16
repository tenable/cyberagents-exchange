---
name: "Cyber Risk Quantifier"
author: "spacebar-tenb"
github_url: "https://github.com/spacebar-tenb/cyber-risk-quantifier"
description: "FAIR-aligned cyber risk quantification — transforms Tenable vulnerability data into board-ready financial risk PDFs"
license: "MIT"
tier: "contributed"
tags: ["cyber-risk", "fair-model", "risk-quantification", "vulnerability-management", "pdf-reporting", "tenable"]
integrations: ["Tenable"]
date_added: 2026-07-16
contribution_agreement_date: 2026-07-16T12:44:04Z
---

Cyber Risk Quantifier is a Python CLI that takes Tenable One Vulnerability Management scan exports and produces board-ready PDF reports with defensible, per-exposure financial risk estimates using the FAIR (Factor Analysis of Information Risk) framework.

## What it does

- Parses Tenable One Vulnerability Management CSV exports with flexible column detection and deduplicates by Plugin ID + Host
- Quantifies each exposure using ALE = LEF × SLE (Annualized Loss Expectancy = Loss Event Frequency × Single Loss Expectancy)
- Derives LEF and loss magnitude from Tenable VPR scores — no reliance on static CVSS severity
- Generates multi-page PDF reports with executive summary, scope context, FAIR methodology, risk portfolio, business impact analysis, remediation recommendations with SLA targets, and detailed exposure breakdowns
- References IBM Cost of a Data Breach Report 2025 benchmarks across 17 industries
- Supports optional business context config for asset criticality, service mapping, and compliance frameworks

## How it works

The tool reads a Tenable One Vulnerability Management CSV export, deduplicates rows by Plugin ID + Host (one exposure per missing patch per asset), then scores each exposure independently using VPR-derived probability and loss magnitude against industry breach cost data. Priority tiers (P0–P3) are assigned based on financial thresholds, and a Recommendations section provides remediation impact analysis with investment justification framing for budget conversations.
