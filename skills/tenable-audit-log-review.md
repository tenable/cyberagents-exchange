---
name: "Tenable Audit Log Review"
author: "dpickenstenable"
github_url: "https://github.com/dpickenstenable/tenable-audit-log-review-agent"
description: "AI-powered daily audit log analyzer for Tenable that detects anomalies, classifies user behavior, and generates compliance-ready reports"
license: "MIT"
tier: "unreviewed"
tags: ["audit-log", "security-monitoring", "compliance", "anomaly-detection", "tenable", "soc2", "behavioral-analysis"]
integrations: ["Tenable"]
date_added: 2026-06-23
compatible_platforms: ["Claude Code"]
invocation: "/tenable-audit-log-review"
---

The **Tenable Audit Log Review** skill is an AI-powered security audit analyzer that performs comprehensive daily reviews of Tenable Vulnerability Management and Tenable One audit logs. It automatically identifies security-relevant activities, detects behavioral anomalies, and generates actionable intelligence reports for security operations teams.

## What it does

This skill analyzes Tenable audit logs across **8 activity categories**: authentication & access, user & permission management, scan activity, configuration changes, data access & exports, asset & tag management, API & integration activity, and deletion & cleanup events. It applies a **4-tier classification system** (Normal, Elevated, Aggressive, Suspicious) to every user action, helping security teams quickly identify concerning patterns that require investigation.

The skill employs **6 anomaly detection heuristics** including temporal analysis (after-hours activity), user behavior deviations (actions outside normal role), sequence patterns (attack chains), volume spikes, geographic anomalies (impossible travel), and correlation with external events. Each finding is enriched with business context, security impact assessment, and prioritized recommendations.

Reports are generated in multiple formats: **Markdown** for daily reviews, **HTML dashboards** with interactive visualizations and print-to-PDF capability, and **JSON** for SIEM integration. The skill provides compliance-ready audit trail highlights for SOC 2, ISO 27001, PCI DSS, and HIPAA frameworks, making it valuable for both security operations and compliance teams.

## How it works

The skill connects to Tenable via the **Tenable MCP Server** (recommended) or direct API authentication. It retrieves audit log events for a specified time window (default: last 24 hours) and performs systematic analysis:

1. **Activity Categorization** - Groups events into 8 operational categories and identifies which actions occurred
2. **Behavioral Classification** - Compares activity against learned baselines and classifies as Normal, Elevated, Aggressive, or Suspicious
3. **Anomaly Detection** - Runs 6 heuristics to identify temporal, behavioral, sequence, volume, geographic, and correlation anomalies
4. **Risk Assessment** - Evaluates business impact, security implications, and urgency for each finding
5. **Report Generation** - Creates comprehensive reports with executive summaries, detailed findings, user activity breakdowns, and prioritized recommendations

The skill maintains **baseline learning** over time, improving anomaly detection accuracy as it learns normal patterns for your environment. First-time runs establish baselines; subsequent runs compare against historical patterns to reduce false positives and catch true deviations.

**Key differentiator:** Unlike traditional SIEM correlation rules that flag individual suspicious events, this skill provides **holistic behavioral analysis** - understanding the context, user role, business justification, and environmental norms before classifying activity. This dramatically reduces alert fatigue while catching subtle attack chains that might otherwise go unnoticed.

Ideal for security teams who need daily visibility into Tenable administrative activity, compliance teams preparing for audits, and incident responders investigating suspicious behavior patterns. Can be scheduled to run automatically via cron, GitHub Actions, or CI/CD pipelines for continuous monitoring.
