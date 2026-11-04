---
name: "Porygon Mitigator"
author: "ori-astsec"
github_url: "https://github.com/ori-astsec/tenable-porygon-mitigator"
description: "Finds the Tenable findings an attacker can reach through your firewalls and plans the mitigations that stop them."
license: "MIT"
tier: "contributed"
tags: ["exposure-management", "compensating-controls", "attack-path-analysis", "ips-signatures", "cisa-kev", "mcp-server", "claude-code"]
domains: ["vulnerability-management", "network-security"]
integrations: ["Anthropic", "NVD", "Palo Alto", "Tenable"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T18:07:33Z
---

A Claude Code agent for the findings you can't patch tonight. A scanner gives you a list too long to act on. Porygon
Mitigator works out which of those findings an attacker can reach through your firewalls, finds the mitigations that stop
them without breaking allowed traffic, and writes the exact change for a person to approve.

## What it does

- **Narrows the list.** A funnel takes Tenable findings down to high and critical, remotely exploitable, then exposed and
  on CISA's known-exploited list, and ends with what the recommended plan leaves unmitigated.
- **Maps the network.** It joins firewall rules, routes and assets, and shows every open path from an attacker zone. A host
  it can't judge reads as unknown, never as safe.
- **Finds mitigations.** It looks up documented workarounds and IPS signatures, and keeps a claim only if its quote appears
  in the source.
- **Simulates before asking.** It tries each mitigation on a copy of the network, and holds any that would break allowed
  traffic for a person to decide.
- **Keeps a person in charge.** The agent can't apply anything. A person approves a plan by its hash, then verification
  checks allowed traffic still passes, and rollback restores the config.

## How it works

A Claude Code plugin with an agent, skills and a Python MCP server over stdio, plus a CLI on the same core. Code computes
reachability, verdicts, plans and verification. Claude reads scanner text and explains the results, and what it reads can
only add exposure, never clear a finding.

Run it on the bundled synthetic network with no keys:

`claude --plugin-dir . --agent porygon-mitigator:porygon`

Then ask it to run the whole flow up to approval.

## Limitations

- It has run end to end on a live Tenable partner lab tenant, on 160 hosts and 99,726 findings. That tenant has no firewalls
  in front of its hosts, so the network around those findings was modeled.
- Applying a plan goes to a local PAN-OS test firewall, so you can rehearse it safely. It refuses any other address, so no
  real device changes.
- `porygon panos collect` reads a Palo Alto firewall or Panorama and can't write to it. It's tested against XML API answers
  shaped like a real device's.
- Whether a signature catches an exploit is assumed, not tested. A mitigation buys time and isn't a fix.

## Data flows

- Anthropic API: CVE IDs, advisory text and scanner text, using your key.
- CVE.org, NVD, CISA, OSV, vendor and distro advisory sites, and public rule catalogues: read-only fetches by CVE ID.
- Tenable (optional): your tenant's asset and vulnerability exports, using your keys. Writing a tag or a rescan needs an
  explicit flag.
- Palo Alto (optional): read-only collection from a firewall you name, and Threat Vault lookups using your key.
- No telemetry. Every outbound host is listed in the README.
