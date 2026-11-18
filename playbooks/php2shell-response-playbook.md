---
last_reviewed: 2026-10-23
playbook_type: "standard"
name: "PHP2Shell Response Playbook"
author: "jtbuchanan-tenb"
github_url: "https://github.com/jtbuchanan-tenb/php2shell-playbook"
description: "Find, fix and hunt PHP2Shell (CVE-2026-109618, CVE-2026-109619) with three Exchange skills in one Claude Code command."
license: "MIT"
tier: "contributed"
tags: ["php2shell", "cve-2026-109618", "cve-2026-109619", "php", "rce", "remediation", "threat-hunting"]
domains: ["vulnerability-management", "security-operations"]
integrations: ["Tenable", "Tenable Hexa AI MCP", "Splunk", "Microsoft Sentinel"]
agents_used:
  - name: "PHP2Shell Tenable Skill"
    role: "Find it: grades every asset against the fixed PHP releases from Tenable One data."
    type: "exchange"
    ref: "skills/php2shell-tenable-skill"
  - name: "Remediation Priority & Impact Agent"
    role: "Fix it: ranks the PHP2Shell hosts by exposure and attack path, with Tenable's exact fix."
    type: "exchange"
    ref: "skills/remediation-priority-impact-agent"
  - name: "SOC-Hunter"
    role: "Hunt for it: hunts for exploitation across SIEM, EDR and Tenable data, back to Oct 17."
    type: "exchange"
    ref: "skills/soc-hunter"
date_added: 2026-10-23
contribution_agreement_date: 2026-10-23T20:27:37Z
works_with_tenable_hexa_mcp: true
cta: "T1"
---

Two critical CVEs let an unauthenticated attacker run code on any PHP that serves web requests, from PHP-FPM to mod_php. This playbook runs Tenable's three-step response from the briefing: find the exposed hosts, fix them in the right order, and hunt for signs they were hit first.

- **📄 [Read the briefing (PDF)](https://github.com/jtbuchanan-tenb/php2shell-playbook/blob/main/php2shell-response-briefing.pdf)**: Find, fix and hunt PHP2Shell, 7 slides. Share it with your team.
- **▶ Run it: `/php2shell-playbook`**: runs all three steps in Claude Code and saves a handoff file after each.

## PHP2Shell at a glance

| | |
|---|---|
| **9.2** | CVSS v4.0 on both CVEs, no login needed |
| **1.3M+** | Internet-facing hosts that may be vulnerable |
| **Oct 17** | First exploitation attempt seen, four days before disclosure |
| **8.1 and older** | No official fix: upgrade |

**Fixed releases:** 8.5.12 · 8.4.27 · 8.3.36 · 8.2.35

**Interim only, until you can patch:** `memory_limit=-1` and `session.upload_progress.enabled=0`, then restart every PHP worker. On PHP 8.5, also set `fatal_error_backtraces=0`.

Source: Tenable Research PHP2Shell FAQ, Oct 21, 2026. The [FAQ](https://www.tenable.com/blog/php2shell-cve-2026-109618-cve-2026-109619-frequently-asked-questions-about-critical-php-remote) is updated continuously, so check it for current guidance. The playbook re-reads it on every run.

## What it does

### Step 1: Find it. Where are we exposed?

**PHP2Shell Tenable Skill** pulls PHP2Shell findings and PHP inventory from Tenable One through Hexa AI MCP, grades every asset against the fixed PHP releases, and writes an HTML, PDF and CSV report naming the ten worst assets.

### Step 2: Fix it. What do we fix first?

**Remediation Priority & Impact Agent** ranks the hosts from step 1 by Asset Exposure Score, confirmed exploitation and attack path, as a FIRST / NEXT / SOON plan with Tenable's exact fix for each. The playbook keeps only PHP2Shell hosts and CVEs, and lists anything else as out of scope.

### Step 3: Hunt for it. Were we hit before we patched?

**SOC-Hunter** hunts for exploitation since Oct 17. It covers every host Tenable saw running PHP, patched ones included, and looks for PHP workers starting shells, `curl` or `wget`, new `.php` files under web roots, and outbound connections from PHP workers, across your SIEM, EDR and Tenable data. No SIEM or EDR connected? The playbook writes a hunt kit of ready-to-paste searches for Splunk, Microsoft Defender XDR / Sentinel and Elastic, plus a manual checklist.

## How it works

`/php2shell-playbook` runs the three skills in order. After each step it writes a handoff file, in Markdown and JSON, and asks before going on. The vulnerability manager can stop after Fix it, and the SOC lead picks up from the handoff with `/php2shell-playbook hunt <run folder>`. The playbook only reads data: it never patches, scans or changes anything in Tenable, a SIEM, an EDR or a host.

## Run all three today

1. Connect Tenable Hexa AI MCP. The playbook walks you through it if it's missing.
2. Install the three skills and this playbook (see the README). The playbook offers to install any skill that's missing.
3. Run `/php2shell-playbook`. Stop after any step; whoever runs the next step picks up from its handoff file.
