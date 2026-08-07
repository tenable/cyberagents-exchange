---
name: "Tenable → FedRAMP POA&M Workbooks"
author: "conard0-git"
github_url: "https://github.com/conard0-git/tenable-fedramp-poam"
description: "Build FedRAMP POA&M workbooks from Tenable.sc — a vulnerability POA&M enriched with team attribution and remediation context, plus STIG/CIS Configuration Findings."
license: "MIT"
tier: "contributed"
tags: ["fedramp", "poam", "conmon", "tenable", "security-center", "stig", "cis", "kev", "vulnerability-remediation"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-07
contribution_agreement_date: 2026-08-06T20:32:58Z
compatible_platforms: ["Claude Code"]
invocation: "/tenable-fedramp-poam"
---

Turn raw Tenable Security Center findings into the monthly FedRAMP
continuous-monitoring (**ConMon**) POA&M deliverables a vulnerability-
management team actually uses: a **vulnerability POA&M workbook** with
team attribution and remediation context, and a **STIG/CIS Configuration
Findings** workbook mapped to the same FedRAMP Open POA&M Items schema.
Both workbooks produce content compatible with the formal POA&M — the
vulnerability workbook adds per-host detail, team ownership (from cloud
tags + Nessus agent groups), aging, and KEV/BOD 22-01 flags so the same
data drives both compliance submission and engineering remediation
handoff. (POA&M = *Plan of Action and Milestones*.)

This is a **documentation skill** — it teaches the workflow and the
FedRAMP mappings so a Claude Code assistant can reproduce the pipeline
against your own environment; it does not ship a runnable implementation.

## What it does

- **Vulnerability POA&M workbook (with team attribution and remediation
  context).** Pulls `analysis.vulns` from Tenable.sc per repository
  (plugin-centric, unioning host findings, CVE intersections, first/last-
  seen, CVSS), classifies OS from Tenable's authoritative
  `operatingSystem` attribute only, separates OS patches from
  application/library updates via a two-stage classifier, and emits
  per-OS + per-agent-group tabs plus a dashboard with a ConMon status
  banner, severity inventory, and multi-month trend. Cloud tags and
  Nessus agent-group membership attach team ownership to each row so the
  same data both feeds the FedRAMP POA&M and routes work to engineering.

- **STIG / CIS Configuration Findings.** Pulls compliance results
  (`pluginType=compliance`, severities 2 & 3 — failed + manual-review),
  extracts DISA STIG **CAT I / II / III** categories from prioritized
  Tenable fields, parses CIS control IDs and DISA Vuln-IDs (formats like
  `X.X.X`, `V-XXXXXX`, `RHEL-XX-XXXXXX`) as stable control aliases, and
  emits per-OS/benchmark failure tabs plus a **Configuration Findings
  (POA&M)** tab mapped to the FedRAMP Open POA&M Items schema (30-column
  canonical layout).

- **Framework-dependent SLA + KEV.** Computes past-due against
  remediation windows selectable per environment — Critical/High = 30
  days and Moderate = 90 across frameworks, and **Low = 180 days
  (FedRAMP) or 120 days (DoD)** with DoD taking precedence when both
  apply. Cross-references the CISA Known Exploited Vulnerabilities
  catalog for **BOD 22-01** items and treats KEV-past-due as the
  top-priority signal.

- **Deviation model.** Applies an approved-plugin allowlist that
  **marks** findings as accepted/deviated rather than removing them —
  expired approvals revert to not-approved, boilerplate rationale
  downgrades to pending. Handles Tenable's plugin-ID churn via stable
  control aliases so approvals survive STIG republishes.

- **Month-over-month baselines.** Writes per-environment JSON baselines
  each run so New / Remaining / Closed can be computed per SLA band, and
  drift/regression alerts surface on the dashboard.

- **Multi-environment merge.** Runs across many Tenable.sc repositories,
  keeps results environment-segregated, then merges into one workbook
  with a leading Combined Summary tab and label-prefixed environment
  tabs (with the openpyxl chart-copy corruption workaround and Excel
  book-view / sheet-title rules that most teams learn the hard way).

## How it works

The pipeline is **read-only against Tenable** — it queries, computes,
and writes Excel; it never modifies Tenable data, hosts, or agents. The
only optional write to a source-of-record is assigning POA&M IDs back
into your local deviation store. Cloud enrichment is optional — AWS EC2
is the reference implementation but the same IP→host/owner matching
applies to any cloud provider (Azure, GCP, etc.); with no cloud access
the pipeline degrades gracefully and labels hosts from Tenable's own
DNS/hostname fields. Everything site-specific — repository IDs,
environment labels, subnet ranges, inventory file paths, deviation
store location — lives in configuration, never in code. Remediation SLA
day-counts are the one exception: they are code constants you edit to
match your authorization boundary (the as-of date is the one
environment-driven SLA input). See `SKILL.md` for the shared pipeline,
`references/vuln-poam.md` for the vulnerability POA&M workflow,
`references/stig-config-findings.md` for the STIG/CIS + POA&M schema
mapping, and `references/deviations-and-merge.md` for the deviation
model + Excel merge mechanics.
