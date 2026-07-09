---
name: "Tenable Host Doctor"
author: "ddangthatscrazy"
github_url: "https://github.com/ddangthatscrazy/tenable-host-doctor"
description: "Diagnoses why a single host failed a Tenable credentialed scan, from its .nessus export."
license: "MIT"
type: "tool"
tier: "unreviewed"
tags: ["tenable", "nessus", "vulnerability-management", "credentialed-scan", "troubleshooting"]
framework: "Python"
integrations: ["Tenable"]
date_added: 2026-06-18
---
Tenable Host Doctor is a local-first, deterministic diagnostic tool that explains
why a specific host failed — or only partially completed — a Tenable Nessus
credentialed scan. It reads a host's `.nessus` export, classifies the root cause
from the actual plugin evidence, and produces an actionable report. An optional
LLM layer adds plain-language narrative on top of the deterministic findings.

## What it does
Given one host from a Nessus scan, it determines the single most likely reason
credentialed local checks didn't run as expected — distinguishing genuine
credential failures from privilege, registry, database, integration, connectivity,
agent-vs-scanner, and host-discovery causes — and returns specific remediation for
the protocol involved (SMB/WMI or SSH). It also surfaces scan-tuning, port-coverage,
and scanner-placement context where the evidence supports it.

## How it works
The tool parses the `.nessus` export (plugin outputs and policy preferences) and runs
a set of deterministic analyzers that key off verified Tenable plugin semantics. It
reports a single primary verdict plus additive findings that can coexist with it, and
is built to assert only what the plugin evidence supports — ambiguous signals are
surfaced as leads, not conclusions. The deterministic core runs without any AI; the
optional LLM enrichment layer interprets the findings in plain language.