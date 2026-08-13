---
last_reviewed: 2026-08-12
name: "Reins Audit Skill"
author: "amcdonnell-dot"
github_url: "https://github.com/amcdonnell-dot/reins-skill"
description: "Guided audit and cleanup of Claude Code standing permissions — works standalone, and drives the Reins MCP Server for deterministic classification and safe revocation when connected."
license: "MIT"
tier: "contributed"
tags: ["ai-agent-security", "permissions", "claude-code", "least-privilege", "remediation"]
integrations: ["Anthropic"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T14:05:02Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "/reins-audit"
---

Reins Audit turns a settings-file cleanup chore into a conversation. Run `/reins-audit`, or just ask "audit my Claude Code permissions," and it walks every standing grant it finds, tells you what each one actually permits, and only touches anything after you say so.

## What it does

The skill reads Claude Code's settings sources, classifies each standing permission grant into one of 12 risk categories, and groups the results by verdict: `remove`, `review`, or `keep`. Anything flagged gets a one-sentence blast-radius narrative — what a hijacked session could do with that grant, not just a risk label. If you ask for cleanup, it lists exactly which rules would be removed and waits for explicit confirmation before changing anything.

## How it works

Two modes, same taxonomy. Standalone, the skill classifies by reading its own bundled reference files (`references/taxonomy.md`, `references/remediation.md`, `references/policy-baseline.md`) and applying that logic by hand against the settings files it reads directly — no MCP server required. When the Reins MCP server is connected, the skill hands classification to it instead: the server's deterministic regex engine, secret redaction, and blast-radius scoring replace the manual pass, and confirmed revocations go through the server's `reins_revoke` tool, which re-verifies each rule is still present, backs up the file, and writes atomically. Either way, the skill never displays a secret's actual value and never modifies read-only sources (the Claude state file or managed settings) — it can only report what's there.
