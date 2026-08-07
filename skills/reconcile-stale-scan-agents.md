---
name: "Reconcile Stale Scan Agents"
author: "conard0-git"
github_url: "https://github.com/conard0-git/reconcile-stale-scan-agents"
description: "Reconcile Nessus agents against a live AWS EC2 fleet and safely remove only the agents whose host is truly gone."
license: "MIT"
tier: "contributed"
tags: ["nessus", "tenable", "aws", "ec2", "vulnerability-management", "agent-cleanup", "inventory-reconciliation"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-06
contribution_agreement_date: 2026-08-06T20:32:58Z
compatible_platforms: ["Claude Code"]
invocation: "/reconcile-stale-scan-agents"
---

Keep a Nessus Manager agent inventory clean by reconciling it against a live
cloud fleet and removing only the agents whose underlying host no longer
exists. The guiding principle is **safety-first deletion**: an offline agent
is not proof that a host is gone, so the skill only deletes an agent after
confirming, against the cloud provider's own inventory, that the host is
truly terminated or missing.

## What it does

- Enumerates the live cloud fleet (AWS EC2 in the reference implementation),
  splitting instances into running and stopped and mapping every NIC's
  private IP so multi-NIC hosts resolve correctly.
- Pulls the full Nessus Manager agent list and considers only offline agents
  as cleanup candidates — online agents are never touched.
- Classifies each offline agent's host as running (protected), stopped
  (skipped by default), terminated/missing (eligible), or reused (delete
  stale record).
- Runs dry-run by default: proposes deletions to a resumable JSON report and
  does nothing destructive without explicit confirmation.
- Surfaces running hosts that have no agent record at all — a coverage-gap
  report that is alerted but never used to delete anything.
- Optionally scrubs deleted hosts' findings from a Tenable Security Center
  repository (scan-import reconciliation) as a best-effort follow-up.
  Security Center-specific; Tenable.io / Vulnerability Management uses a
  different asset/findings model that this path does not target.

## How it works

The skill treats the cloud provider as the source of truth for what is
alive. It matches each offline Nessus agent against the fleet by IP (across
every NIC the agent reports), then applies a conservative decision table:
running hosts are always skipped, stopped hosts are skipped unless the user
overrides, and only truly-terminated or IP-reused records are eligible for
deletion. Configuration is entirely environment-variable driven — no config
files, no hardcoded secrets, account IDs, or subnet ranges — so the skill
stays portable. See `SKILL.md` for the full workflow,
`references/aws-ec2-reconciliation.md` for the AWS EC2 details, and
`references/findings-cleanup.md` for the optional Tenable findings scrub.
