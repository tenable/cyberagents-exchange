---
name: "Cloud External Attack-Path Suite"
author: "Echo6Bravo"
github_url: "https://github.com/Echo6Bravo/cloud-ext-attack-path-suite"
description: "High-fidelity external attack-path agent for Tenable Cloud Security: running, internet-exposed workloads with a reachable service, an exploitable publicly-evidenced vulnerability (EPSS or CISA KEV), tiered by identity blast radius."
license: "MIT"
tier: "contributed"
tags: [cloud-security, tenable, attack-path, cnapp, exposure, epss, cisa-kev, cspm]
integrations: [Tenable, AWS, Azure, GCP]
date_added: 2026-08-02
contribution_agreement_date: 2026-08-02T20:51:53Z
---

The Cloud External Attack-Path Suite is an autonomous agent for Tenable Cloud Security
that answers one question with high fidelity: **which workloads can actually be reached
and exploited from the internet right now, and how bad is it if they are?** It is built
for cloud security architects and incident responders who want a short, defensible list
of genuine external attack paths — not a raw vulnerability dump.

It ships in two editions: an **MCP edition** that runs through the Tenable Cloud Security
(`tcs`) MCP connector's Explore/UDM data model for the richest results, and an
**API-token edition** that uses the public GraphQL API with a Bearer token and no
connector, for headless daily runs. Both editions share one self-testing detection spec
and one report renderer, so their findings are identical by construction.

## What makes a finding

A reachable IP:port and a high CVSS score are not, by themselves, an attack path. The
agent reports a workload only when the **entire chain** holds, applied in order:

1. It is a **running** virtual machine (a stopped VM is not a live path).
2. It is reachable **directly from the internet** (`ExternalDirect`).
3. It is open to a **wide range of IPs** / the whole internet (`Wide`/`All`).
4. A **live listening service was actually observed** on an internet-facing port
   (validated network endpoint — ports come from the endpoint, never a firewall rule).
5. The vulnerability finding is **open**.
6. It is **exploitable over the network** (AV:N).
7. It requires **no unusual conditions** to exploit (AC:Low).
8. The **vulnerable component is the service on the exposed port** (a curated
   package→service→port map excludes local-privilege-escalation and client-side CVEs).
9. There is **at least one independent public threat signal**: EPSS ≥ 0.30 **or** the CVE
   is on the CISA Known Exploited Vulnerabilities catalog.

Findings are then **tiered by identity blast radius**: Tier 1 (the workload's cloud
identity holds severe/administrative permissions — compromise can escalate to broad cloud
control) and Tier 2 (the same exposed, exploitable service on a standard-privilege
identity — a real foothold with contained blast radius). Privilege ranks findings; it
never hides one.

## Deliberately excluded signals

Evaluated and intentionally **not** used as qualifying gates: **CVSS base/impact score**
(frequently overweighted relative to real-world exploitability), **VPR** (proprietary; the
methodology targets the underlying exploitability signals directly), and
**proof-of-concept availability** (as a gate it admits lower-impact, older findings — it
is displayed for context only). Because the evidence gate is CVE-keyed, findings without a
CVE identifier (e.g. distribution advisories) are out of scope by design.

## How it works

All detection logic lives in a single self-testing source of truth
(`attack_path_spec.py`) that declares the gates as ordered data and **generates every
query from that declaration**, so the documented logic and the executed query cannot
drift. Running the spec fails loudly if a gate is missing or reordered, if a rejected
signal leaks into a filter, or if the stopped-VM gate is dropped. The renderer contains no
thresholds — it applies the component↔port post-filter, tiers by privilege, and writes a
self-contained two-tier HTML report (with per-finding attack-path diagrams, evidence,
exposed IP:port, and a print stylesheet for clean PDF export).

- **MCP edition** — pulls three datasets (inventory, validated endpoints, qualifying
  CVEs) via the `tcs` MCP `udm_execute_query` tools.
- **API-token edition** — introspects the GraphQL schema, maps each gate to concrete
  fields, and pulls the same three datasets cursor-paginated with a Bearer token.

## Run it daily

Both editions can run unattended each morning and report the delta from the prior day.
The API-token edition ships a `run_daily.sh` wrapper and a crontab example; the MCP
edition can be driven by the Claude Code scheduler. Real assessment data and API tokens
are kept out of version control.

## Requirements

- **MCP edition:** the Tenable Cloud Security `tcs` MCP connector; Python 3.8+ (stdlib
  only).
- **API-token edition:** a Tenable Cloud Security API token; `bash`, `curl`, `jq`;
  Python 3.8+ (stdlib only).
