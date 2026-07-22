---
name: "Trust Posture Narrator"
author: "kffbos"
github_url: "https://github.com/kffbos/tenable-trust-posture-narrator"
description: "Turns live Tenable exposure and remediation data into a quick-scan snapshot plus ready-to-use trust-center copy, RFP answers, and proof points."
license: "MIT"
tier: "contributed"
tags: ["trust-center", "marketing", "reporting", "compliance", "vulnerability-management"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-07-22
contribution_agreement_date: 2026-07-22T18:47:17Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code"]
invocation: "/trust-posture-narrator"
---

## What it does

Trust Posture Narrator bridges a gap most Tenable-integrated agents don't touch: it turns live exposure-management data into accurate, ready-to-use language for the teams downstream of security — trust/compliance, marketing, and executive reporting. Instead of manually drafting trust-center blurbs, RFP security-questionnaire answers, and proof points from stale or guessed figures, this skill pulls current aggregate metrics — findings by severity, remediation SLA compliance, scan coverage, and trend vs. the prior period — directly from Tenable via the Hexa MCP server, and drafts a bulleted quick-scan snapshot plus all three copy formats in one pass, with every hard number bolded and trend arrows in place of a chart.

Every output is run through a redaction and claims filter before it's returned: no host, IP, asset, or CVE-level detail; no absolute-security language ("fully secure," "zero vulnerabilities"); no claim that isn't traceable to a metric the skill actually retrieved that run. Every response ends with a mandatory footer requiring Security, Legal, and Compliance sign-off before external use — this skill produces first drafts, not approved copy.

## How it works

It's a single Claude Code skill definition — no custom backend, no data storage, no credentials handled by the skill itself. It relies entirely on the Tenable Hexa MCP server for data access (auth stays in your existing Hexa MCP connection) and on a constrained instruction set that governs what it's allowed to query, retain, and phrase. Because the underlying data is live, output only reflects the Tenable environment the invoking user is already authenticated to.
