---
name: "KeenDreams Security Memory"
author: "Agent9AI"
github_url: "https://github.com/Agent9AI/keendreams-security"
description: "Shared memory for security agents where every fact cites its evidence and only a human in a browser can confirm one"
license: "MIT"
tier: "contributed"
tags:
  [
    "memory",
    "knowledge-graph",
    "human-in-the-loop",
    "evidence",
    "audit-trail",
    "prompt-injection",
    "cloudflare-workers",
  ]
domains: ["vulnerability-management", "ai-security"]
integrations: ["Tenable"]
date_added: 2026-09-17
contribution_agreement_date: 2026-09-22T16:37:44Z
works_with_tenable_hexa_mcp: false
transport: "http"
runtime: "node"
auth_method: "oauth2"
compatible_clients: ["Claude Code"]
tools_exposed:
  - name: "recall"
    description: "Answers a question in plain language by fusing BM25 keyword search with vector search, then filtering by trust and validity in SQL so an unconfirmed claim can never be returned as settled"
  - name: "find_facts"
    description: "Exact lookup by subject, relationship, object or status, with as_of to ask what the team believed on a past date rather than what it believes now"
  - name: "get_entity"
    description: "Everything currently known about one asset, vulnerability, identity or indicator, with its neighbours and a count of proposals still waiting for review"
  - name: "explore_graph"
    description: "Walks outward from an entity across confirmed relationships only, up to three hops, optionally limited to certain relationship types"
  - name: "fact_history"
    description: "The full timeline of one relationship: every version, what replaced it, who confirmed it and when. Built for answering an auditor rather than an agent"
  - name: "list_proposals"
    description: "Facts waiting for a human decision, each with a short quote of the evidence behind it and any flags raised during ingestion"
  - name: "record_episode"
    description: "Stores raw evidence as a quoted episode. Credential-shaped strings are redacted before storage and the count is recorded; instruction-like text is flagged for the reviewer"
  - name: "assert_fact"
    description: "Proposes that a subject relates to an object, citing the episode that proves it. The caller cannot set the resulting status, whatever their role"
  - name: "suggest_facts"
    description: "Asks the deployment's own model to read one episode and propose relationships. Every suggestion is validated like any other write, stored unconfirmed, and malformed ones are dropped and counted"
resources_exposed: []
prompts_exposed: []
---

A remote MCP server that gives security agents and the analysts working alongside them a
shared memory with a property most memory layers lack: nothing in it is believed because
something asserted it. Every fact points at the evidence it came from, and the only way a
proposal becomes trusted is a person confirming it in a browser. Administrators
may separately allowlist a specific automation identity and source to write
trusted facts directly.

## What it does

Security agents start every session cold. They re-read the same scan output, re-derive the
same conclusions, and re-ask questions a human already answered last month. The obvious fix,
letting the agent remember what it was told, creates a worse problem: scanner output, ticket
comments and pasted chat logs are attacker-reachable text, and an agent that treats its own
memory as ground truth will happily act on a sentence someone planted there.

This server stores memory as a graph of claims, each attached to quoted evidence, and keeps
the decision about what is true outside the agent entirely.

- **The caller cannot choose trust.** Ordinary MCP writes and model suggestions
  start as proposals. The status a write receives is decided by policy, never by
  a caller-supplied field. The single exception is an identity an
  administrator has explicitly allowlisted for one named source, which is a deliberate act
  with an audit entry attached.
- **Proposals are labelled, loudly.** Every fact carries a `confidenceLabel`, so an agent
  reading `UNCONFIRMED` in a tool result cannot quietly treat it as settled. `recall` and
  `find_facts` exclude unconfirmed facts by default.
- **Previous versions stay auditable.** A correction supersedes its predecessor and the older
  version stays readable. This is what makes `as_of` answerable: asking what the team
  believed before an incident returns what they actually believed, not today's view
  backdated.
- **Every decision is auditable.** Confirmations, rejections and rollbacks append to a
  hash-chained log that database triggers make append-only. A verifier reports the first row
  whose hash does not match.

The practical payoff for a vulnerability workflow is that an agent triaging a finding can
ask whether this host and CVE pair was already accepted as risk, marked a false positive, or
remediated, and get back the answer with who decided it, when, and when the acceptance
expires.

## How it works

Three decisions shape the implementation.

**One database per tenant, not one database with a tenant column.** Each client's memory
lives in its own Durable Object with its own SQLite database and its own vector namespace.
Cross-tenant leakage is not prevented by remembering to write a `WHERE` clause correctly in
every query; there is no shared table to leak from. A separate registry decides who may open
which client.

**Trust is a state machine, not a field.** A fact moves from proposed to trusted only
through a browser session backed by the deployer's own identity provider, and the MCP
surface has no tool that performs that transition. An agent holding a valid token for the
server still cannot confirm anything. Supersession applies only when a fact is trusted, so a
proposal cannot close out a fact the team relies on.

**Recall degrades rather than fails.** A question runs BM25 full-text search and vector
search in parallel, merges them with reciprocal rank fusion, and then applies the trust and
validity filter in SQL. If the vector index or the embedding model is unavailable, the
keyword leg still answers and the response says `search_mode: "keyword_only"`, because a
security tool that returns nothing during a partial outage teaches people to stop asking it.

Ingestion redacts credential-shaped strings before anything is stored and flags
instruction-like text for the reviewer. A flag never raises trust; it only draws a human's
attention to evidence that is trying to be an instruction.

The server runs entirely in the deployer's own Cloudflare account, using Workers, Durable
Objects with SQLite storage, Vectorize and Workers AI. It holds no vendor API key and no
shared client secret, sign-in goes through the deployer's own Cloudflare Access application,
and no component reports to the project authors. Authentication is OAuth 2.1 with PKCE and
dynamic client registration, so connecting a client involves approving a browser prompt
rather than copying a key.

A companion Claude Code skill in the repository connects this memory to Tenable's Hexa AI
MCP server: it pulls findings for a scoped query using an explicit allowlist of read tools,
checks each one against what the team already decided, and records the difference as
proposals for review. The allowlist is deliberate. Hexa exposes roughly ninety tools that
mix reads with writes, including ones that launch scans and notify ticket assignees, so the
skill names the tools it may call rather than letting a model choose.
