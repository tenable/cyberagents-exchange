---
name: "Threat Intel Toolkit"
author: "kevinmhorvath"
github_url: "https://github.com/kevinmhorvath/threat-intel-toolkit"
description: "Defensive IOC and CVE triage agent that rates indicators and exploit maturity from free, key-free open-source intelligence."
license: "MIT"
tier: "contributed"
tags: ["threat-intelligence", "ioc", "cve", "vulnerability-triage", "exploit-maturity", "cisa-kev", "epss", "defensive"]
integrations: ["NVD", "Rapid7"]
date_added: 2026-08-13
contribution_agreement_date: 2026-08-13T14:29:02Z
works_with_tenable_hexa_mcp: false
last_reviewed: 2026-08-13
---

The Threat Intel Toolkit is a defensive triage agent for security operators who need a fast, defensible answer to two everyday questions: "is this indicator known-bad, and who says so?" and "how weaponized is this CVE right now?" It runs entirely on free, anonymously-fetched open-source intelligence — no API keys, no registration, no account — so a team can clone it and get answers in the first minute rather than after a procurement cycle.

## What it does

Hand the agent one indicator or a batch pasted from a SIEM alert, firewall log, or phishing email — IPs, domains, URLs, CVEs, in any mix, including defanged forms like `1[.]2[.]3[.]4` and `hxxp://`. It returns a verdict per indicator (malicious, suspicious, exploited, context-only, or clean), names exactly which sources fired, and adds a short "so what" recommendation weighted to what you're investigating. For CVEs it separately reports in-the-wild status and public exploit maturity, because those two facts diverge and a defender needs both to prioritize a patch.

Indicator reputation is checked against roughly 435,000 entries drawn from ten curated free feeds (CISA KEV, abuse.ch Feodo Tracker, stamparm/ipsum, Emerging Threats Open, blocklist.de, GreenSnow, SANS DShield, Spamhaus DROP, Phishing.Database, and the Tor exit list). CVE exploit maturity is rated from CISA KEV, FIRST EPSS, Metasploit, Nuclei, Exploit-DB, and the nomi-sec and trickest proof-of-concept aggregators. The toolkit references each feed's URL and fetches it at runtime into a local cache on the operator's own machine — it never re-hosts or redistributes feed data, and each source stays under its own license.

It is defensive by design. It reports what public sources already say and never contacts, scans, or attacks an indicator; a clean result is explicitly not treated as proof of safety, since feeds lag reality. The exploit-availability component locates and *rates* already-public exploit material for prioritization only — it does not write, weaponize, or provide steps for exploits. A recent hardening pass also fixed a fail-open case so that an unreachable feed now renders as an explicit "unknown," never as a false negative finding.

## How it works

A `threat-intel-analyst` subagent sits on top of two complementary skills and routes by indicator type: IPs, domains, and URLs go to an indicator-reputation skill backed by a single standard-library Python script that aggregates the ten feeds into a local SQLite cache and looks indicators up offline; CVEs go to an exploit-availability skill that queries the maturity sources and computes a tier. A mixed batch is split and both skills run, then the agent presents one unified triage with analyst judgment layered on top of the raw signals — corroboration weighting, recency caveats, and honest coverage limits (for example, file hashes are intentionally out of scope because the reputable free hash feeds now require a key).

Everything is standard-library Python 3.8+ with no dependencies to install, so it runs the same on an analyst laptop or an air-gapped jump box. A weekly GitHub Actions health check smoke-tests every source and fails loudly if a feed goes unreachable, empty, or unparseable before it can mislead a user. The repository doubles as its own single-plugin marketplace for one-click install, and either skill can also be used directly without the orchestrating agent.
