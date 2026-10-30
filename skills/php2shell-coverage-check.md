---
last_reviewed: 2026-10-29
name: "PHP2Shell Coverage Check"
author: "Lance Duvall"
github_url: "https://github.com/lanz/php2shell-coverage-check"
description: "Checks that Tenable scanning is set up to detect PHP2Shell on every PHP host: plugin feed, credentials and scan settings. Lists the hosts that need a rescan, and flags end-of-life PHP. Works from Tenable Vulnerability Management, Security Center or .nessus files, without Hexa."
license: "MIT"
tier: "contributed"
tags: ["php2shell", "php", "cve-2026-109618", "cve-2026-109619", "scan-coverage", "rescan", "tenable", "tenable-vm", "security-center", "nessus", "pytenable", "claude-code"]
domains: ["vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-10-27
contribution_agreement_date: 2026-10-27T03:00:09Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "/php2shell-coverage-check"
---

Tenable detects PHP2Shell (CVE-2026-109618, CVE-2026-109619) once a host is scanned with the
PHP2Shell plugins and the right settings. Hosts that haven't had that scan yet show no
finding, the same as patched hosts. PHP2Shell Coverage Check tells them apart for every
host where Tenable has seen PHP, and gives you the list of hosts to rescan.

> **PHP2Shell coverage is evolving quickly.** Tenable Research keeps publishing plugins and
> updating its guidance. The check picks up new CVE plugins automatically, and the skill
> will be updated as coverage evolves. Always follow the
> [Tenable Research PHP2Shell FAQ](https://www.tenable.com/blog/php2shell-cve-2026-109618-cve-2026-109619-frequently-asked-questions-about-critical-php-remote)
> for current guidance.

## Why it's useful

The PHP2Shell plugins were published on 2026-10-21, and more keep arriving as distro
advisories and product checks are added. Early in an emergency like this, how many
findings you have depends as much on when and how each host was last scanned as on how
many hosts are vulnerable. This check shows which is which:

- **Turns "no finding" into a next step:** each PHP host is sorted into vulnerable, needs a
  rescan, or done, with the reason and the fix.
- **Finds the scan settings that matter:** plugin feed, credentials, "Assess component
  installs" and "Scan for Unpatched Vulnerabilities", read from each host's last scan.
- **Flags end-of-life PHP** (8.1 and older, with no fixed release) from the detected
  version, even before a CVE finding exists for it.
- **Avoids false alarms on distro PHP**, whose backported fixes don't change the version
  number, by leaving those hosts to the distro plugins.
- **Prints the rescan list** (`targets`), one address per line, ready to paste into a scan.

## What it does

- **Gives every PHP host a verdict, with the reason and the fix:**
  - *vulnerable:* a plugin for either CVE reports it
  - *likely-vulnerable:* the detected PHP version is affected, but no PHP2Shell plugin
    reports it, as with end-of-life PHP
  - *unverified:* no finding yet, because the last scan wasn't set up to detect it
  - *patched*, or *no-finding* from a scan that was set up to detect it
- **Explains why a host needs a rescan:** a plugin feed from before the plugins existed, no
  credentials with only remote PHP detection, missing scan information, or "Assess
  component installs" off for PHP bundled in another product.
- Reports as markdown, CSV or JSON, and includes Tenable Research's fixed versions and
  interim mitigations.

## How it fits with the other PHP2Shell listings

The **PHP2Shell Tenable Skill** and the **PHP2Shell Response Playbook** answer *where are we
exposed, what do we fix first, and were we hit?*, from Tenable One through Hexa AI MCP.
This check answers the question before those: *are our scans set up to find it
everywhere?*

1. Run this check and rescan the hosts it lists.
2. Run the exposure report or the playbook, so it works from complete scan data.
3. Run this check again to explain any host that shows as unknown or has no finding.

Without Tenable One or Hexa AI, it works on its own.

## How it works

For each host it joins three things:

1. The PHP installs and versions from the inventory plugins (48243, 58987, 216936, 200476).
2. Every finding for the two CVEs, from any plugin, so new plugins are included
   automatically.
3. The host's latest Nessus Scan Information (plugin 19506), which records the plugin feed
   the scan used, whether it was credentialed, and its settings.

- **Sources:** two vulnerability exports on Tenable Vulnerability Management, cumulative
  and patched analysis queries on Tenable Security Center, or `.nessus` exports from any
  Nessus edition (including Security Center's zipped downloads).
- **Read-only:** every request reads data. On VM it starts two export jobs, which change
  nothing, and cancels them if collection stops early.
- **Local snapshot:** results are saved owner-only, and reports run offline from it.
- **Profile-driven:** the PHP2Shell specifics live in a small JSON profile, which is
  updated as coverage changes, and the same tool can cover the next emergency
  vulnerability.

It has been run against live Tenable VM containers and live Security Centers, where it
found hosts last scanned before the plugins existed and end-of-life PHP with no CVE
finding yet. It's covered by offline tests using synthetic data in the formats of real
plugin output.
