---
name: "Cross-Agent Handoff Attestor"
author: "SweetKenneth"
github_url: "https://github.com/SweetKenneth/shpbl-handoff-attestor"
description: "Signs and verifies delegation between agents so authority can only narrow: scope containment, constraint compatibility, freshness, replay refusal and parent-chain continuity."
license: "MIT"
tier: "contributed"
tags: ["ai-agent-security", "least-privilege", "delegation", "multi-agent", "authorization", "attestation", "deterministic", "mcp"]
integrations: []
date_added: 2026-09-11
contribution_agreement_date: 2026-09-11T21:33:55Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "bun"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor"]
tools_exposed:
  - name: "issue_handoff"
    description: "Issue a signed cross-agent handoff attestation with scope, constraints and optional parent chain"
  - name: "verify_handoff"
    description: "Verify a handoff attestation's signature, freshness, replay, scope narrowing, constraint compatibility and chain continuity"
  - name: "check_scope"
    description: "Answer whether a child scope is a subset of a parent scope under the specification's containment rule"
  - name: "describe_keys"
    description: "Return the registered key adapter's algorithm identifier and accepted key references; never returns key material"
resources_exposed: []
prompts_exposed: []
---

In multi-agent workflows, authority spreads by convention: one agent asks another to "finish the remediation," and the second agent ends up acting with broader reach than the first was ever granted. This server makes delegation an explicit, signed, checkable artifact whose permissions can only shrink.

## What it does

An issuing agent mints a handoff attestation naming the receiving agent, the resources in scope, the constraints that travel with it, an expiry and an optional parent attestation. Verification is where the guarantees live: the signature must hold, the attestation must be fresh and not previously used, the child scope must be contained by the parent under a documented containment rule, the constraints must be compatible with the parent's, and the parent chain must be continuous back to its root. Widening is refused at issuance and again at verification, so an attempt to gain reach fails closed instead of proceeding quietly. `check_scope` answers the containment question directly, which makes the rule testable rather than folklore.

## How it works

A zero-dependency stdio MCP server written from a public behaviour specification. Resource patterns are compared with exact literal matching plus a single trailing-`*` prefix form, and the specification and README state precisely what is and is not contained — including the cases that surprise people, such as a double separator not matching a prefix pattern. Signing is delegated to a caller-registered key adapter, so key material never enters the server's records and `describe_keys` returns algorithm identifiers only. Chain depth is bounded, replay is tracked, and clock skew is bounded explicitly. No model call and no network egress. Conformance tests cover the numbered specification properties, the containment boundary cases and the depth limit.
