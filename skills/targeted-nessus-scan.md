---
name: "Targeted Nessus Scan"
author: "conard0-git"
github_url: "https://github.com/conard0-git/targeted-nessus-scan"
description: "On-demand Nessus vulnerability and compliance/audit scans of specific hosts, one combined Excel report, and agent-profile assignment."
license: "MIT"
tier: "contributed"
tags: ["nessus", "tenable", "stig", "cis", "compliance", "vulnerability-scanning", "aws", "ec2", "reporting"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-06
contribution_agreement_date: 2026-08-06T20:32:58Z
compatible_platforms: ["Claude Code"]
invocation: "/targeted-nessus-scan"
---

Launch ad-hoc, agent-based scans against a known set of hosts on an existing
Nessus Manager, aggregate the findings into one combined Excel workbook, and
manage agent-profile assignments — by explicit IP list or by matching cloud
(AWS EC2) instances on a tag. Built around temporary, self-cleaning scan
artifacts so an on-demand scan never leaves stray groups or state behind.

## What it does

- **Ad-hoc targeted scan.** Take an IP list and one or both scan types
  (vulnerability, compliance/audit — DISA STIG, CIS, or any Nessus audit
  policy), resolve the linked agents on the chosen Nessus Manager, create a
  temporary agent group, launch the scan against a named policy, poll to
  completion, and export the `.nessus` result.
- **Combined Excel report.** Aggregate the findings into a single workbook:
  Dashboard tab (with hyperlinks to the finding sheets), Vulnerability
  Findings tab, and a STIG Findings tab that holds every FAILED item from
  whatever compliance/audit policy you ran. Color-code rows on a shared
  scale — Critical or High → red, Medium → orange, Low → yellow, unknown →
  gray. DISA STIG audits are categorized by CAT level (CAT I → red,
  CAT II → orange, CAT III → yellow) and sorted CAT I → II → III; audits
  that don't expose a CAT (e.g. a CIS benchmark) still have their failed
  items reported, bucketed under "Unknown" until the parser is extended to
  read that framework's native severity field.
- **Agent-profile assignment.** Two entry points: assign by explicit IP
  list, or match AWS EC2 instances by a tag substring and assign their
  Nessus agents to the target profile (looked up by UUID or name). Agents
  already on the target profile are detected and skipped. The interactive
  menu always previews (matched instance names + Nessus linkage) and
  requires confirmation before assigning; the CLI path exposes the same
  preview via an opt-in `--dry-run`. Supports a repeatable per-manager
  override when agents span multiple Nessus Managers.
- **Automatic cleanup.** Temporary scan groups are removed after the run
  unless the caller explicitly opts out; raw `.nessus` files are kept only
  on explicit request.

## How it works

The skill separates *per-run* state (the temporary agent group used for the
targeted scan) from *long-lived* state (the agent profile a host stays
assigned to). Both are treated as intentional mutations of the Nessus
Manager and are never conflated. Compliance parsing is framework-aware:
DISA STIG audits get CAT-level classification (with robust detection across
STIG output variants), while other Nessus audit policies fall back to
pass/fail with their native severity field. Configuration is entirely
environment-variable driven — Nessus URLs and API keys, policy names to
reference, optional AWS credentials for the cloud-tag flow — with no
config files, hardcoded secrets, account IDs, or policy IDs. See
`SKILL.md` for the full workflow and practical notes for adopters,
`references/scanning-and-reporting.md` for the scan+report mechanics
(including framework-specific parsing), and
`references/agent-profile-assignment.md` for the profile-assignment flows
and platform notes.
