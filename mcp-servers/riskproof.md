---
name: "RiskProof"
author: "creimer808"
github_url: "https://github.com/creimer808/RiskProof"
description: "Agentic vulnerability investigator that turns Tenable/Nessus findings into evidence-backed remediation decisions"
license: "MIT"
tier: "contributed"
tags: [vulnerability-prioritization, tenable, nessus, epss, cisa-kev, greynoise, risk-scoring, mcp]
domains: ["vulnerability-management", "threat-intelligence"]
integrations: ["Tenable"]
date_added: 2026-11-03
contribution_agreement_date: 2026-11-03T18:20:35Z
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop"]
tools_exposed:
  - name: "import_nessus"
    description: "Import a .nessus report from the operator-configured import directory and return a KEV-aware triage summary with ranked candidates"
  - name: "import_tenable"
    description: "Read-only Tenable Vulnerability Management export via API, with an optional asset-tag filter"
  - name: "list_tenable_tags"
    description: "List the tenant's Tenable tag categories and values to build a tag filter"
  - name: "investigate_finding"
    description: "Build the evidence record and risk assessment for findings (batches of 25)"
  - name: "enrich_threat_intel"
    description: "Fetch EPSS scores and CISA KEV status for CVEs, with provenance"
  - name: "verify_applicability"
    description: "Cross-check scanner claims against observed versions and flag suspected false positives"
  - name: "validate_exposure"
    description: "Non-destructive connectivity, banner and certificate checks against allowlisted targets only"
  - name: "analyze_exploit_scenario"
    description: "Describe exploit prerequisites, exposure, KEV-grounded consequences and explicit uncertainties"
  - name: "simulate_remediation"
    description: "Compare fix, restrict and verify options and their expected risk effects"
  - name: "execute_risk_policy"
    description: "Apply a P1-P4 decision table and record approval-gated, dry-run-by-default actions"
  - name: "get_audit_trail"
    description: "Read the append-only audit trail for a finding or recent activity, including pending actions"
  - name: "generate_report"
    description: "Write a self-contained HTML report of investigated findings (owner-only file permissions)"
resources_exposed: []
prompts_exposed: []
---

RiskProof is an MCP server that turns raw scanner output into defensible remediation decisions. It is an investigator, not a scanner and not a generic CVSS calculator: it evaluates what a finding means for your organization and records its reasoning.

## What it does

- Imports findings from a Nessus `.nessus` report or from Tenable Vulnerability Management (read-only export, optional tag filter).
- Enriches CVEs with FIRST EPSS scores, CISA KEV status and, optionally, GreyNoise exploitation signals. EPSS is always reported as a statistical probability, never as a claim about a specific system.
- Applies operator-supplied asset context (criticality, environment, internet exposure) and flags suspected false positives.
- Runs authorized, non-destructive validation checks (TCP connect, HTTP banner, TLS certificate dates) against targets on an operator-controlled allowlist.
- Produces exploit scenarios, remediation what-ifs and P1-P4 policy decisions, and writes a self-contained HTML report.

## How it works

RiskProof runs locally over stdio, one instance per analyst, and stores findings, evidence and an append-only audit trail in SQLite. Scoring follows a documented decision table rather than a black-box score. Remediation actions are dry-run and approval-gated by default, and no remediation executors exist yet, so nothing can change a system. Import and report directories, validation targets and API credentials are operator configuration that tool arguments cannot override.

Outbound network calls go to the EPSS and KEV feeds, to the Tenable VM API (only when `import_tenable` is used) and to GreyNoise (only when a key is configured), plus the allowlisted validation targets. Tenable and GreyNoise keys are read from the server's process environment, never from a file or tool input. Setup uses `uv sync` and `uv run riskproof serve`. An offline demo on bundled SAMPLE data runs with `uv run riskproof demo`.
