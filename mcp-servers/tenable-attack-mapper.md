---
name: "Tenable ATT&CK Mapper"
author: "ayuksel-tenb"
github_url: "https://github.com/ayuksel-tenb/tenable-attack-mapper"
description: "An MCP server that maps Tenable Security Center findings to MITRE ATT&CK, lets you analyze exposure by tactic or technique in plain language, and exports a VPR-scored ATT&CK Navigator layer you can open in a local matrix viewer."
license: "MIT"
tier: "unreviewed"
tags: ["mitre-attack", "attack-mapping", "navigator", "vulnerability-management", "purple-team", "tenable", "mcp"]
integrations: ["Tenable", "NVD"]
date_added: 2026-06-20
transport: "stdio"
runtime: "python"
auth_method: "api-key"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor", "Windsurf", "VS Code Copilot"]
tools_exposed:
  - name: "map_environment"
    description: "Pull open findings from Security Center and map them to ATT&CK; returns the coverage summary and per-technique scores ranked by aggregated VPR. Scope to a repository or saved query."
  - name: "export_navigator_layer"
    description: "Map the environment and write a MITRE ATT&CK Navigator layer (v4.5) JSON to disk, ready to open in the matrix viewer or import into ATT&CK Navigator."
  - name: "techniques_for_tactic"
    description: "List the ATT&CK techniques under a given tactic (e.g. initial-access, execution, privilege-escalation) from the local catalog — a starting point for analysis."
  - name: "my_findings_for_techniques"
    description: "Reverse lookup: which of my findings map to the given ATT&CK technique IDs. Base techniques (T1190) also match their sub-techniques."
resources_exposed: []
prompts_exposed: []
---

Connect an AI assistant (Claude Code, Claude Desktop, or any MCP client) to **Tenable Security Center** and turn raw findings into a threat-informed, ATT&CK-mapped view of your exposure — then investigate it in plain language. Ask "which techniques cover initial access, and which of my findings match them?" and the agent answers from live, mapped data. When you want the visual, export a VPR-scored Navigator layer and open it in a local matrix viewer.

## What it does

- **map_environment** — pulls open findings from Security Center and maps each one to the MITRE ATT&CK techniques an adversary would use to exploit it, returning a coverage summary and per-technique scores ranked by aggregated VPR.
- **export_navigator_layer** — writes a ready-to-import ATT&CK Navigator layer (v4.5) you can open in the bundled matrix viewer, where every technique links back to the vulnerabilities (and their detail pages) behind it.
- **techniques_for_tactic** — lists the techniques under a tactic so you can scope an investigation ("for privilege-escalation, what should I watch for?").
- **my_findings_for_techniques** — reverse lookup from technique IDs to the findings that map to them, sub-technique aware.

Every mapping carries a confidence and a reason code; low-confidence mappings are flagged `needs-review` rather than silently trusted.

## How it works

Built on the official MCP SDK's FastMCP (Python 3.12), the server exposes the mapping core over stdio and authenticates to Tenable.sc with API keys read from the environment (`TSC_URL` / `TSC_ACCESS_KEY` / `TSC_SECRET_KEY`). A deterministic backbone resolves CVE → CWE (optionally via NVD) → CAPEC → ATT&CK where an authoritative chain exists; where it doesn't, a semantic fallback runs through the local `claude` CLI (billed to your Claude Code subscription — no API key, no per-token cost) to map the plugin name and description to candidate techniques with an evidence/reason code. The two layers are reconciled and de-duplicated, VPR drives the per-technique intensity score, and the result is emitted as a Navigator-compatible layer for overlaying against existing detection coverage to surface exploitable-but-undetected gaps.
