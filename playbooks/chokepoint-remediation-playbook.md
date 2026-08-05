---
name: "Chokepoint Remediation Playbook"
author: "tarhou"
github_url: "https://github.com/tarhou/chokepoint-finder-playbook"
description: "An eight-stage remediation chain from thousands of findings to a handful of proven fixes, with a human checkpoint before every external mutation and a runner that enforces the contract offline."
license: "MIT"
tags: ["vuln-management", "exposure-management", "remediation", "change-management", "human-in-the-loop", "verification", "claude-code"]
tier: "contributed"
integrations: ["AWS", "Tenable"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T02:04:27Z
works_with_tenable_hexa_mcp: false
playbook_type: "standard"
agents_used:
  - name: "Chokepoint Finder"
    role: "Carries the loop end to end: collapses findings into shared fixes, ranks them, gates unsafe targets, and holds no external write tools."
    type: "github"
    ref: "https://github.com/tarhou/chokepoint-finder"
  - name: "Chokepoint Finder MCP Server"
    role: "Provides the typed tools the chain binds to: ingest, rank, pre-flight, plan hashing, execution accounting and verification."
    type: "github"
    ref: "https://github.com/tarhou/chokepoint-finder-mcp"
  - name: "Chokepoint Finder Skill"
    role: "The portable, dependency-free form of the same ranking method, for operators who run the chain without the MCP server."
    type: "github"
    ref: "https://github.com/tarhou/chokepoint-finder-skill"
  - name: "Tenable MCP Server"
    role: "Read-only collection of findings and asset context, and the authoritative re-scan the verification stage diffs against."
    type: "exchange"
    ref: "tenable-mcp-server"
  - name: "AWS MCP Server (Agent Toolkit for AWS)"
    role: "Read-only cloud posture collection, and the execution path for approved cloud changes under the operator's own credentials."
    type: "info"
---

The operating chain that turns the Chokepoint Finder method into something a team can
actually run on a Monday: eight stages with explicit owners, explicit handoffs, and a
human checkpoint in the middle that cannot be skipped.

## What it does

Gather read-only, collapse findings into the fixes they share, rank by marginal risk,
gate on evidence, **stop for a human**, execute through the operator's own tools in
per-site waves, hand intel to SOC and threat hunt, then prove the risk moved with a
re-scan before the change record closes — and repeat on a schedule.

Every external mutation along the way takes its own explicit approval. Not just the
infrastructure change: opening the change ticket, notifying a SOC or opening a hunt
ticket, and launching the verification scan each count as mutations and each require
their own yes. The playbook holds no credentials, no collectors, and no write path of
its own.

## How it works

The chain is defined once, machine-readably, in `stages.yaml`: each stage's capability,
who provides it, whether that provider is read-only or write, and where approvals bind.
The prose playbook and the runnable slash command are both **validated against that
file** rather than trusted to stay in sync — the validator asserts that both documents
contain exactly the stages of `stages.yaml` in order under the same titles, that every
named provider exists in the component registry and is classified read-only or write,
that every referenced MCP tool is one the server actually ships, and that every mutating
stage declares human approval with matching approval language in the text. The test
suite proves those checks have teeth by injecting drift — a dropped stage, a renamed
tool, a stripped approval — and asserting validation fails.

A bundled offline state-machine runner enforces the receipt contract without calling any
live system. It refuses skipped stages, pre-gate or altered manifests, widened target
sets, replayed or stale or mismatched approvals, later waves before proof, mismatched
source scopes, rescan-digest drift, and simulated evidence offered as closure. Refused
transitions are transactional: they consume no receipt and leave no partial state.

Stage owners are deliberately swappable — a different scanner, ticketing system or patch
platform slots in — because the interfaces are expressed as capabilities rather than
products. The repository is explicit about the boundary of what the runner can prove: it
validates receipt structure and consistency, but it does not authenticate the claimed
human identity and cannot attest that a dishonest connected tool behaved as its receipt
says. Approval identity is therefore only as strong as the system that issues and
transports the operator receipt.
