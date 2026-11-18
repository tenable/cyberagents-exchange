---
last_reviewed: 2026-10-28
name: "Tenable Scan Sweep"
author: "Lance Duvall"
github_url: "https://github.com/lanz/tenable-scan-sweep"
description: "Answers which scans target an IP, range, hostname, tag, agent group, asset list, scanner or credential across every scan in Tenable Vulnerability Management or Tenable Security Center, and audits scan configurations for duplicates, missing credentials and unparsable targets, from a read-only local snapshot."
license: "MIT"
tier: "contributed"
tags: ["tenable", "scan-management", "scan-coverage", "scan-hygiene", "vulnerability-management", "tenable-vm", "security-center", "pytenable", "audit", "claude-code"]
domains: ["platform-operations", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-10-26
contribution_agreement_date: 2026-10-26T20:45:33Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "/tenable-scan-sweep"
---

Neither Tenable Vulnerability Management nor Tenable Security Center can answer "which scans
target 10.20.4.17?" In VM, getting the answer means reading every scan's configuration, one
API call per scan. In Security Center, it means expanding every asset list the scans use.
Doing that through an AI assistant or MCP server spends a tool call and its tokens on each
scan or list, and runs out of either long before a large container is covered. Tenable
Scan Sweep is a Claude Code skill with a bundled script that makes those calls itself,
once, read-only. It saves a local snapshot and then answers scan-configuration questions
instantly.

## What it does

- **Finds which scans target something.** The target can be an IP, CIDR, range, octet range
  or hostname, matched by address overlap. It can also be a tag, agent group, target group,
  scanner, credential type, policy, template or owner. Each match says why it matched, and
  the output notes when an address falls under a VM exclusion or an SC freeze window.
- **Resolves tag-targeted and agent scans for a specific asset.** With `collect --assets`, it
  also indexes the asset inventory and agent list, so `find` knows which tags an address
  carries and which agent groups its agent is in. Without the index, those scans are listed
  as unresolved, with their tags, rather than silently skipped.
- **Finds overlapping and duplicate scans**, with shared address counts and schedules.
- **Audits scan configurations:**
  - scans with no targets
  - credentialed templates without credentials, checking both the scan and its policy
  - targets VM won't parse, such as pasted rich text, URLs and octets over 255
  - DNS-dependent subnets
  - deprecated target groups
  - on-demand-only scans
  - unused agent groups, target groups and scanners (on SC, a count of asset lists no scan
    uses)
- **Reports credential usage**: which scans use each credential type and managed credential.

## How it works

`collect` lists every scan, paging when the response is paginated. It reads each scan with
one `GET /editor/scan/{id}` call, whose option lists also resolve tag, agent group, scanner
and policy names, so no extra lookups are needed. It reads each referenced policy once for
its credentials, and the exclusion list once. Every request is a `GET`, except the optional
`--assets` index, which starts one asset export job (and cancels it if collection stops
early). Credential secrets are never collected. Every other command (`find`, `overlaps`,
`audit`, `credentials`, `show`, `list`, `status`) runs offline against the snapshot. The
target parser follows the documented VM target formats. The skill tells Claude how to map
questions to commands, report the snapshot's age, and explain the cases the snapshot can't
decide.

On Security Center, `collect --platform sc` reads every scan, asset list, policy and
freeze window in a handful of `GET` requests. Static, DNS-name and watchlist asset lists
are expanded to their members, and `--assets` reads the current members of the rule-based
lists that scans use, one request per list. Overlaps are compared within a repository.

It has been run against live Tenable VM containers, including one with a paginated scan
list, and live Security Centers, and is covered by offline tests using synthetic data.
