---
last_reviewed: 2026-08-27
name: "ComplyAgent for Tenable One"
author: "nreynolds-pub-git"
github_url: "https://github.com/nreynolds-pub-git/complyagent"
description: "Turns a Tenable CIS/STIG/PCI compliance scan into a remediation runbook, exception register, and POA&M. Read-only."
license: "MIT"
tier: "contributed"
tags: ["compliance", "cis-benchmark", "stig", "poam", "tenable", "remediation", "nist-800-53"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-08-26
contribution_agreement_date: 2026-08-26T19:20:37Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code", "Claude Desktop", "Claude Cowork"]
invocation: "Run ComplyAgent"
---

ComplyAgent turns a Tenable compliance scan into auditor-ready remediation work without touching a host. It runs as a guided conversation over your existing Tenable One (Hexa AI) MCP connection in Claude, and every output is a document for a human to review — Phase 0 is read-only and never writes back to Tenable.

## What it does

Point it at a CIS/STIG/PCI compliance scan and it produces a per-asset system profile; an environment-aware remediation runbook (every failed/warning control classified apply / caution / do-not-apply with grounded, reversible steps); an auditor-ready exception register (business justification, compensating controls, residual risk — plus a ready-to-run Tenable Change Result rule per exception); and a POA&M draft (FedRAMP workbook + OSCAL + CSV) with a NIST 800-53 crosswalk. Everything is delivered as one rolled-up package.

## How it works

The core idea: disposition completeness tracks discovery completeness. ComplyAgent first works out what each system actually is and does — pairing the compliance scan with a credentialed vulnerability scan for deep per-host discovery — then decides each control accordingly. The same control can be a do-not-apply exception on a Kubernetes node and a straight apply on a plain server, decided by evidence rather than the control ID. An adaptive interview reads each host's own discovery, names what's likely also present, and asks only the questions whose answers would change a disposition. A deterministic Python skeleton parses, classifies, and renders the styled documents; the agent does the reasoning, grounded in a knowledge base — behind a human-approval gate.
