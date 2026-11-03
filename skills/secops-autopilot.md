---
name: "SecOps Autopilot"
author: "sword0x00"
github_url: "https://github.com/sword0x00/SecOps-Autopilot"
description: "Drives Tenable CVE findings through KRI risk scoring, approval-gated remediation, containment, and verified evidence."
license: "MIT"
tier: "contributed"
tags: ["vulnerability-management", "tenable", "kri", "remediation", "claude-code", "secops"]
domains: ["governance-risk-compliance", "security-operations"]
integrations: ["Tenable", "Cisco", "Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-03T23:02:58Z
compatible_platforms: ["Claude Code"]
invocation: "/secops-autopilot"
---

SecOps Autopilot is an AI agent that carries an identified vulnerability from
detection to a verified, evidenced fix. It automates the KRI process across
Tenable, asset inventory, security controls, patch management, the NAC solution,
and ticketing, and writes an audit-ready evidence package.

## What it does

- Normalizes a CVE or advisory and resolves the affected endpoints and servers
  from Tenable.
- Runs the KRI-01 … KRI-09 register per asset and ranks by real risk rather than
  raw CVSS.
- Produces a remediation plan with patch targets and compensating controls.
- Creates a ticketing-system ticket only after a recorded Human Approval, then
  gates containment, patch submission, and restore behind separate Human Approval
  conditions.
- Verifies the fix with a fresh Tenable read and writes an audit-ready evidence
  package: Markdown/HTML reports and a SHA-256 manifest.
- Produces one consolidated management report across all CVEs and assets in
  Markdown, HTML, and PDF.

## How it works

Install the Python engine with `pip install -e .` and the Claude Code skill from
`SKILL.md`. The `secops` CLI runs the read-only pipeline with
`secops run --cve <CVE>` and stops at the first state change. Each gate is opened
explicitly with `secops approve --gate <ticket|remediation|containment|patch|restore>`.
Ticketing, NAC, EDR, and patch connectors are simulated by default and pluggable
for live systems; Tenable Vulnerability Management is live-tested, while the
Tenable Security Center and Cisco ISE ERS adapters follow documented APIs and are
marked not live-validated.
