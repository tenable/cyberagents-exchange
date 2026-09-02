---
name: "PCI Failure Pattern Explainer"
author: "jdelong-tenb"
github_url: "https://github.com/jdelong-tenb/pci-failure-pattern-explainer"
description: "Analyzes a completed PCI scan and produces plain-English failure explanations, PCI DSS v4.0 requirement cross-references, a remediation priority ranking (critical path to pass vs. secondary), and a dispute-or-fix recommendation per finding type."
license: "MIT"
tier: "contributed"
tags: ["pci-dss", "vulnerability-management", "compliance", "remediation", "asv-scanning"]
integrations: ["Tenable"]
date_added: 2026-08-31
contribution_agreement_date: 2026-08-31T00:00:00Z
compatible_platforms: ["Claude Code"]
invocation: "Say things like \"explain my PCI scan failures,\" \"which PCI findings are critical to fix,\" \"which findings can I dispute vs. must fix,\" or \"help me prioritize my PCI remediation\" — the skill activates automatically."
last_reviewed: 2026-08-31
---

## What it does

A completed PCI ASV scan returns plugin IDs and CVSS scores — but it does not tell you which failures actually block your attestation, which are disputable false positives, or what the PCI DSS requirement behind each finding is. This skill reads a completed scan and produces a structured analysis against your real Tenable VM account state.

This is a community-built skill, not official Tenable support and not PCI DSS compliance advice. Consult your QSA for authoritative compliance guidance.

**Scope:** Post-scan analysis of an already-completed PCI ASV scan. Does not run or configure scans — see the PCI ASV Scan Copilot skill for that.

## How it works

Install the skill into your Claude Code skills directory. When invoked with a scan ID or name, it uses Tenable VM MCP tools to:

1. **Retrieve the scan** — lists recent scans (`scan_list_scans`) and pulls results for the selected scan (`scan_results`).
2. **Categorize findings** — groups by severity into: attestation-blocking (CVSS ≥ 4.0), informational/low (CVSS < 4.0). For each blocking finding, calls `plugins_get_plugin_details` for full description and DSS cross-references; calls `workbenches_get_vulnerability_outputs` for raw scanner output when needed to assess disputes.
3. **Explain each failure** — plain-language description of what the scanner found and why it is a risk to cardholder data, with a PCI DSS v4.0 requirement cross-reference for each finding.
4. **Rank remediation priority** into three levels: critical path (CVSS ≥ 7.0, must fix), attestation blockers with dispute potential (CVSS ≥ 4.0), and informational.
5. **Recommend dispute or fix** per finding — with evidence checklists for dispute cases and specific remediation steps with time estimates for fix cases.

Includes a command-line script (`scripts/pci_failure_summary.py`) to print an attestation-blocking findings summary for any scan without using the skill.
