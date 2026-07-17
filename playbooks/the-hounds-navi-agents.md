---
playbook_type: "standard"
name: "The Hounds — navi-agents"
author: "packetchaos"
github_url: "https://github.com/packetchaos/the-hounds-repo"
description: "The executable harness for The Hounds — a local console that runs the exposure-management agent pack over Tenable navi."
license: "MIT"
tier: "contributed"
tags: [tenable, exposure-management, navi, playbook, python, console, vulnerability-management]
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
contribution_agreement_date: 2026-07-15T18:28:19Z
---

The Hounds — navi-agents is the executable harness for the pack: a local console
(`navi-agents/`) that runs the exposure-management hounds over
[Tenable **navi**](https://github.com/packetchaos/navi) (`navi.db` + the Tenable API) and
surfaces the results in the browser. It runs on a stock Python install — the default server
needs no third-party packages.

## What it does

It executes the same pack of specialists as a program rather than a skill: CISA KEV
(Laelaps), attack paths (Fenrir), IoT/OT (Cerberus), AI inventory (Pythia), certificates
(Certania), EOL software (Charon), ACR calibration (Anubis), and the rest. Each hound
hunts one kind of exposure and proposes navi tag/ACR writes for human approval; writes are
disabled by default (`NAVI_ALLOW_WRITES=0`).

## How it works

Launch with `python3 run.py` (zero-dependency stdlib server, or optional FastAPI/Flask).
On first run it builds a bundled sample database so you can evaluate it with no setup; for
production, point `NAVI_DB_PATH` at navi's real `navi.db`. The `core/` engine provides the
shared detection, discovery, health, MITRE, and EOL logic, and `core/agents/` holds the
individual hound implementations. Every write stays grounded in real navi data and gated
behind explicit confirmation.
