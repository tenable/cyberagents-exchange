---
name: "Tenable SC Health Check"
author: "byadler"
github_url: "https://github.com/byadler/tenable-sc-health-check"
description: "Monitor Tenable SC health — scans, credentials, scanners, feeds, license — with AI recommendations and safe one-click fixes"
license: "MIT"
tier: "contributed"
tags: ["tenable", "security-center", "health-check", "vulnerability-management", "python", "monitoring", "operations"]
integrations: ["Tenable", "Anthropic"]
date_added: 2026-07-23
contribution_agreement_date: 2026-07-23T16:26:45Z
---

An open-source Python tool that monitors the health of your on-prem Tenable Security Center — scans, credentials, scanners, scan zones, plugin feed, license usage, users, and system diagnostics — with AI-powered recommendations through Claude.

**Zero dependencies** — uses only the Python standard library, so it runs anywhere Python 3.6+ is installed with no `pip install` required.

## What it does

- Flags scans that ended in Error/Partial/Stopped
- Detects hosts with authentication failures
- Monitors license usage against thresholds
- Identifies scanners not in a working state
- Finds scan zones with no assigned scanners
- Checks plugin/feed freshness
- Surfaces stale and locked user accounts
- Computes an overall health score (0–100) with trend tracking
- Optionally sends email alerts on critical issues

## How it works

The tool talks directly to the SC REST API using Python's standard library (`urllib`). It stores timestamped JSON snapshots for historical comparison and optionally sends findings to Claude for AI-powered analysis. An interactive web UI (`sc_health_web.py`) provides safe one-click fixes for low-risk issues like triggering feed updates, re-launching failed scans, and assigning scanners to empty zones.
