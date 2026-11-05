---
name: "Vuln Prioritizer"
author: "alkaf499"
github_url: "https://github.com/alkaf499/vuln-prioritizer"
description: "Turns a Tenable scan dump into a ranked, evidence-backed remediation worklist with defensible SLAs, using a deterministic two-layer model over CVSS, VPR, EPSS, CISA KEV and asset context."
license: "MIT"
tier: "contributed"
tags: ["vulnerability-management", "prioritization", "remediation", "sla", "kev", "epss", "vpr", "cvss", "asset-context", "deterministic", "navi", "tenable-vm"]
domains: ["vulnerability-management", "threat-intelligence"]
integrations: ["Anthropic", "NVD", "Rapid7", "Tenable"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T20:00:00Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "vuln-prioritizer"
---

## What it does

A Tenable tenant hands an analyst tens of thousands of findings and no answer to the only question
that matters: **what do I fix first, and by when can I defend that deadline in an audit?** Sorting by
CVSS measures theoretical severity, not whether a flaw is being exploited today, and not whether it
sits on an internet-facing firewall or a developer's laptop.

Vuln Prioritizer reads an existing Tenable inventory (a `navi.db` produced by
[navi](https://github.com/packetchaos/navi)), enriches it with open exploit intelligence, conditions
it on asset context from the CMDB, and emits a **tiered remediation worklist** where every row carries
its evidence, its tier, its SLA and its due date. On a 20,522-finding reference tenant it surfaced
**25 Tier 0 emergencies** — internet-exposed assets carrying actively exploited CVEs — plus 161 further
items due within 24 hours, and separated 9,399 scanner-informational artifacts out of the remediation
ranking altogether.

Alongside the worklist it writes an executive report (findings by tier, SLA compliance measured from
first-found, per-role breakdown, divergence highlights), a per-finding CSV with every resolved input
and its source, and a separate file of out-of-scope assets — nothing is silently dropped.

Two properties make it usable as the input to a patch process rather than as a one-off report:

- **It is deterministic.** The same inputs produce byte-identical output, including live-enriched runs
  replayed from a frozen intel cache. Every tier is a reproducible function of recorded values, so a
  disputed deadline can be reconstructed months later.
- **It is read-only against the tenant.** No tags, no ACR changes, no scans — verified by test. It
  works with a read-only API user.

## How it works

**Layer 1 — the vulnerability.** Impact resolves through a CVSS fallback chain (NVD → CNA →
unattributed → scan severity → `Low` + an explicit `IMPACT_MISSING` flag) so a missing score never
quietly becomes zero. Probability resolves from Tenable VPR, falling back to EPSS with banded
cutoffs, and **CISA KEV membership acts as a floor** — a CVE on KEV is forced to at least High
probability, applied last over any source. Both axes bin to a band and meet in a 4×4 matrix that
yields Tier 1 (24h) through Tier 4 (next patch cycle). A finding with no probability signal at all —
an end-of-life package, a configuration check — is scored on impact alone, **capped at Tier 3, never
uplifted, and flagged for re-evaluation**, which is what stops a CVE-less finding from manufacturing
a false emergency.

**Layer 2 — the asset.** Exposure, business criticality and environment are CMDB facts, not scanner
facts, so they resolve through a priority chain: Tenable One exposure classes → Tenable tags → a YAML
classification overlay exported from the CMDB → unknown-and-flagged. Exactly one ±1 tier shift
applies per asset: external exposure uplifts (Tier 0, ~12h emergency), non-critical production and
non-production downgrade, and only an explicit `in_scope: false` excludes. Deliberately there is no
"no-downgrade floor": a Patch-Tuesday wave of KEV'd criticals must not put an entire laptop fleet on
a 24-hour clock, and the single-shift limit means a KEV'd critical can never fall past Tier 3. That
is what makes the SLAs achievable and therefore defensible.

**Threat intelligence.** Exploit maturity comes from
[threat-intel-toolkit](https://github.com/kevinmhorvath/threat-intel-toolkit) — CISA KEV, Metasploit,
Exploit-DB and Nuclei from locally cached feeds by default, with optional per-CVE EPSS and GitHub PoC
aggregators. Lookups are gated to findings worth enriching and memoized per distinct CVE, so a CVE on
500 assets costs one fetch. Evidence text states exactly which sources were consulted, so a CVE found
in no feed never reads as a false "no public exploit found." A `vpr_low_but_exploited` divergence flag
marks findings the vendor score rated Low that are on KEV or weaponized — nine of them in the
reference run.

**The optional AI layer.** For the long tail of assets no deterministic rule resolves, an LLM reads
scanner evidence (device type, OS fingerprint, CPE, open ports) and *proposes* classifications. It is
structurally constrained: `scoring/` never imports `classifier/` (enforced by an import-graph test and
a fresh-interpreter check), it can never set `external`, `crown_jewel` or `in_scope` at any confidence,
its output is validated against the project's enums, and it abstains with a review flag rather than
fabricate. The AI proposes, a human freezes the overlay, the deterministic engine decides.

Python 3.10+, standard library only at runtime, MIT, 489 tests. Ships as a Claude Code plugin with a
skill, so the whole pipeline can be driven conversationally.
