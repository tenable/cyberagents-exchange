---
playbook_type: "standard"
name: "The Hounds — Pack Playbook"
author: "packetchaos"
github_url: "https://github.com/packetchaos/the-hounds-harness"
description: "A skill-packaged playbook for The Hounds — 18 exposure-management specialists that hunt, tag, and calibrate risk over Tenable navi."
license: "MIT"
tier: "contributed"
tags: [tenable, exposure-management, navi, playbook, claude-skills, asset-tagging, vulnerability-management]
integrations: [Tenable, Anthropic]
agents_used:
  - name: "Laelaps"
    role: "Finds and tags CISA KEV (known exploited) exposure."
    type: "info"
  - name: "Certania"
    role: "Tracks certificate expiry and weak crypto."
    type: "info"
  - name: "Heimdall"
    role: "Assesses post-quantum readiness."
    type: "info"
  - name: "Fenrir"
    role: "Chains signals into ranked attack paths (foothold to crown jewel)."
    type: "info"
  - name: "Cerberus"
    role: "Confidence-scored IoT / OT / embedded device discovery."
    type: "info"
  - name: "Pythia"
    role: "Discovers and governs AI/ML inventory across five sources."
    type: "info"
  - name: "Atlas"
    role: "Establishes asset ownership."
    type: "info"
  - name: "Mimir"
    role: "Software inventory."
    type: "info"
  - name: "Charon"
    role: "Flags end-of-life / unsupported software."
    type: "info"
  - name: "Anubis"
    role: "Calibrates Asset Criticality Rating (ACR)."
    type: "info"
  - name: "Chronos"
    role: "Scan health monitoring."
    type: "info"
  - name: "Sirius"
    role: "Agent group analysis."
    type: "info"
  - name: "Garmr"
    role: "Tag removal and cleanup."
    type: "info"
  - name: "Orthrus"
    role: "Maps findings to MITRE ATT&CK."
    type: "info"
  - name: "Argus"
    role: "Custom application discovery."
    type: "info"
  - name: "Argos"
    role: "Single-asset deep-dive."
    type: "info"
  - name: "Sphinx"
    role: "'On the Scent' environment overview."
    type: "info"
  - name: "Covenant"
    role: "Enforces the AI Contract governance policy."
    type: "info"
date_added: 2026-07-15
last_reviewed: 2026-07-17
contribution_agreement_date: 2026-07-15T18:28:14Z
---

The Hounds is a pack of exposure-management specialists — "hounds" — that run over
[Tenable **navi**](https://github.com/packetchaos/navi) (`navi.db` + the Tenable API). This
repository packages the pack as a Claude skill (`the-hounds/SKILL.md` plus `references/`):
the domain knowledge for what each hound looks for, how it tags it, and which navi selector
it uses.

## What it does

Each hound hunts one kind of exposure and then tags it, calibrates its risk, or answers a
question — from CISA KEV (Laelaps) and attack paths (Fenrir) to IoT/OT (Cerberus), AI
inventory (Pythia), certificates (Certania), EOL software (Charon), and ACR calibration
(Anubis). You can run a hound by name ("run Laelaps") or "release the hounds" to run the
whole pack.

## How it works

The playbook follows a strict operating doctrine: grounded (answer only from real navi
results), propose-then-confirm for every write (show the exact command, `category:value`,
and matched-asset count; platform writes also require `NAVI_MCP_ALLOW_WRITES=1`), prefer
built-in selectors, distinguish ephemeral vs persistent tags, surface blind/uncredentialed
coverage, and verify after writing. Pair it with the navi skills
(navi-core, navi-enrich, navi-explore, navi-mcp) that supply the tool mechanics.
