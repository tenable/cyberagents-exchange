---
name: "Tenable One API Claude Skill"
author: "ethodder"
github_url: "https://github.com/ethodder/tenable-one-skill"
description: "A token-optimized knowledge pack that makes AI coding assistants expert in the Tenable One exposure management platform API."
license: "MIT"
tier: "unreviewed"
tags: ["tenable", "vulnerability-management", "pytenable", "api-skill", "exposure-management", "security-automation"]
integrations: ["Tenable"]
date_added: 2026-06-17
compatible_platforms: ["Claude Code"]
invocation: "/tenable-one-api-claude-skill"
---

A structured knowledge pack that makes Claude (and other AI coding assistants) an expert in the Tenable One exposure management platform. Instead of pasting raw API docs into chat, this skill gives the AI pre-distilled platform knowledge, correct authentication patterns, and production-ready code recipes - reducing prompt token overhead by 80%+ and getting code right on the first try.

## What it does

- Covers all major Tenable One modules: Vulnerability Management, Web App Scanning, Exposure Management, Attack Path Analysis, Identity Exposure, OT Security, Security Center, Attack Surface Management, and more.
- Provides opinionated best practices (use exports not workbenches, VPR over CVSS, Tags not Target Groups, never hardcode keys).
- Includes ready-to-use pyTenable SDK patterns for chunked async exports, SLA compliance reporting, CSV generation, auto-tagging by subnet, and Jira/ServiceNow/SIEM integration.
- Documents 100+ API endpoints, exact JSON response schemas, and correct authentication with the `X-ApiKeys` header format.
- Handles V1 and V2 asset export differences, rate limit retry strategies, and RBAC boundary awareness.

## How it works

The skill is a pure-text knowledge pack (no scripts to run). Place the `tenable-one-api-claude-skill/` directory in your project root and your AI coding assistant automatically reads the `SKILL.md` frontmatter for platform context. The core skill file contains platform rules, authentication patterns, module-specific API workflows, and inline code recipes. Reference files provide endpoint tables and response schemas for deep lookups. The entire skill compresses Tenable's 4.5 MB API specification into under 11,000 tokens of active context.
