---
name: "Tenable Report Workshop"
author: "blckdvc"
github_url: "https://github.com/blckdvc/Tenable-Report-Workshop"
description: "Local app that turns Tenable Security Center and VM data into risk-ranked, branded PDF and Excel remediation reports."
license: "MIT"
tier: "contributed"
tags: ["remediation", "reporting", "security-center", "tenable-vm", "vpr", "pdf", "excel"]
domains: ["vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T18:22:03Z
---

Tenable Report Workshop is a local web app and CLI that turns Tenable vulnerability data into client-ready remediation reports. It runs entirely on your machine (bound to 127.0.0.1) and has no telemetry.

## What it does

- Imports findings from a Security Center or Tenable Vulnerability Management CSV export, or directly from either product's API using a saved query or a chosen scope (asset lists or tags).
- Groups plugin findings into concrete remediation actions through an editable rule set. For example, many "Product < X" findings become one "Install version X or later" action.
- Ranks actions by Security Center severity weighting, VPR, or VPR × ACR, and shows ACR, AES and an estimated Cyber Exposure Score when the data has them.
- Produces six report templates: a full remediation plan, an executive summary, per-machine sheets, a comparison of two exports, a themed PHP2Shell exposure report, and an Excel action-tracking workbook.
- Applies per-client branding (logo, colour, footer, watermark) and writes reports in French, English, Spanish or Italian.
- Can email a report through your own SMTP server, but only when you ask it to.

## How it works

A Flask server hosts a local interface, and `generer.py` exposes the same engine on the command line, so reports can run as scheduled jobs. The engine parses the export or API response, applies the CSV rule set, scores and orders the actions, and renders the PDFs with ReportLab and matplotlib and the workbook with openpyxl. API keys live in a local `config.json` that git ignores, or in environment variables. Data leaves your machine only for the calls you start yourself: to your Tenable instance, your SMTP server, or PyPI during setup.

Remediation actions are inferred from plugin names, so have a technical team review the plan before you send it to a client.
