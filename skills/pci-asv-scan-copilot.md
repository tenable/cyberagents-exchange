---
last_reviewed: 2026-09-09
name: "PCI ASV Scan Copilot"
author: "jdelong-tenb"
github_url: "https://github.com/jdelong-tenb/pci-asv-scan-copilot"
description: "Walks a PCI ASV user through the full quarterly external scan cycle — scan setup, launch and monitoring, finding review grouped by PCI DSS v4.0 requirement, dispute candidate identification, and attestation readiness check."
license: "MIT"
tier: "contributed"
tags: ["pci-dss", "vulnerability-management", "asv-scanning", "compliance", "attestation"]
integrations: ["Tenable"]
date_added: 2026-08-31
contribution_agreement_date: 2026-08-31T00:00:00Z
compatible_platforms: ["Claude Code"]
invocation: "Say things like \"help me set up my quarterly PCI ASV scan,\" \"I need to run a PCI external vulnerability scan,\" \"which PCI findings can I dispute,\" or \"am I ready to submit my attestation\" — the skill activates automatically."
---

## What it does

PCI DSS Requirement 11.3.2 mandates quarterly external vulnerability scans of your cardholder data environment (CDE) by an Approved Scanning Vendor (ASV). The five places users get stuck — scan template selection, target scoping, interpreting which findings block attestation versus which are disputable, compensating controls framing, and knowing when to submit — are what this skill covers, against your real Tenable VM account state.

This is a community-built skill, not official Tenable support and not PCI DSS compliance advice. Consult your QSA for authoritative compliance interpretation.

**Scope:** PCI external vulnerability scanning (ASV) only. Does not cover internal scans, penetration testing, or other PCI DSS requirements.

## How it works

Install the skill into your Claude Code skills directory. When invoked, it uses Tenable VM MCP tools to walk you through five phases:

1. **Scan setup** — checks existing PCI scan policies (`policy_list_policies`) and available ASV templates (`policy_templates`), then helps configure targets for your external-facing CDE components.
2. **Launch and monitor** — creates the scan (`scan_create`) and launches it (`scan_launch`), monitoring status (`scan_status`) until completion.
3. **Review findings** — pulls completed scan results (`scan_results`, `scan_host_details`, `plugins_get_plugin_details`) and groups findings by PCI DSS v4.0 requirement with plain-language explanations and CVSS scores.
4. **Dispute candidates** — identifies false positives and compensating control candidates with documentation guidance per finding type.
5. **Attestation readiness** — checks asset coverage (`workbenches_list_assets_with_vulnerabilities`), counts unresolved CVSS ≥ 4.0 findings, verifies the 90-day scan window, and issues a pass/conditional/fail verdict with specific action items.

Includes a utility script (`scripts/list_pci_scans.py`) to list existing PCI scans and available templates before you start.
