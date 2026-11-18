---
last_reviewed: 2026-10-07
name: "Repository Risk Simulator"
author: "bikashshah15"
github_url: "https://github.com/bikashshah15/repo-risk-simulator"
description: "Maps GitHub dependencies to OSV advisories and renders evidence-linked risk scenarios in an offline HTML report."
license: "MIT"
tier: "contributed"
tags: ["sbom", "dependency-analysis", "osv", "supply-chain", "vulnerability-triage", "spdx"]
domains: ["application-security", "vulnerability-management"]
integrations: ["GitHub", "Google OSV"]
date_added: 2026-10-06
contribution_agreement_date: 2026-10-06T17:27:25Z
compatible_platforms: ["Claude Code"]
invocation: "/repo-risk-simulator"
---

Dependency triage usually stops at a list of advisories matched to package versions, which
leaves the hardest question unanswered: does any of this matter for *this* application? This
skill keeps that question visible. It pairs a GitHub-hosted SBOM and Google OSV advisory data
with inspected source evidence, then models up to three hypothetical scenarios whose
prerequisites you can toggle — while refusing to claim that any vulnerability is reachable or
exploitable.

## What it does

Given a GitHub repository URL, it produces a self-contained HTML report that works offline
after generation:

- **Inventory** — starts GitHub's asynchronous SPDX export and downloads the result. No local
  scanner, no Docker service, no MCP server, and no separate model API key.
- **Advisory matching** — queries Google OSV for packages with supported, exactly-versioned
  purls (npm, PyPI, Maven, RubyGems, Go, crates.io, NuGet, Packagist, Hex, Pub), recording
  `matched`, `no_match`, `unsupported`, and `error` statuses separately so coverage gaps stay
  visible rather than reading as clean results.
- **Source evidence** — slices exact numbered line ranges from manifests, lockfiles, imports,
  call sites, and configuration, recording the source commit and a SHA-256 for each excerpt.
- **Assessment** — marks each finding `unknown`, `potentially_applicable`, or
  `ruled_out_under_evidence`, with cited evidence and per-finding limitations.
- **Scenarios** — up to three, each linked to a real finding, separating facts from assumptions
  and unknowns, stating its application evidence gap explicitly, and defining 1–8 prerequisite
  controls you can switch in the report.

Deliberate boundaries: it attempts no exploitation, includes no payloads or runnable exploit
commands, never executes code from the analyzed repository, and never modifies it. Results are
static assessments, not certified VEX.

## How it works

Python 3.10+ standard-library helpers handle collection, matching, validation, and rendering;
the current Claude session does the reasoning over the downloaded evidence. The pipeline runs
`preflight` → `collect` → `lookup` → `tree`/`source`/`evidence` → `init-analysis` →
`validate` → `render`, and every intermediate artifact is preserved next to the report.

Three outbound HTTPS destinations are used and documented in the repository: `api.github.com`,
`api.osv.dev`, and GitHub's SBOM download redirect host. `Authorization` is stripped on
cross-host redirects, signed download URLs are never stored, and an existing `GITHUB_TOKEN` or
`GH_TOKEN` is read from the environment only — never requested in chat or written into
artifacts.

The report embeds its own data, styles, and scripts, blocks network access with a Content
Security Policy, and renders untrusted text with `textContent`. Advisory URLs appear as text,
not as automatic requests. Scenario simulation is deterministic: any known contradiction blocks
the modeled path, otherwise any unknown yields unknown, otherwise prerequisites are satisfied.
A blocked result applies only to that scenario's explicit prerequisites and rules out nothing
else.

A labeled synthetic demo (`scripts/demo.py`) and two test suites ship with the skill for
offline verification.
