---
last_reviewed: 2026-11-04
name: "Exposure Radio"
author: "Agent9AI"
github_url: "https://github.com/Agent9AI/exposure-radio"
description: "A security radio station for small IT teams: two hosts brief what changed in Tenable, what to fix first and what was verified fixed, between weather, CISA and Cloudflare Zero Wire news, Learn segments and music."
license: "MIT"
tier: "contributed"
tags: ["exposure-management", "audio", "team-awareness", "evidence", "read-only"]
domains: ["vulnerability-management", "security-operations"]
integrations: ["Tenable", "GCP", "Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T10:47:01Z
works_with_tenable_hexa_mcp: false
---

# Exposure Radio

Small IT teams rarely hold a security standup. Exposure Radio gives them one they can hear while they work. It compares yesterday's and today's Tenable Vulnerability Management exports (the before and after of a scan cycle) and airs four short segments: a **Priority** interruption when something on CISA's exploited list lands on your machines, a **Watch list** that separates new exposure from new visibility, **Wins** verified by a rescan, and **Blind spots** for missed or uncredentialed scans. Weather, CISA and Cloudflare Zero Wire news, sixty-second Learn explainers and original music fill the hour.

## What it does

- Two hosts speak plainly ("the Ivanti Connect Secure flaw is open on one asset"); CVE IDs, owners and deadlines stay on screen and on a copyable action card.
- Every tenant exposure line is rebuilt from typed evidence and compared word for word; its caption passes a claim gate that blocks 27 of 27 adversarial statements.
- A station host serves the listener and a console for segments, queue, Learn topics and connections. Keys stay in a private file on the host; the browser only learns whether one is set.
- Bring-your-own services: Tenable export API (read-only), Gemini voices and Search-grounded Learn suggestions, the official YouTube embedded player, keyless NWS weather and CISA feeds.
- Keyless Cloudflare Zero Wire briefings add plain-language threat context and coverage caveats. Exact-CVE matches enrich open action cards locally; tenant CVEs never leave the host for this lookup. Public context does not change the evidence gate or establish that Cloudflare protects an environment.
- Read-only MCP tools: exposure_briefing, check_claims, remediation_packet and explain_priority. Open the clone in Claude Code and they load from `.mcp.json`, with an exposure-briefing skill that runs every factual sentence through check_claims before answering.

## Run

Python 3.10+, standard library only:

```bash
python3 -m exposure_radio station serve
make check
```

The repository includes a pre-rendered sample hour built from synthetic Tenable exports, so it plays with no keys. Exposure segments use local voices unless the operator's Gemini project is on a paid tier.
