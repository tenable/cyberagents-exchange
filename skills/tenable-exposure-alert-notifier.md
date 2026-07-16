---
name: "Tenable Exposure Alert Notifier"
author: "dpickenstenable"
github_url: "https://github.com/dpickenstenable/exposure-alert-notifier"
description: "Customizable email notification skill for Tenable VM with SMTPS security and professional HTML alert templates"
license: "MIT"
tier: "unreviewed"
tags: ["tenable", "vulnerability-management", "email-notifications", "alerts", "smtps", "crown-jewel", "cisa-kev"]
integrations: ["Tenable"]
date_added: 2026-06-23
compatible_platforms: ["Claude Code"]
invocation: "/exposure-alert-notifier"
---

The Exposure Alert Notifier delivers intelligent, customizable email notifications for Tenable Vulnerability Management findings. Built with security-first principles, it supports fully user-defined alert rules, SMTPS encryption, and professional HTML email templates.

## What it does

- **Customizable Alert Rules** — Define ANY alert condition using 30+ fields (severity, AES, ACR, VPR, CVE, hostname, IP, tags, OS, exploit availability, etc.) with 12 operators (equals, greater_than, contains, regex matches, etc.)
- **SMTPS Security** — All emails sent via encrypted SMTPS (ports 465 or 587 with STARTTLS). Plain SMTP is intentionally not supported.
- **Professional HTML Templates** — Pre-built templates for CISA KEV alerts, Crown Jewel assets (AES > 900), and infrastructure critical findings. Easily create custom templates.
- **Alert Fatigue Prevention** — Built-in throttling (hourly, daily, weekly) and deduplication windows prevent notification spam
- **Tag-Based Routing** — Dynamic recipient assignment using Tenable asset tags (e.g., automatically email the asset owner)
- **Scheduled Digests** — Support for cron-scheduled summary reports and executive briefings

## How it works

The skill connects to Tenable VM via the MCP Server or Direct API, retrieves vulnerability and asset data, then evaluates your user-defined rules from `rules.yaml`. When conditions match, it generates HTML emails from templates, performs variable substitution (asset name, AES score, plugin details, etc.), and sends via your configured SMTPS server. All sent notifications are tracked in `notification_history.json` to enforce throttling and prevent duplicate alerts.

Rules support complex multi-condition logic (all conditions must match), regex pattern matching for hostnames and IPs, network segment filtering, compliance-specific tags (PCI DSS, HIPAA), and scheduled execution for digest reports.
