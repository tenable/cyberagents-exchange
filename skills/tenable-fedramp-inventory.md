---
name: "Tenable → FedRAMP Integrated Inventory Workbook"
author: "conard0-git"
github_url: "https://github.com/conard0-git/tenable-fedramp-inventory"
description: "Build the FedRAMP Integrated Inventory Workbook (IIW) by reconciling a cloud fleet, Tenable Security Center, and Nessus Manager. Read-only, review-by-default."
license: "MIT"
tier: "contributed"
tags: ["fedramp", "fiiw", "iiw", "integrated-inventory", "inventory", "tenable", "security-center", "nessus", "conmon", "compliance-reporting"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-07
contribution_agreement_date: 2026-08-06T20:32:58Z
compatible_platforms: ["Claude Code"]
invocation: "/tenable-fedramp-inventory"
---

Produce the monthly FedRAMP **Integrated Inventory Workbook (IIW)** by
reconciling three sources into one authoritative asset list: a **cloud
fleet** (running instances), **Tenable Security Center** scan data, and
the **Nessus Manager** agent registry. The output maps onto the canonical
FedRAMP IIW column schema and is maintained as a protected master
workbook that carries forward month to month. The cloud side is a
**pluggable inventory provider** — the reference implementation uses AWS
EC2, but Azure, GCP, or on-prem sources meeting the same per-instance
contract (instance id, name, IPs, MAC, DNS, location, owner tag,
running-state) drop in without touching the reconciliation logic.

This is a **documentation skill** — it teaches the workflow and the
FedRAMP inventory mappings so a Claude Code assistant can reproduce the
pipeline against your own environment; it does not ship a runnable
implementation.

## What it does

- **Three-source reconciliation.** Cloud is authoritative for asset
  existence, lifecycle, IPs, and owner tag; Tenable is authoritative for
  scan presence, authenticated-scan status, and OS/version; Nessus is
  used only to annotate why a host lacks an authenticated scan. Tool-wide
  match precedence: **instance id → name → IP → DNS**.
- **Canonical FedRAMP IIW schema.** Maps every value onto the 24-column
  canonical layout (Unique Asset Identifier, IP, Virtual, Public, DNS,
  NetBIOS, MAC, Authenticated Scan, OS Name/Version, Location, Asset
  Type, Hardware Make/Model, In Latest Scan, Software/DB Vendor, Patch
  Level, Function, Comments, Asset Tag, VLAN, System/App Administrator,
  End-of-Life, …) via a fuzzy column resolver so header drift,
  hand-edits, and template revisions don't break the pipeline.
- **Review-by-default master update.** Review mode (the default) writes
  a dated review workbook — Inventory + summary sheets with Nessus agent
  annotations explaining un-authenticated hosts — and leaves the master
  untouched. Update mode overwrites the master in place, but only after
  decommissioned rows are dropped and helper columns stripped.
- **Owner precedence.** Cloud owner/team tags are authoritative — they
  set or replace the owner when the tag is present and non-placeholder.
  Optional inference passes (comment-rule, comment-prefix majority,
  diagram-label majority) fill blank owner cells only, never overwriting
  existing values, with ≥ 2-vote / skip-ties guards.
- **OS + EOL enrichment.** Parses OS/version from Tenable scan records
  with source priority (richer network-device OS from credentialed
  plugin output beats a general server OS parse), estimates End-of-Life
  from an OS→EOL lookup, and re-derives EOL at the end so manual edits
  to the OS column stay consistent.
- **Ghost-asset detection.** Scanned hosts whose IPs fall in cloud
  network space but aren't running instances are flagged as ghost assets
  (reported, never auto-added to inventory).
- **Decommission tracking.** On-prem/physical hosts absent from recent
  scans can be immediately dropped or **aged** (drop after ≥ N
  consecutive absent days, default ~15, tracked in a small local
  miss-tracker workbook) so a single missed scan doesn't remove a host
  prematurely.

## How it works

The pipeline is **read-only against source systems** — it reads from the
cloud provider, Tenable, and Nessus and writes only local files (Excel
workbooks, cached scan downloads, and small tracker workbooks). It never
modifies Tenable data, hosts, or agents. The **review-by-default**
posture is the second safety layer: the protected master workbook stays
untouched unless the caller explicitly enables update mode, and even
then the update path drops decommissioned rows and strips helper columns
first. Environment scoping is done by **IP CIDR** rather than a stored
column, so one workbook can span multiple environments and be filtered
without polluting the FedRAMP-standard structure. Everything site-
specific — master filenames, scan names, network ranges, region
defaults, owner/team normalization maps — lives in configuration, never
in code. See `SKILL.md` for the pipeline, `references/reconciliation.md`
for the three-source pull and join cascade,
`references/inventory-schema.md` for the canonical schema + resolver +
review/update model, and `references/enrichment.md` for OS/EOL, staging,
decommission, and the optional physical-asset layer.
