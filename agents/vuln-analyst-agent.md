---
name: "Vuln Analyst Agent"
author: "Ash Collins"
github_url: "https://github.com/digitalpapercut/vuln-analyst"
description: "AI agent that applies CISA SSVC to live CVE data (EPSS, KEV, NVD, OSV) for defensible patch decisions."
license: "MIT"
tier: "contributed"
tags: ["vulnerability-management", "ssvc", "cve-triage", "epss", "cisa-kev", "browser-extension", "security-research"]
integrations: ["NVD", "Anthropic"]
date_added: 2026-07-16
contribution_agreement_date: 2026-07-17T01:35:42Z
works_with_tenable_hexa_mcp: false
last_reviewed: 2026-07-16
---

An open-source AI agent for vulnerability research and triage. Point it at any CVE and it fetches live data from EPSS, CISA KEV, NVD, cvelistV5, OSV.dev, and public exploit indexes, walks the finding through the CISA SSVC decision tree, and produces a defensible verdict with its full evidence chain — not just a score.

Three ways to use it: a browser extension that works on any CVE page, a CLI harness for automation and scripting, or a set of AI coding assistant skills (Claude Code, Cursor, Copilot). No data-source API keys are required — all enrichment sources are free and open.

## What it does

Most vulnerability tooling tells you *what* to patch. This agent reasons about *when* you can actually act and *whether* a finding is an emergency — applying the CISA SSVC decision framework to produce an **Act / Attend / Track\* / Track** verdict that accounts for exploitation evidence, attack automation potential, technical impact, and your environment's specific exposure.

It offers three tabs of output: **Triage** (SSVC verdict, signal strip of EPSS/KEV/exploit tooling, decision inputs, and an environment context form to refine the decision), **Research** (a full multi-source enrichment profile — CVSS decoded, CWE, affected versions, exploit tooling, identifier aliases), and **Write-up** (one-click executive summary, remediation ticket, or auditor-ready risk-acceptance memo generated from the actual evidence fetched during triage).

## How it works

The agent never states a score, status, or version from model memory — it fetches from EPSS, CISA KEV, NVD 2.0, cvelistV5, OSV.dev, and public Nuclei/Metasploit indexes, cites the source, and states the data date. Before rendering a verdict it asks about asset exposure and mission impact, and shows how the decision changes under different answers. All data sources are free and open, so the methodology works regardless of which scanner or vendor produced the underlying finding. The agent is read-only by construction: it researches and advises, but does not take action on your behalf.
