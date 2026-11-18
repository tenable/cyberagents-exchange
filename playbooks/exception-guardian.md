---
last_reviewed: 2026-11-04
playbook_type: "standard"
name: "Exception Guardian"
author: "Alien0ne"
github_url: "https://github.com/Alien0ne/exception-guardian"
description: "Re-grades every Tenable risk exception against today's CISA KEV, EPSS and asset exposure, then writes Sigma detections, SIEM queries, a hunt brief and a human-gated approval plan for the ones that should be revoked."
license: "MIT"
tier: "contributed"
tags: ["risk-exceptions", "accept-risk", "recast-rules", "cisa-kev", "epss", "sigma", "threat-hunting", "human-in-the-loop", "claude-code"]
domains: ["vulnerability-management", "security-operations"]
integrations: ["Tenable", "Splunk", "Microsoft Sentinel"]
agents_used:
  - name: "Exception Guardian CLI"
    role: "Reads exceptions, grades each REVOKE, REVIEW or OK from KEV, EPSS and exposure, converts and tests Sigma rules, writes the approval plan. All grades come from tested code."
    type: "github"
    ref: "https://github.com/Alien0ne/exception-guardian"
  - name: "Claude Code"
    role: "Runs the CLI, explains each trigger's then-vs-now evidence, and drafts Sigma rules where SigmaHQ leaves a gap (no rule, no query for a SIEM, or no rule that catches the attack)."
    type: "info"
  - name: "SOC-Hunter"
    role: "Runs the generated hunt briefs over the window each revoked exception was hiding the exposure."
    type: "exchange"
    ref: "skills/soc-hunter"
  - name: "Human approver"
    role: "Confirms each Tenable VM rule disable, one at a time, in their own terminal."
    type: "info"
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T17:47:03Z
works_with_tenable_hexa_mcp: false
---

Exception Guardian is a Claude Code playbook and CLI that re-checks risk exceptions that were decided once and
never revisited.

**Run it:** `/exception-guardian` in Claude Code, or `exception-guardian demo` for the whole flow offline on sample
data.

## At a glance

| On the demo data | |
|---|---|
| Exceptions re-graded | 13 (made-up exceptions on real CVEs, real CISA KEV and FIRST EPSS values) |
| To revoke | 6, each with then-vs-now evidence and its source |
| Detections tested | 12 (5 distinct rules, some shared by several exceptions), on labelled sample logs |
| SIEM queries written | 32 (Splunk, Microsoft Sentinel, Defender XDR) |
| Time | under a second, offline |

On a real Tenable lab (4 Nov 2026), a fresh clone read 324 exceptions, graded 7 REVOKE, 316 REVIEW and 1 OK,
and wrote 25 tested rules (6 drafted by Claude, each catching its attack samples with no false alarm). Nothing
in Tenable was changed.

Why it matters, on public data: of the CVEs CISA added to KEV in the year to 2 Nov 2026 that already had an EPSS
score 90 days earlier, 56% were below 0.1. That is the kind of score an exception is accepted on.

## What it does

Find: reads Tenable VM accept/recast rules and scan exclusions, Tenable Security Center accept/recast risks, and
any scanner's CSV/JSON export, and grades each REVOKE, REVIEW or OK with then-vs-now evidence. Guard: for each
REVOKE gathers SigmaHQ or Claude-drafted Sigma rules, converts them to Splunk, Microsoft Sentinel and Microsoft
Defender queries, tests them on labelled sample logs and writes a hunt brief. Approve: writes an approval plan
and ticket text; an opt-in apply mode disables confirmed Tenable VM rules only after a human confirms each one.

## How it works

The grading is plain, tested code, so the same input always gets the same grade. An exception is REVOKE when one
of its CVEs is in CISA KEV or has an EPSS of 0.5 or more, or an asset it covers is internet-facing, on a Tenable
One attack path or critical. It is REVIEW when it is stale or contradicts itself: EPSS rose since acceptance, no
expiry, over a year old, expired but still on, or a justification that says "internal" for an exposed asset.
Every trigger shows what was true when the exception was accepted, what is true now, and the source.

Claude runs the CLI, explains that evidence, and drafts a Sigma rule where the 281 bundled SigmaHQ rules leave a
gap: no rule for the CVE, no query for one of the SIEMs, or no rule that catches the attack samples. The CLI validates each rule, tests it on labelled sample logs and converts it to Splunk,
Sentinel and Defender queries. Nothing in Tenable changes unless a person runs apply mode in their own terminal
and confirms each rule; a Claude Code hook blocks Claude from running it.

When a company does not tag what faces the internet, it can name its own tags, ranges or a host list, or let
Claude propose exposure from passive sources (public DNS, existing internet-scan records). The CLI re-checks every
claim before it counts. Every outbound call is listed in the README. `exception-guardian demo` runs all of it
offline on sample data in under a second.

## Safety

- **A person decides.** Grades and drafts are advice. Nothing in Tenable changes unless a person runs apply mode in
  their own terminal and confirms each rule; it re-reads the live rule first and verifies the change after.
- **Read-only by default.** Find and guard only read from Tenable. Keys come from the environment or a git-ignored
  `.env` that Claude Code hooks stop Claude from reading or printing.
- **Checked, not trusted.** Grades come from tested code, not the model. Claude's exposure claims are re-checked
  before they count, and every rule is tested before its queries are shown. A red team of 21 attacks on the
  guardrails, including 14 prompt injections hidden in the data, ended with 0 breaches.
