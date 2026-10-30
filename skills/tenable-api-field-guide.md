---
last_reviewed: 2026-10-29
name: "Tenable API Field Guide"
author: "Lance Duvall"
github_url: "https://github.com/lanz/tenable-api-field-guide"
description: "An agent skill that makes AI coding assistants write correct Tenable API and pyTenable code: export defaults that silently drop data, per-product auth headers and paging, 409/429 handling, concurrency limits, pyTenable traps, Security Center quirks, and the Nessus scan API license restriction, checked against the public docs, live API behavior and the pyTenable source."
license: "MIT"
tier: "contributed"
tags: ["tenable", "tenable-api", "pytenable", "integrations", "exports", "developer-tools", "rate-limiting", "security-center", "nessus"]
domains: ["platform-operations"]
integrations: ["Tenable"]
date_added: 2026-10-26
contribution_agreement_date: 2026-10-26T20:45:33Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code", "Codex", "Cursor", "GitHub Copilot", "Gemini CLI"]
invocation: "/tenable-api-field-guide"
---

Code that an AI assistant writes against Tenable's APIs usually looks right and fails
quietly. A vulnerability export with no time filter returns only the last 30 days. One with
no `state` never includes fixed findings. A polling loop that waits for `FINISHED` hangs
forever if the job is cancelled. Retrying a `409` re-submits an export that's already
running. pyTenable adds traps of its own: a misspelled credential argument produces an
unauthenticated client, not an error, and its export defaults differ from the API's. Tenable
API Field Guide gives the assistant rules checked against developer.tenable.com, live API
behavior and the pyTenable source, so it gets these right the first time.

## What it does

- Covers authentication and clients for each product it documents: the header format,
  base URL, pyTenable constructor and environment variable prefix, plus SSL and timeout
  defaults.
- Covers VM exports end to end: lifecycle and status values, default windows, filter syntax
  (including tag formats that differ by export), chunk handling and expiry, duplicate handling,
  joining findings to assets, and reconciling deleted assets.
- Documents rate limiting and `retry-after`, the concurrency caps (10 exports, 3 detail
  calls, 25 active scans), pyTenable's retry behavior, and User-Agent identification.
- Gives the pagination scheme for each API, plus the record caps that force you onto
  exports.
- Covers Security Center: errors that arrive inside HTTP 200, analysis paging, filter
  tuples, and the automatic WAS exclusion.
- Covers Nessus: the scan API is a licensed feature that Professional and Expert commonly
  lack, so the assistant checks `license.features.scan_api` before writing scan automation
  instead of producing code that fails with "API is not available". It also covers the
  response quirks that break parsers (`null` lists, scores sent as strings, text
  timestamps on imported scans), single-use export downloads, credentials mixed into scan
  details, creating and launching scans, and pyTenable's Nessus quirks.
- Includes a troubleshooting table by symptom and working recipes. Where live API behavior
  differs from the published reference, the guide says which one it follows.

## How it works

It's a single folder in the Agent Skills format: a `SKILL.md` with the rules that prevent
most bugs and a routing table, plus focused reference files the assistant loads only when
the task needs them. It runs no code and makes no network requests. The same folder loads
in Claude Code, Codex, Cursor, GitHub Copilot and Gemini CLI, and the README gives the
install path for each. The rules were checked against the published API reference, live
API behavior and pyTenable 26.10.1. The VM recipes were run against live Tenable VM
containers (the Security Center recipe is syntax-checked), and the Nessus rules against
live Nessus Manager, Professional and Expert scanners. The tests check the skill's
structure for each platform and that every example compiles.
