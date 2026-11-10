---
name: "Counterfactual Immune Forge"
author: "SweetKenneth"
github_url: "https://github.com/SweetKenneth/shpbl-immune-forge"
description: "Adjudicates reported defensive-change observations through reproduction, impact, same-scenario, regression and improvement gates, then seals the decision record and every rejection as a recomputable Merkle evidence root."
license: "MIT"
tags: ["ai-agent-security", "detection-engineering", "regression-gate", "evidence", "change-control", "deterministic", "provenance", "mcp"]
domains: ["ai-security", "security-operations"]
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
    description: "Adjudicate one defensive-mutation episode from recorded observations: impact screen, same-scenario replay, mandatory regression gates and positive fitness delta, then seal the decision as a Merkle evidence root. Executes nothing and promotes nothing on its own."
  - name: "verify_episode_evidence"
    description: "Recompute the Merkle evidence root of a sealed episode. Optionally compare it to an independently retained expected root; without one, verification proves internal CIF/0.3 semantic-and-hash consistency only."
  - name: "export_immune_lineage_report"
    description: "Export the hash-linked lineage of every episode adjudicated in this session, with verdict counts and an integrity flag."
  - name: "verify_immune_lineage"
    description: "Verify an exported lineage entry list link by link. Optionally compare the computed head to an independently retained expected head hash."
  - name: "describe_policy"
    description: "Return the protocol versions, hash algorithm, default gate thresholds, input limits, rejection reasons and the declared absence of side effects."
  - name: "reset_state"
    description: "Clear this session's lineage. Previously exported reports remain independently verifiable."
resources_exposed: []
prompts_exposed: []
---

When a guardrail, agent policy or detection rule is defeated, the patch that follows is usually accepted on trust. This server refuses to accept it on trust. It seals the attack scenario first, then makes every proposed change earn promotion against that same sealed scenario — and preserves cryptographic identity plus gate evidence for the ones that failed.

## What it does

The operator's own harness runs the attack and the regression suite; the server adjudicates the observations that harness supplies. An episode is `INCONCLUSIVE` unless the reported baseline replay is bound to the sealed scenario, reproduces the event and says the attack succeeded against the current defense; that gate cannot be disabled. Each candidate change is screened for blast radius before it can earn replay credit; its supplied replay must carry the same sealed scenario hash, and a missing or mismatched binding fails the replay gate. A candidate is rejected outright if its reported replay says the attack still succeeds; that gate also cannot be disabled. Survivors are put through a mandatory protected-behaviour regression gate. Only after the baseline attack is proven does fitness participate: survivors must score finitely and strictly above an explicit baseline fitness produced on the same evaluator-defined scale by at least the configured margin. Inconclusive baselines do not invoke or require fitness scoring. At most one candidate — the highest scoring one that cleared every gate — receives a `PROMOTED` verdict. Every rejected candidate's identity hashes and gate observations are preserved with a machine-readable reason (`IMPACT_SCREEN_FAILED`, `SCENARIO_REPLAY_FAILED`, `ATTACK_NOT_NEUTRALIZED`, `REGRESSION_GATE_FAILED`, `NO_PROVEN_IMPROVEMENT`). The decision record is sealed as a SHA-256 Merkle evidence root and appended to a hash-linked lineage. Verification can be anchored to an independently retained evidence root or lineage head; without such an anchor the episode verifier establishes CIF/0.3 semantic-and-hash consistency and the lineage verifier establishes CIF-LINEAGE/0.1 entry-semantic and chain-hash consistency, not historical authenticity. The server never executes a candidate or independently verifies that harness observations are truthful.

## How it works

A zero-runtime-dependency stdio MCP server (`node:crypto` only) written from a public behaviour specification. Missing evidence is a failed gate, never a pass: an absent replay, regression or fitness observation cannot clear a gate. The scenario is canonicalized with sorted keys and hashed before any candidate is considered, and one sealed scenario is bound to all observations in that episode. Optional exploratory "dream" analysis runs only after sealing, receives only sealed evidence, and cannot alter the verdict or the root. The source contains no filesystem, network, process-spawning or environment access; a static conformance test checks that declared boundary. The test suite covers each gate, adversarial promotion paths, replay identity, deep immutability, tamper detection, lineage mutation and reordering, malformed and cyclic input rejection, transport boundaries, and the MCP handshake.

Known limitations, stated verbatim in the repository: it is not an autonomous security oracle, and a compromised evaluator — a rigged harness or a fitness function rewarding the wrong thing — yields sealed evidence of a bad decision. Sealing proves integrity, not wisdom. Session lineage is in memory; exported reports are the durable artifact.
