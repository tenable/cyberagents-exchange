---
last_reviewed: 2026-10-26
name: "T1OTE IEC 62443 Onboarding"
author: "dpstorey"
github_url: "https://github.com/dpstorey/T1OTE_IEC62443"
description: "Guided IEC 62443 zones-and-conduits onboarding for Tenable OT: validate, plan, approve, then create policies."
license: "Apache-2.0"
tier: "contributed"
tags: [tenable-ot, iec-62443, zones-conduits, segmentation, ot-security, compliance]
integrations: ["Tenable"]
date_added: 2026-10-12
contribution_agreement_date: 2026-10-12T18:26:15Z
domains: ["ot-iot-security", "governance-risk-compliance"]
compatible_platforms: ["LibreChat"]
invocation: "Ask the agent to onboard a Tenable OT site to IEC 62443"
---

An agent skill that turns an IEC 62443 zones-and-conduits design into Tenable OT objects. It asks guided questions (or reads a spreadsheet), validates the model, shows a numbered plan, and changes nothing until the user approves it. Tested with LibreChat and Qwen.

## What it does

IEC 62443 describes a network as zones (sets of assets) joined by conduits (the allowed communication paths between them). Tenable OT has no native objects for either. This skill builds them from what Tenable OT does have: a zone becomes one or more address-based asset groups, and a conduit becomes a set of detection policies that fire when traffic strays outside the allowed path.

- **Guided input.** Asks for the site, zones, address space (CIDR blocks, ranges, IP lists, VLANs or picked assets) and conduits, in chat or from a spreadsheet template it generates.
- **Validation.** A deterministic script checks CIDR syntax, overlaps between zones, duplicate and reserved names, conduits that reference unknown zones, and missing directions.
- **Data quality check.** Reports the site's data quality (the share of assets positively classified, against a target of 90% that the user can change) and warns when type-based asset groups would miss unclassified assets. Counts only; it never lists assets.
- **Plan first.** Produces a numbered plan of every call it will make, with the resulting object counts. Nothing is written until the user approves.
- **Strict conduit direction.** Each conduit declares who initiates. It warns when a one-way conduit carries UDP-heavy protocols, because the sensor can infer direction wrongly for those. The one-way direction rule has not been tested with UDP or mid-connection TCP traffic.
- **Safe defaults.** Policies are created disabled unless the user asks otherwise. Every write is a dry run first. Undo disables policies; archives are never done automatically.
- **Optional samples.** Sample asset groups by device type, a remote-admin-to-controllers policy, and a new-asset-in-zone policy per zone.

## How it works

Five helper scripts do the deterministic work (template generation, workbook parsing, validation, plan building, journal and undo), so the model only asks questions and drives the approval gate. The plan uses three policy shapes: a boundary policy per zone (traffic to anywhere except itself and its permitted targets), one policy for traffic from outside any declared zone into a zone, and a conformance policy per conduit direction that alerts on any protocol outside the conduit's allowed set.

It is a companion to the Tenable OT MCP server, Enterprise Manager edition ([EM-MCP](https://github.com/dpstorey/EM-MCP)), and needs that server with write tools enabled. The skill's scripts make no outbound network calls; all traffic is the MCP server talking to the user's own Enterprise Manager and Tenable OT sites.
