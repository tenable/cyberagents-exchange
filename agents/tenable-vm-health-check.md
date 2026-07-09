---
name: "Tenable VM Health Check"
author: "d-zito"
github_url: "https://github.com/d-zito/tenable-healthcheck-agent"
description: "Monitor Tenable VM scanning health, credentials, agents, scanners, and license usage with AI-powered insights."
license: "MIT"
type: "tool"
tier: "unreviewed"
tags: ["health-monitoring", "vulnerability-management", "tenable-vm", "credential-scanning", "agent-monitoring", "license-tracking", "cli-tool"]
framework: "Python CLI (pytenable SDK)"
integrations: ["Tenable", "Anthropic"]
date_added: 2026-06-15
---

An open-source Python CLI tool that tracks Tenable Vulnerability Management health metrics over time and provides AI-powered recommendations through Claude.

## What it does

Tenable VM Health Check monitors critical aspects of your Tenable environment:
- **Scan Health** — Tracks aborted/incomplete scans
- **Credential Scans** — Monitors percentage of successful credentialed scans
- **License Usage** — Alerts on significant changes in license consumption
- **Agent Status** — Flags agents offline for 14+ days
- **Scanner & Connector Health** — Monitors infrastructure status
- **User Management** — Tracks accounts, roles, and login activity
- **AI Analysis** — Claude-powered insights and recommendations

Each run compares against historical data to detect trends and anomalies.

## How it works

The tool uses the official pytenable SDK to collect data from the Tenable VM API, stores historical snapshots for comparison, and sends analysis to Claude for AI-powered insights. Generates both console and HTML reports with color-coded alerts and actionable recommendations.

Supports configuration via JSON file or environment variables, making it suitable for both development and production/CI environments.
