---
name: "SecHelix"
author: "omarmohelal"
github_url: "https://github.com/omarmohelal/SecHelix"
description: "Evidence-first application-security review skill that sends every candidate finding to an independent verifier whose job is to disprove it before it is reported."
license: "Apache-2.0"
tier: "contributed"
tags: ["appsec", "secure-code-review", "authorization", "bola", "idor", "business-logic", "false-positive-reduction", "supply-chain", "ai-security", "devsecops"]
integrations: ["Anthropic"]
date_added: 2026-09-09
contribution_agreement_date: 2026-09-09T00:00:00Z
last_reviewed: 2026-09-10
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code", "Codex", "Gemini CLI", "GitHub Copilot"]
invocation: "sechelix"
---

Most review tooling optimises for finding more. The expensive failure in
application security is the opposite one: a queue of confident findings that
nobody can act on, because a third of them are wrong and there is no cheap way
to tell which third. SecHelix is built around that asymmetry.

## What it does

SecHelix reviews a codebase, pull request, API, cloud configuration or
agent/MCP integration you own or are explicitly authorized to test, and returns
findings that carry their own evidence — plus an explicit list of the candidates
it *refuted*, and why.

The refuted list is the point. A review that reports six issues and shows the
eleven it disproved is a different artifact from one that reports six and stays
silent about its own uncertainty.

Coverage emphasis is the classes that static pattern matching handles worst:
object and function authorization (BOLA, IDOR, BFLA), tenant isolation,
business-logic and entitlement abuse, payment and ledger invariants, race
conditions and idempotency, secret handling, SSRF and outbound-fetch
boundaries, supply chain, and the prompt/tool/authorization boundaries of AI
agents and MCP servers.

## How it works

Scope and mode are fixed first. Execution is one of `STATIC`, `LOCAL`,
`STAGING`, `PRODUCTION_SAFE`, or `UNTRUSTED_REPO` — the last treats repository
content as data and never as control instructions, so a `CLAUDE.md` or
`AGENTS.md` in the reviewed repository cannot redirect the review of itself.

The workflow then maps the attack surface and trust boundaries, resolves which
checks actually apply, and runs specialist review lanes in parallel. Every lane
produces *candidates* — never findings. Candidates go to an independent
verifier that reconstructs the claim from the code without assuming it is
correct, and reports `VERIFIED`, `REFUTED`, `UNPROVEN` or `BLOCKED`.

Three properties make the output usable rather than merely long:

**Missing evidence is not absence.** Applicability resolves to `APPLICABLE`,
`NOT_APPLICABLE`, `UNKNOWN` or `BLOCKED`. A check that could not run is
recorded as one that could not run.

**High and Critical findings require regression proof.** A fix is not complete
because the code changed. It is complete when a test that failed before the fix
passes after it, and the original finding no longer reproduces.

**The release gate is fail-closed.** It returns `PASS`,
`PASS_WITH_KNOWN_RISK`, `BLOCKED` or `INCOMPLETE`. A run whose lanes were
blocked returns `INCOMPLETE` — never a clean `PASS`. Silence is never rendered
as safety.

## Prerequisites and limitations

The skill is the product and runs on the agent alone. An optional Python
runtime (`pipx install sechelix`) adds stored runs, a coverage ledger of what
previous runs did *not* examine, replayable evidence, SARIF/HTML/Markdown
reports, CI exit codes, and a read-only MCP adapter with no shell tool and
path arguments confined to a configured root.

Limitations, stated plainly: SecHelix reasons over code and configuration and
inherits the judgment limits of the model driving it. It is not a substitute
for a penetration test, and it makes no measured detection-rate claim — the
public benchmark position is `NOT_MEASURED`, deliberately, rather than a
flattering number produced by grading its own homework. It is for systems you
own or are authorized to assess, and it carries no exploitation, lateral
movement, or exfiltration capability.
