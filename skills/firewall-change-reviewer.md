---
last_reviewed: 2026-10-07
name: "Firewall Change Reviewer"
author: "LordBusiness011124"
github_url: "https://github.com/LordBusiness011124/Tenable-Cyber-Agent-Skill-Builder-Exchange"
description: "Reviews firewall changes against required and forbidden access policy using exact local range evaluation."
license: "MIT"
tier: "contributed"
tags: ["firewall", "change-review", "access-policy", "network-segmentation", "configuration-analysis"]
domains: ["network-security"]
integrations: []
date_added: 2026-10-06
contribution_agreement_date: 2026-10-06T15:54:15Z
compatible_platforms: ["Codex"]
invocation: "$firewall-change-reviewer"
---

Firewall Change Reviewer helps security engineers determine whether a proposed firewall configuration introduces forbidden access or blocks required connectivity. It is a reusable agent skill backed by an offline Python engine, with evidence reports for human review before approval.

## What it does

- Compares current and proposed configurations with explicit required and forbidden access requirements.
- Separates introduced, existing, and resolved policy violations, and reports newly permitted or blocked access.
- Identifies added, removed, modified, reordered, enabled, disabled, and broadened rules, plus full shadowing and relevant partial overlaps.
- Produces JSON and Markdown findings with exact affected ranges, before/after behavior, responsible rules or default actions, example connections, severity rationale, and suggested corrections.
- Adds optional asset names, roles, owners, and criticality to example evidence without allowing inventory labels to determine authorization.

## How it works

The user supplies current configuration, proposed configuration, and confirmed policy in the documented vendor-neutral JSON format. Codex follows SKILL.md to collect inputs, run the bundled reviewer, explain findings, and help draft separate corrected proposals. The Python engine uses ipaddress and exact interval partitioning across relevant address and destination-port boundaries. It evaluates first-match behavior across complete ranges for both configurations; it does not assume a sampled address represents an entire subnet.

The engine runs locally without an LLM API dependency, API keys, vendor integrations, or target-host connections. A plain-language policy interpretation requires confirmation before becoming authoritative. Corrections are checked by rerunning against the original current configuration and the same confirmed policy. Resource exhaustion produces an explicit incomplete verdict and partial evidence rather than a clean result.

Version one supports one ordered IPv4 rule list, TCP/UDP, destination ports and inclusive ranges, enabled/disabled rules, and an explicit default action. Native vendor parsing, NAT, routing, IPv6, connection tracking, application identity, and multiple firewall hops are outside its scope. Results describe configuration access within supplied policy coverage and do not prove live network reachability. The skill does not deploy firewall changes.

Setup, Codex installation, input formats, executable examples, and pytest verification are documented in the linked repository.
