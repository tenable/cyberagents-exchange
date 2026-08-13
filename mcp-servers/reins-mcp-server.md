---
last_reviewed: 2026-08-13
name: "Reins MCP Server"
author: "amcdonnell-dot"
github_url: "https://github.com/amcdonnell-dot/reins"
description: "Audits Claude Code standing permission grants, scores each grant's prompt-injection blast radius, and generates deny-rule guardrails — local, read-only by default, zero network egress."
license: "MIT"
tier: "contributed"
tags: ["ai-agent-security", "permissions", "claude-code", "prompt-injection", "least-privilege", "governance", "python"]
integrations: ["Anthropic"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T13:58:00Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop"]
tools_exposed:
  - name: "reins_audit"
    description: "Audit standing permission grants across Claude Code settings sources, classified into 12 risk categories with redacted evidence"
  - name: "reins_explain"
    description: "Deep-dive on a single grant: what it permits, why it was flagged, and remediation options"
  - name: "reins_blast_radius"
    description: "Rank grants by worst-case prompt-injection blast radius (credential access, exfiltration, destruction, persistence, code integrity, privilege escalation)"
  - name: "reins_generate_policy"
    description: "Generate permissions.deny rules, PreToolUse hook scripts, and a managed-settings baseline from findings (dry — never writes)"
  - name: "reins_snapshot"
    description: "Save the current grant set as a baseline for drift detection"
  - name: "reins_drift"
    description: "Diff live grants against the saved baseline; newly added grants are fully classified and scored"
  - name: "reins_revoke"
    description: "Remove selected allow rules by audit-issued rule id — confirmation-gated, timestamped backups, atomic writes, read-only sources refused"
resources_exposed: []
prompts_exposed: []
---

Every time a developer clicks "always allow," Claude Code writes a standing permission into settings files that are almost never re-read. Those allowlists accumulate embedded credentials, destructive wildcards, credential-store reads, and unrestricted push/publish rights. Reins audits that surface before a prompt-injected agent session gets to use it.

## What it does

Reins classifies every standing permission grant across Claude Code's settings sources into 12 risk categories, using shell-aware tokenization (`shlex`) rather than regex-only matching so obfuscated or compound commands still classify correctly. Every non-safe finding gets a blast-radius score answering one question: if a prompt-injected agent fired this grant right now, what happens with no human in the loop? Findings convert directly into enforceable guardrails: `permissions.deny` rules, `PreToolUse` hook scripts, and an org-distributable `managed-settings.json` baseline. A snapshot/diff mechanism means a re-audit tells you exactly which grants appeared since your last known-good baseline.

## How it works

The classification engine is pure stdlib Python with no I/O beyond the files it's told to read or write, so it's fully unit-testable independent of the MCP transport. Detectors are data: a table of regex patterns per risk category, so contributors add coverage without touching pipeline code. Blast-radius scoring is deterministic (severity × breadth × reach, no LLM in the scoring path) and every string a tool returns passes through a single redaction boundary before it leaves the process — known secret shapes and high-entropy tokens are replaced with a stable fingerprint so the same secret is recognizable across findings without the value ever appearing. Writes are confirm-gated: `reins_revoke` requires an explicit `confirm: true`, re-verifies each targeted rule is still present before touching anything, writes a timestamped backup, and performs an atomic `os.replace`. Removal is non-destructive — Claude Code simply re-prompts the next time the permission is needed. The server is stdio-only with zero network egress, enforced by an automated socket-blocking test across the full suite.
