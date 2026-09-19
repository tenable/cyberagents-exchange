---
name: "PCI Failure Pattern Explainer"
author: "jdelong-tenb"
github_url: "https://github.com/jdelong-tenb/pci-failure-pattern-explainer"
description: "Analyzes a completed PCI ASV scan and produces plain-English failure explanations, PCI DSS v4.0 requirement cross-references, a remediation leverage table (ranked by findings cleared per action), dispute-or-fix recommendations with evidence checklists, scan age validation, and an optional HTML report by asset."
license: "MIT"
tier: "contributed"
tags: ["pci-dss", "vulnerability-management", "compliance", "remediation", "asv-scanning"]
domains: ["governance-risk-compliance", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-08-31
contribution_agreement_date: 2026-08-31T00:00:00Z
compatible_platforms: ["Claude Code"]
invocation: "Say things like \"explain my PCI scan failures,\" \"which PCI findings are critical to fix,\" \"which findings can I dispute vs. must fix,\" or \"help me prioritize my PCI remediation\" — the skill activates automatically."
last_reviewed: 2026-09-14
---

## What it does

A completed PCI ASV scan returns plugin IDs and CVSS scores — but it does not tell you which failures actually block your attestation, which are disputable false positives, or what the PCI DSS requirement behind each finding is. This skill reads a completed scan and produces a structured analysis against your real Tenable VM account state.

This is a community-built skill, not official Tenable support and not PCI DSS compliance advice. Consult your QSA for authoritative compliance guidance.

**Scope:** Post-scan analysis of an already-completed PCI ASV scan. Does not run or configure scans — see the PCI ASV Scan Copilot skill for that.

## How it works

Install the skill into your Claude Code skills directory. When invoked with a scan ID or name, it uses Tenable VM MCP tools to:

1. **Retrieve the scan** — identifies the scan by name or ID, validates scan age (flags scans > 60 days old against the 90-day PCI validity window), and confirms pass/fail status via plugin 33929/33930.
2. **Categorize findings** — groups by severity: attestation-blocking (CVSS ≥ 4.0) vs. informational. Clarifies what "passing" means: all CVSS ≥ 4.0 findings must be resolved or disputed — compensating controls require a separate AoC process with a QSA.
3. **Explain each failure** — plain-language description with PCI DSS v4.0 requirement cross-reference per finding.
4. **Remediation leverage table** — groups findings by normalized solution text, classifies effort (Config / Patch / Version Upgrade / Major Upgrade / Decommission), ranks by CISA KEV first then by findings-cleared-per-action. Flags KB rollup groupings, EOL OS as infrastructure projects (not patch tickets), and Tomcat 9→10 as a major upgrade.
5. **Priority ranking** — includes a "Start Here" triage block: if backdoor/trojan plugins (SubSeven, WinShell, jspwebshell, cleartext credential leakage) appear, flags them for incident response before any patch work.
6. **Dispute or fix recommendation** — evidence checklists for dispute cases, specific remediation steps with time estimates for fix cases. Helps prepare evidence to submit through the attestation portal.
7. **Optional HTML report** — prompts the user; if yes, generates a self-contained report organized by asset with severity badges, effort tiers, and Tenable brand styling.

Includes a command-line script (`scripts/pci_failure_summary.py`) to print an attestation-blocking findings summary for any scan without using the skill.
