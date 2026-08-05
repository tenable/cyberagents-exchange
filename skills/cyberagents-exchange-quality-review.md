---
name: "cyberagents-exchange-quality-review"
author: "Echo6Bravo"
github_url: "https://github.com/Echo6Bravo/cyberagents-exchange-quality-review"
description: "Adversarial pre-submission quality and security gate for cybersecurity agents, skills, and MCP servers — especially those bound for the CyberAgents Exchange. Hunts the failure classes that hurt a customer across 19 dimensions, reports findings as rejection gates, defects, and informational notes, and mirrors the live Exchange reviewer checklist so you clear review with fewer round-trips."
license: "MIT"
tier: "contributed"
tags: ["quality-assurance", "security-review", "pre-submission", "code-review", "static-analysis", "prompt-injection"]
integrations: ["Anthropic"]
date_added: 2026-08-04
contribution_agreement_date: 2026-08-04T02:23:11Z
last_reviewed: 2026-08-04
compatible_platforms: ["Claude Code"]
invocation: "/cyberagents-exchange-quality-review"
---

A Claude Code skill that runs an adversarial, proof-over-assertion quality and security review of a cybersecurity agent / skill / MCP server **before** you push it publicly or submit it to the CyberAgents Exchange. It turns "did I miss anything?" from a gut check into a repeatable checklist that finds the failure classes that actually hurt a customer — and it mirrors the Exchange's own reviewer checklist so you clear review with fewer round-trips.

> This is a community contribution authored by a Tenable employee. It is **not** an official, supported Tenable product, and passing it is **not** a guarantee of Exchange acceptance — the live Exchange checklist and `validator.py` are always authoritative. The skill fetches and defers to them at review time.

## What it does

Invoke it ("run a quality review on this repo" or `/cyberagents-exchange-quality-review`) and it works **19 dimensions**, ranked by customer impact, reporting each finding with a concrete reproduction and fix — then an explicit **verdict**: ready to submit, or the blocking items.

- **Core (1–12):** detection false-negatives; injection/XSS; messy-data robustness; scale; operational behavior (exit codes / retry / determinism); version portability & TLS; schema/contract drift; secrets (full git history + credential-at-rest); malicious/offensive self-check; undisclosed egress; tests & CI; docs.
- **LLM / AI-agent (13–18):** indirect prompt-injection; AI data handling (at-rest & vendor egress); LLM output grounding & non-determinism; token/cost & runaway-loop controls; access control & agent authority; supply-chain provenance. These were derived from analyzing the live Exchange agent repositories, most of which are LLM/MCP agents.
- **Generated artifacts (19):** for tools that *emit* something a human or CI later runs (remediation scripts, IaC, SQL, playbooks, config) — execution-scope correctness. The failure it catches is not an error but a *wrong success*: an artifact spanning more scope than its tooling can address in one invocation resolves identifiers against whichever scope the runner happens to be authenticated to, acting on the wrong account while the run reports success.
- Plus a **CyberAgents Exchange submission** section that mirrors the live contributing checklist (automated screening, listing requirements, listing↔repo congruence, and the outright-rejection gates).

## How findings are reported

Findings land in **three buckets, ordered by who decides and against what standard** — so a reviewer can read the first bucket and stop, while a contributor reads the rest as a fix list.

1. **Rejection gates** — pulled verbatim from the live Exchange checklist (committed secrets, weaponized behavior, no detectable license, undisclosed egress). Binary, with no severity: the checklist says a detected credential is "an immediate rejection," so there is no *how bad*. Any failure sets the verdict on its own.
2. **Defects** — Critical / High / Medium / Low, scored on consequence rather than effort to fix. Every severity must **cite its basis** (a checklist item, a CodeQL `security-severity` score, a scanner rule plus its own rating, or the stated rubric row), because an unsourced label is how a guess acquires the appearance of authority. A scanner's rating is evidence that may **raise but never lower** a finding — `bandit` rates a hardcoded password LOW, the exact class the Exchange rejects outright. A **CWE is optional, and is classification rather than severity**: cited where a real one fits, explicitly absent where none does, since a wrong-but-official-looking label misdirects triage worse than no label at all.
3. **Informational** — efficiency, cost, ergonomics, style. No severity and never blocking, so an "output is 70% boilerplate" note cannot read like a credential leak. Promoting one into Defects requires naming the consequence.

## How it works

Before reviewing, it runs a **coverage preflight** — checking which scanners are present and telling you up front which dimensions run in degraded mode — so the verdict is never trusted beyond what actually ran. For each dimension it then **runs a probe** (adversarial input, a container, a scanner) rather than reasoning about it, preferring proof over assertion. It leans on a standard toolkit where available — **gitleaks** (full-history secret scan), **ruff** + **bandit** (Python lint/SAST), **shellcheck**, **actionlint**, and **CodeQL** (as a GitHub Action) — and treats each as a CI gate that must stay green. For Exchange submissions it fetches the live `contributing_checklist.md` and `validator.py` and defers to them as the source of truth. It installs nothing without your approval and runs commands in your environment; treat its verdict as a strong pre-check, not a certification.
