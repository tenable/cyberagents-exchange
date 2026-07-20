---
name: "Tenable VM Onboarding Guide"
author: "jdelong-tenb"
github_url: "https://github.com/jdelong-tenb/tenable-vm-onboarding-guide"
description: "Walks a new Tenable Vulnerability Management user through onboarding — connectivity, scanner/agent linkage, first scan, the scan-to-findings milestone bridge, and tagging — by checking real account state instead of pointing at generic docs."
license: "MIT"
tier: "contributed"
tags: ["onboarding", "vulnerability-management", "customer-success"]
integrations: ["Tenable"]
date_added: 2026-07-09
contribution_agreement_date: 2026-07-09T22:50:48Z
compatible_platforms: ["Claude Code"]
invocation: "Say things like \"I just signed up for Tenable,\" \"how do I get started,\" \"I ran a scan but don't see anything,\" or \"my scanner won't link\" — the skill activates automatically based on its description."
last_reviewed: 2026-07-16
---

## What it does

Generic onboarding docs don't know where a new Tenable Vulnerability
Management (VM) user actually is. In practice, the steps people get stuck on
most are scanner/agent linkage, and — for those who do scan — actually
looking at the results afterward (the "scan-to-findings" gap). This skill
checks the user's real VM account state via the Tenable public API and walks
them through whichever of five steps they're stuck on: connectivity,
scanner/agent linkage, first scan, reviewing scan status, or tagging setup —
then points them at findings once everything else is working.

This is a community-built skill, not official Tenable support — it reads your
own account via the public API and gives best-effort guidance. It's
calibrated for a brand-new account with a small scan history; see the repo's
Known Limitations for the scale caveat on established accounts.

**Scope:** Tenable Vulnerability Management onboarding only. It does not cover
WAS, ASM, Identity Exposure, or Cloud Security onboarding.

## How it works

Install the skill into your Claude Code skills directory. When invoked, it:

1. Runs `scripts/check_onboarding_status.py` against your own Tenable
   Vulnerability Management API keys (`TIO_ACCESS_KEY` / `TIO_SECRET_KEY`).
2. Checks connectivity, scanner/agent linkage, scan completion, findings, and
   tag setup, and determines the earliest stage you haven't cleared —
   distinguishing a check that failed to run (surfaced as `*_check_error`)
   from one that ran and confirmed something is genuinely absent.
3. Guides you through that specific step conversationally, re-checking real
   account state rather than trusting "I did it" at face value. For tagging, it
   hands off to Hexa MCP tools when available rather than duplicating that
   capability — and doesn't assume you know what Hexa is just
   because it happens to be available in the session.

Covered by 13 unit tests (stdlib `unittest`, mocked API responses) and
live-tested against a real Tenable VM account.

Dashboards, role-based personalization, and gamification are out of scope for
this skill — see the repo's
[Known Limitations](https://github.com/jdelong-tenb/tenable-vm-onboarding-guide#known-limitations).
