---
name: "Tenable User Health"
author: "dstarks17"
github_url: "https://github.com/dstarks17/tenable-user-health"
description: "Audits Tenable user activity, authentication security, and maps findings to compliance frameworks"
license: "MIT"
tier: "contributed"
tags: ["tenable", "compliance", "user-management", "authentication", "audit", "security"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-07-08
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code"]
invocation: "/tenable-user-health"
---

A Claude Code skill that generates comprehensive user management and authentication security health reports from Tenable Vulnerability Management.

## What it does

- Audits user activity and inactivity patterns via the Tenable audit log
- Analyzes authentication methods (password, API key, SSO, MFA) and detects failed login attempts
- Assesses least privilege, separation of duties, and API key usage patterns
- Maps all findings to compliance frameworks including NIST 800-53, CIS Controls v8, ISO 27001, SOC 2, PCI DSS, and HIPAA

## How it works

The skill queries the Tenable audit log and platform configuration APIs (scan ownership, managed credentials) to build per-user authentication and access profiles. It then analyzes risk indicators — inactive accounts, shared credentials, missing MFA, over-privileged access — and produces a structured report with prioritized recommendations mapped to the user's chosen compliance framework.
