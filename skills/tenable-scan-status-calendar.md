---
name: "Tenable Scan Status Calendar"
author: "ylliermij"
github_url: "https://github.com/ylliermij/Tenable_Scan_Cal_sync"
description: "Puts upcoming Tenable VM scan jobs on Google Calendar and flags any scan whose last run aborted or failed, so broken scan configs get noticed instead of quietly re-running unattended."
license: "MIT"
tier: "contributed"
tags: ["tenable", "vulnerability-management", "calendar", "google-calendar", "scan-scheduling", "monitoring"]
integrations: ["Tenable"]
date_added: 2026-08-14
contribution_agreement_date: 2026-08-14T17:25:31Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code", "Claude Cowork"]
invocation: "tenable-scan-status-calendar"
---

Turns your Tenable VM scan schedule into a Google Calendar early-warning system, instead of just a list of "next run" times.

## What it does

For every Tenable VM scan with an active recurring schedule due to fire in the next 7 days, the skill creates one Google Calendar event. The event description pairs "when this will run next" with "how did the most recent run go" — findings by severity and number of assets scanned from the last completed run. If the most recent run of that scan aborted or failed, the description opens with a clear warning so the person investigates before the scan fires again unattended. A scan that keeps re-running on a broken config is a worse outcome than a scan that quietly finds nothing, and a calendar of run times alone doesn't surface that.

## How it works

Tenable's VM API doesn't expose a scan's schedule start time or rrule directly, and there's no pure read-only call for the current enabled/disabled state — so the skill infers both from data it can read. It lists all scans, calls the scan-configure endpoint with only the scan ID (a read-back trick that changes nothing) to check whether the schedule is enabled, then looks at each enabled scan's recent run history to infer its cadence and project the next occurrence inside the coming 7-day window.

For findings, the skill deliberately looks at the single most recent run regardless of status, not just the last clean one. A completed run sources the findings summary directly; an aborted, failed, or in-progress run triggers a fallback to the most recent completed run for the numbers (labeled as such), plus a status-appropriate note in the calendar description — a warning for aborted/failed, a neutral note for still-running. Severity and asset counts are extracted from the scan results text (via a bundled Python helper for accurate summation across potentially hundreds of hosts) rather than hand-totaled, and a scan reporting zero hosts is flagged rather than treated as an unremarkable clean result. The skill only reads from Tenable and writes to Google Calendar — it never modifies scan configuration.
