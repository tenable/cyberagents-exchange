---
name: "Exposure Case Builder"
author: "SpookyFox9"
github_url: "https://github.com/SpookyFox9/exposure-case-builder"
description: "Ranks Tenable VM findings into cases and engineer-ready fix packages, with Claude-written cited narratives and a human-recorded decision."
license: "MIT"
tier: "contributed"
tags: ["triage", "prioritization", "remediation", "mcp", "tenable-vm", "case-management"]
domains: ["vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-11-03
contribution_agreement_date: 2026-11-03T22:24:56Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Code"]
tools_exposed:
  - name: "fleet_summary"
    description: "Totals for the loaded export: hosts, active findings by severity, case and fix-package counts, CISA KEV count, data-quality notes."
  - name: "case_queue"
    description: "Ranked cases as two lists, single-vulnerability threats and patch backlogs, each row explaining why it ranks where it does."
  - name: "fix_queue"
    description: "Ranked fix packages (a product plus a kind of fix) with what each contains and how many distinct actions it spans. order=coverage lists them in a greedy, heuristic order by hosts newly brought to zero urgent findings; the score rank is unchanged."
  - name: "case_file"
    description: "One case: score breakdown, facts, the fix packages that address it, top vulnerabilities with CVEs, hosts, timeline, limitations and any recorded disposition."
  - name: "fix_package"
    description: "One fix package: Tenable's fix actions with what each clears, contained impact, hosts, CVEs and advisories, and the cases it relieves."
  - name: "findings"
    description: "The real finding records behind a case or package, paged, so a narrative can cite genuine finding ids."
  - name: "trend_diff"
    description: "Compare with an earlier saved export (set EXPOSURE_CASE_BASELINE): counts per category, host overlap, data-quality counters, or a page of finding ids. A finding missing from the later export is never reported as fixed."
  - name: "export"
    description: "Render a case or package as Markdown or CSV for a ticket; with write=true and confirm=true, save all formats to a fixed local directory."
  - name: "record_disposition"
    description: "Record the analyst's decision (assigned, risk-accepted, false-positive, needs-info) as one appended line in a local log; needs confirm=true."
resources_exposed: []
prompts_exposed: []
---

Turns a Tenable Vulnerability Management export into ranked **cases** (what is risky) and **fix packages** (what to do and what it clears), so an analyst sees the most important work first and engineers get what they need. A deterministic Python engine does the clustering, scoring and evidence collection; Claude writes the cited narrative from the tool results; the human analyst makes and records the decision.

## What it does

- Reads a saved Tenable VM export and builds two linked views of the same findings: **cases** for the security team (a score broken down into severity, exploitation signals including CISA KEV and VPR, breadth, size, age, unsupported software, recurrence and patch availability) and **fix packages** for engineers (Tenable's own solution text grouped by product and kind of fix).
- Returns single-vulnerability *threats* and patch *backlogs* as separate lists, so a large OS backlog cannot bury an exploited vulnerability.
- Offers a second, heuristic order for fix packages (`fix_queue` with `order=coverage`): greedy by hosts newly brought to zero urgent findings if every listed action in each package is applied. It is not the shortest plan, and the score order stays the default.
- With an earlier saved export configured (`EXPOSURE_CASE_BASELINE`), `trend_diff` reports what changed since: new, newly visible, fixed as recorded by Tenable, reopened, not seen, and severity changes, with host overlap beside every count. A finding missing from the later export is never reported as fixed.
- Exports each case or package as Markdown (tickets), CSV (complete host and action lists) and JSON. Tenable-supplied text is neutralized for Markdown, HTML and spreadsheet formulas.
- Output is evidence and facts, never a verdict, and nothing recommends action against a person. Every number traces to Tenable finding IDs that the `findings` tool returns.

## How it works

A stdio MCP server (`mcp==2.3.0`, Python 3.10+) wraps a standard-library engine. It reads an export saved by `scripts/fetch_tenable.py`, the only component that makes a network call. The server itself is read-only except two local writes, each needing `confirm=true`: export files in a fixed directory and an append-only disposition log. No tool accepts a file path or changes Tenable or any other system.

**Outbound calls** (all from the fetch script, to `https://cloud.tenable.com` only): `POST /vulns/export` (creates an export job on Tenable's side, the only state change), `GET /vulns/export/{uuid}/status`, `GET /vulns/export/{uuid}/chunks/{n}`, and `GET /workbenches/vulnerabilities?date_range=90`. Every request sends Tenable's standard `User-Agent: Integration/1.0 (VENDOR; PRODUCT; Build/VERSION)` header. API keys come from environment variables only.

## Limitations

The ranking weights are a documented judgment, not a validated model. Fix grouping is heuristic (product from the first CPE, fix type from the solution's opening verb), and the tool does not claim that one update supersedes another because Tenable's data does not say so. The coverage order is a heuristic whose steps can span many distinct actions, and the trend diff has not been tested against two real pulls (Tenable's finding-id stability between pulls is undocumented). `confirm=true` is a convention enforced by the client's tool-permission prompt, so keep the two write tools on "ask". Tested on one tenant (160 hosts, 19,437 findings) on Windows 11, with the suite passing on Python 3.10 and 3.14 and CI on Linux. The full list is in the repository's `docs/LIMITATIONS.md`.
