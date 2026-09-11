---
name: "Retrieval Context Provenance Auditor"
author: "SweetKenneth"
github_url: "https://github.com/SweetKenneth/shpbl-retrieval-auditor"
description: "Records payload-free provenance for every retrieval an agent uses, traces a decision back to its sources, ranks source influence with an explicit unexplained residual, and flags schema drift and untrustworthy sources."
license: "MIT"
tier: "contributed"
tags: ["ai-agent-security", "rag-security", "provenance", "data-poisoning", "audit", "supply-chain", "deterministic", "mcp"]
integrations: []
date_added: 2026-09-11
contribution_agreement_date: 2026-09-11T21:33:55Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "bun"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor"]
tools_exposed:
  - name: "index_sources"
    description: "Register retrievable sources with kind, first-seen time and optional declared schema"
  - name: "record_retrieval"
    description: "Record one decision's context assembly as digests plus declared metadata; never accepts document text"
  - name: "record_source_observation"
    description: "Record a corroboration, contradiction or failure observation about a source"
  - name: "trace_decision"
    description: "Traverse the source -> chunk -> transformation -> context -> decision lineage graph"
  - name: "score_source"
    description: "Advisory source trust, freshness and retirement recommendation with an explicit basis"
  - name: "report_influence"
    description: "Ranked influence attribution for a recorded decision, with a mandatory unexplained residual"
  - name: "check_retrieval_drift"
    description: "Compare an observed source schema against its declared baseline"
  - name: "describe_scoring_policy"
    description: "Return the trust policy identifier and its fixed public maxObservationStep"
  - name: "export_audit_records"
    description: "Export the payload-free hash-linked audit records produced so far"
resources_exposed: []
prompts_exposed: []
---

When a retrieval-augmented agent makes a decision an incident responder disagrees with, the hard question is not what the model said — it is which retrieved material produced that answer, where that material came from, and whether the source had already started behaving badly. Most stacks cannot answer any of the three after the fact.

## What it does

The server records the provenance of every context assembly as digests and declared metadata only — never document text — and keeps those records in a hash-linked chain so a later reader can verify the chain has not been edited. From those records it can trace a decision backwards through context, transformations, chunks and sources; rank which sources actually influenced a decision while always reporting the share it cannot explain; score a source's trust and freshness with an explicit basis and a bounded per-observation step; and flag when a source's schema has drifted away from the shape that was declared for it.

## How it works

The implementation is a zero-dependency stdio MCP server written from a public behaviour specification. Trust movement is bounded by a published `maxObservationStep`, so a single poisoned observation cannot swing a source's standing; the value is readable at runtime through `describe_scoring_policy`. Hashing is SHA-256 via Web Crypto. There is no model call, no network egress, and no filesystem read of source documents: callers hand in digests and metadata, which is what keeps the audit trail free of the payloads it describes. Trust scores are advisory inputs for a human, not automatic blocking decisions. The repository ships its conformance tests against the numbered properties of the public specification, plus a poisoned-source worked example.
