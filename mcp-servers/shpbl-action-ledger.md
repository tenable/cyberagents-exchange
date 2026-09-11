---
name: "Agent Action Evidence Ledger"
author: "SweetKenneth"
github_url: "https://github.com/SweetKenneth/shpbl-action-ledger"
description: "Hash-linked, redaction-aware evidence ledger for agent actions: records proposals and executions, exports a self-contained range, and verifies it offline from its own bytes."
license: "MIT"
tier: "contributed"
tags: ["ai-agent-security", "audit", "evidence", "tamper-evident", "incident-response", "governance", "deterministic", "mcp"]
integrations: []
date_added: 2026-09-11
contribution_agreement_date: 2026-09-11T21:33:55Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "bun"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor"]
tools_exposed:
  - name: "record_action"
    description: "Record one agent action (proposal, execution, redaction or annotation) as the next entry in the hash-linked ledger"
  - name: "export_ledger"
    description: "Export a self-contained, verifiable range of the ledger"
  - name: "verify_ledger"
    description: "Verify an exported ledger document using only its own bytes; no live store is consulted"
  - name: "describe_policy"
    description: "Return the active redaction allowlist, hash algorithm, canonicalization and export format versions, clock-skew bound, size limits and anchoring policy"
resources_exposed: []
prompts_exposed: []
---

After an agent-driven change goes wrong, the reconstruction usually depends on chat logs and tool transcripts that nobody can prove were not edited. This server gives an agent workflow a purpose-built evidence trail instead: append-only, hash-linked, and verifiable by someone who was not there.

## What it does

Each recorded action — a proposal, an execution, a redaction or a later annotation — becomes an entry chained to the one before it. Any range of the ledger can be exported as a self-contained document, and that document can be verified from its own bytes alone, with no access to the original store. Redaction is a first-class recorded event rather than a deletion, so removing a sensitive value does not silently break the chain or erase the fact that something was removed. `describe_policy` publishes the exact rules in force: which fields the redaction allowlist keeps, the hash algorithm, the canonicalization and export format versions, the accepted clock-skew bound and the size limits.

## How it works

A zero-dependency stdio MCP server written from a public behaviour specification. Entries are canonicalized deterministically and hashed with SHA-256 via Web Crypto; verification is a pure function of the exported bytes, which is what makes third-party checking possible. Storage is a caller-provided sink, so the ledger can be held wherever the operator already keeps evidence. Local by default: no model call, no network egress, no telemetry. Known limitation stated plainly in the repository — a hash chain proves internal consistency and detects edits within what was recorded; it cannot prove that an action was recorded at all, so anchoring the chain externally is the operator's responsibility. Conformance tests cover the numbered specification properties and every documented failure mode.
