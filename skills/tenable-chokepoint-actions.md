---
name: "Tenable One Choke-Point Action Dashboard"
author: "arnzg"
github_url: "https://github.com/arnzg/apa-chokepoint-analysis"
description: "Turns Tenable One Attack Path Analysis data into a prioritized, self-contained HTML remediation dashboard with native Tenable scoring and a CISA KEV cross-reference for actively-exploited findings on choke points"
license: "MIT"
tier: "contributed"
tags: ["tenable-one", "exposure-management", "attack-path-analysis", "choke-points", "vuln-management", "threat-intelligence", "cisa-kev", "ransomware", "dashboard", "claude-code"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-07-10
contribution_agreement_date: 2026-07-10T16:24:52Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code"]
invocation: "/tenable-chokepoint-actions"
---

A Claude Code skill that converts Tenable One (Exposure Management) Attack Path Analysis data into an actionable HTML dashboard centered on **choke points** — the assets, identities, groups, and OT devices that the most attack paths pass through — and flags **actively-exploited weaknesses** on those choke points using the CISA Known Exploited Vulnerabilities catalog.

## What it does

- Detects the Tenable One instance with computed APA data and pulls choke-point assets via the connected Tenable MCP server.
- Ranks choke points using **native Tenable scoring** — AES (Asset Exposure Score), ACR (Asset Criticality Rating), and APA path tier — no invented composite score.
- Computes shared-weakness blast radius and resolves every affected asset/account name so each remediation row shows exactly who to fix.
- Cross-references findings against the **CISA KEV** catalog, flagging actively-exploited and ransomware-linked weaknesses; surfaces those that hit choke points as urgent priority.
- Surfaces identity and OT choke points with class-aware remediation (the choke-point table is filterable by type — Device, Identity, OT, Application), intersects them with crown-jewel assets, renders an interactive attack-path map of the real APA topology, and writes everything into a single offline HTML file with an executive summary, a 🔴 Actively Exploited section (with CVEs, CISA-KEV dates, and VPR backfilled from plugin data), choke-point landscape, practitioner remediation queue, and CSV export.

## How it works

Invoke it from within Claude Code with a Tenable MCP server connected. It runs read-only inventory queries (MCP or REST), pulls the KEV feed once at generation time, scores choke points per the documented methodology, and writes a self-contained dashboard to `./chokepoint-output/`. The dashboard itself is fully offline — no CDNs, no network calls. The skill is explicit about provenance: native Tenable scores are exact, blast radius and choke-point intersections are computed from the asset↔finding map, and KEV flags come from a verified `finding_cves` filter match. If the KEV feed is unreachable (TLS-intercepting proxy, offline), the urgent section is gracefully omitted while the rest of the dashboard generates.
