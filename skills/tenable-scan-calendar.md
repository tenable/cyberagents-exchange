---
name: "Tenable Scan Calendar"
author: "ylliermij"
github_url: "https://github.com/ylliermij/Tenable_Calendar"
description: "Puts actively-scheduled Tenable VM scans due in the next 7 days onto your calendar, with severity breakdown from each scan's last completed run."
license: "Apache-2.0"
tier: "contributed"
tags: ["tenable", "vulnerability-management", "calendar", "scan-scheduling"]
integrations: ["Tenable"]
date_added: 2026-07-27
contribution_agreement_date: 2026-07-27T00:35:43Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Cowork"]
invocation: "natural language — triggers on requests like 'what Tenable scans are coming up', 'put my scans on my calendar', 'sync my scans to my calendar', or 'what's scanning this week'"
---

A Claude skill that syncs actively-scheduled Tenable Vulnerability Management scans onto your calendar, with severity context from each scan's last completed run.

## What it does

Finds Tenable VM scans with an active recurring schedule that are due to run in the next 7 days and creates one calendar event per scan. Each event's description includes the severity breakdown (critical/high/medium/low/informational) from that scan's most recent completed run, so the person can see at a glance both when the next scan fires and how bad things looked last time. Scans that are disabled, orphaned (referencing a scanner that no longer exists), or whose next-run time can't be confidently inferred from history are handled explicitly rather than silently included or dropped — the user is told what's uncertain instead of being shown a confident-looking guess.

## How it works

The skill confirms a scan's schedule is actually enabled (rather than assuming existence means scheduled), infers cadence and next-run time from the pattern of recent runs in `scan_history` since Tenable's API doesn't expose the schedule's rrule directly, and pulls severity counts from the most recent completed run via `scan_results`. A bundled Python script (`scripts/parse_severity.py`) parses the per-host and per-finding severity data — handling both inline and large/file-based results — so severity totals are computed programmatically rather than eyeballed. Calendar events are created as free/available blocks so a background scan doesn't appear to occupy the user's time.
