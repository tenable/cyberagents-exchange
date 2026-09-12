---
name: "Counterfactual Immune Forge"
author: "SweetKenneth"
github_url: "https://github.com/SweetKenneth/shpbl-immune-forge"
description: "Adjudicates candidate defensive changes against a sealed attack scenario: reproduction gate, blast-radius screen, same-scenario replay, mandatory regression gate and proven improvement, then seals the decision and every rejection as a verifiable Merkle evidence root."
license: "MIT"
tags: ["ai-agent-security", "detection-engineering", "regression-gate", "evidence", "change-control", "deterministic", "provenance", "mcp"]
tier: "contributed"
integrations: []
date_added: 2026-09-12
contribution_agreement_date: 2026-09-12T01:50:00Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "node"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor"]
tools_exposed:
  - name: "adjudicate_defensive_mutation"
    description: "Adjudicate one defensive-mutation episode from recorded observations and return sealed evidence plus a lineage entry; executes nothing and promotes nothing on its own"
  - name: "verify_episode_evidence"
    description: "Recompute an episode's Merkle evidence root and report whether the covered bytes are unmodified"
  - name: "export_immune_lineage_report"
    description: "Export the hash-linked lineage of every episode adjudicated in this session with verdict counts and an integrity flag"
  - name: "verify_immune_lineage"
    description: "Verify an exported lineage entry list link by link without trusting this session's state"
  - name: "describe_policy"
    description: "Return protocol versions, hash algorithm, default gate thresholds, input limits, rejection reasons and the declared absence of side effects"
  - name: "reset_state"
    description: "Clear this session's lineage; previously exported reports remain independently verifiable"
resources_exposed: []
prompts_exposed: []
---

When a guardrail, agent policy or detection rule is defeated, the patch that follows is usually accepted on trust. This server refuses to accept it on trust. It seals the attack scenario first, then makes every proposed change earn promotion against that same sealed scenario — and preserves the ones that failed.

## What it does

The operator's own harness runs the attack and the regression suite; the server enforces the gate chain over what the harness reports. An episode is `INCONCLUSIVE` unless the current defense demonstrably fails the sealed scenario. Each candidate change is screened for blast radius before it can earn replay credit, replayed against the identical sealed scenario, put through a mandatory protected-behaviour regression gate, and required to score finitely and strictly above the baseline by at least the configured margin. At most one candidate — the highest scoring one that cleared every gate — is promoted. Every rejected candidate is preserved with a machine-readable reason (`IMPACT_SCREEN_FAILED`, `SCENARIO_REPLAY_FAILED`, `REGRESSION_GATE_FAILED`, `NO_PROVEN_IMPROVEMENT`), which makes the "defeated the attack but broke legitimate traffic" case a first-class review artifact instead of a lost result. The decision is sealed as a SHA-256 Merkle evidence root and appended to a hash-linked lineage that can be exported and verified independently of the server's memory.

## How it works

A zero-dependency stdio MCP server (`node:crypto` only) written from a public behaviour specification. Missing evidence is a failed gate, never a pass: an absent replay, regression or fitness observation cannot clear a gate. The scenario is canonicalized with sorted keys and hashed before any candidate is considered, and the same frozen object is used for the baseline and every candidate replay, so goalposts cannot move mid-episode. Optional exploratory "dream" analysis runs only after sealing, receives only sealed evidence, and cannot alter the verdict or the root. The implementation performs no filesystem, network, process or environment access, and a conformance test asserts that boundary over the source. Thirty-four tests cover each gate, promotion selection among competing candidates, tamper detection on every covered field, lineage reordering and edits, malformed and cyclic input rejection, and the MCP handshake.

Known limitations, stated verbatim in the repository: it is not an autonomous security oracle, and a compromised evaluator — a rigged harness or a fitness function rewarding the wrong thing — yields sealed evidence of a bad decision. Sealing proves integrity, not wisdom. Session lineage is in memory; exported reports are the durable artifact.
