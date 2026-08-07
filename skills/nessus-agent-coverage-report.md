---
name: "Nessus Agent Coverage Report"
author: "conard0-git"
github_url: "https://github.com/conard0-git/nessus-agent-coverage-report"
description: "Report Nessus agent coverage by correlating AWS EC2, the Nessus Manager agent list, and Tenable Security Center scan data. Read-only."
license: "MIT"
tier: "contributed"
tags: ["nessus", "tenable", "security-center", "aws", "ec2", "coverage-report", "compliance-reporting", "inventory"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-06
contribution_agreement_date: 2026-08-06T20:32:58Z
compatible_platforms: ["Claude Code"]
invocation: "/nessus-agent-coverage-report"
---

Report Nessus agent **coverage** — which live hosts have an agent, and (more
importantly) which do not. The skill correlates three data sources so a host
is only called a gap when it's genuinely live and genuinely un-agented:
the live cloud fleet (AWS EC2), optional on-premise subnets, and the Nessus
Manager agent inventory. Cross-references Tenable Security Center so a host
that is being *scanned* but has no installed agent is still surfaced. This
is the inverse of stale-agent cleanup: cleanup removes agents whose host is
gone; this finds hosts that exist but have no agent.

## What it does

- **Cloud fleet enumeration.** Pull running EC2 instances across all
  configured profiles/regions and capture primary private IP, primary public
  IP, Name tag, VPC, and launch date.
- **Nessus agent inventory.** Pull every installed agent from the Nessus
  Manager, normalizing status to online/offline (online wins on IP
  collisions).
- **Tenable Security Center enrichment.** Query each configured repository
  for its IP set (`sumip` analysis) — for cloud hosts this flags "scanned
  but un-agented" vs. "invisible"; for on-premise hosts it *is* the
  inventory source, with the on-prem universe defined as scanned IPs
  inside a caller-supplied CIDR list.
- **Match by identifier ladder.** Primary private IP → primary public IP →
  Name tag / hostname, so a host isn't falsely flagged as missing just
  because its agent registered under a different identifier.
- **Exclusions.** Honor an exclusion list (IPs or CIDRs, from a file or an
  env value) for hosts that intentionally can't or shouldn't carry an
  agent, so they don't appear as false gaps.
- **Excel coverage report.** Dashboard (totals, matched, missing after
  exclusions, on-prem breakdown) + an "EC2 hosts missing an agent" sheet
  (sorted by AWS profile then instance name) + an "on-prem hosts missing/
  offline" sheet (missing first, then most-recently-seen). Hosts in a
  configurable set of VPCs can be split onto a separate tab.

## How it works

The design guarantee is that the workflow is **read-only** — it never
installs, removes, or modifies agents; it only reports. Correlation runs on
three data sources merged into a single view: cloud says which hosts *should*
have an agent (or on-prem CIDRs + SC scan data does), the Nessus Manager
says which hosts *do*, and Security Center enrichment closes the gap on
"scanned but un-agented" so purely-invisible hosts and merely-un-agented
ones are distinguished. Configuration is entirely environment-variable
driven — cloud credentials/profiles/regions, Nessus URL + keys, optional SC
URL + keys + repository IDs, optional on-prem CIDR list, optional
exclusions — with no hardcoded secrets, hosts, CIDRs, or repo IDs. See
`SKILL.md` for the full workflow, `references/coverage-correlation.md` for
the matching + classification logic, and `references/reporting-and-exclusions.md`
for the Excel structure and exclusion model.
