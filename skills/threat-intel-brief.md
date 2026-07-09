---
name: "Threat Intel Brief"
author: "meir-asiskovich"
github_url: "https://github.com/meir-asiskovich/Brief-me-on-Hexa-skill"
description: "Comprehensive cyber threat intelligence briefings for any CVE, advisory, threat actor, or product — in minutes."
license: "MIT"
type: "skill"
tier: "unreviewed"
tags: ["threat-intelligence", "cve", "incident-response", "soc", "mitre-attack", "vulnerability-management", "tenable-one"]
integrations: ["Tenable"]
date_added: 2026-07-06
compatible_platforms: ["Claude Code", "Claude Cowork"]
invocation: "/threat-intel-brief"
---

A Claude skill that produces comprehensive **cyber threat intelligence briefings** for any domain, threat actor, CVE, product, or vendor — in minutes instead of days.

Built for **security analysts, SOC teams, IR leads, CISOs, and MSSPs**. Given any starting point, the skill researches and compiles a structured brief covering CVEs & advisories, threat actor profiles, targeted industries, MITRE ATT&CK-mapped exploitation techniques, trend analysis, and live Tenable One asset exposure.

## What it does

1. **CVE & Advisory Landscape** — vulnerabilities from NVD, CISA KEV, and official agency advisories (CISA, FBI, NSA, NCSC, ENISA, BSI, ANSSI, and more)
2. **Threat Actor Profiles** — who's attacking, attribution, motivation, aliases, and MITRE ATT&CK group links
3. **Targeted Organizations & Industries** — which sectors and named victims (from public sources only)
4. **Exploitation Techniques** — full ATT&CK tactic chain, named malware/tools, detection opportunities
5. **Trend Analysis & Watch List** — forward-looking signals for the next 30–90 days
6. **Tenable One Asset Exposure** — queries your Tenable One environment to show which of your assets are affected by the CVEs found in the brief

## Input modes

The skill accepts any of these as a starting point and detects the type automatically:

- **CVE ID** — e.g., `CVE-2024-3400` or `CVE-2023-46805, CVE-2024-21887`
- **Advisory ID** — e.g., `AA24-131A`, `NCSC advisory on SVR activity`
- **Free-text description** — e.g., `"that Palo Alto GlobalProtect auth bypass from last month"`
- **Product or vendor** — e.g., `Siemens S7-1500 PLC`, `VMware vCenter`, `Juniper Junos`
- **Broad topic** — e.g., `Volt Typhoon`, `healthcare ransomware`, `OT/ICS attacks`

## Example prompts

```
Brief me on Volt Typhoon — who they're targeting, what CVEs they use, and which agencies have issued warnings.
```

```
CVE-2024-3400 — give me the full threat picture: who's exploiting it, what they do post-exploitation, and who's been targeted.
```

```
I need a board-ready brief on ransomware threats to US healthcare — business impact, active groups, and regulatory exposure.
```

## Tenable One Integration

Phase 6 runs automatically on every brief. When CVEs are identified, the skill queries your Tenable One environment to surface which of your assets are exposed — turning external threat intel into internal exposure data.

Setup: create `~/tenable_keys.env` with your Tenable One API keys (get them from Settings → My Account → API Keys).

A standalone script is also bundled at `scripts/tenable_cve_assets.py` for direct CVE-to-asset lookups outside the skill.
