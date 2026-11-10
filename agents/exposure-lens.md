---
name: "Exposure Lens"
author: "yukselao"
github_url: "https://github.com/yukselao/exposure-lens"
description: "Identity-aware, AI-assisted vulnerability management for on-prem Security Center and Identity Exposure."
license: "MIT"
tier: "contributed"
tags: ["security-center", "identity-exposure", "active-directory", "attack-path", "local-llm", "ollama", "on-premises"]
domains: ["identity-access", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-11-10
contribution_agreement_date: 2026-11-10T20:56:37Z
---

Exposure Lens brings identity context to on-premises vulnerability management. It pulls data from Tenable Security Center and Tenable Identity Exposure into PostgreSQL and links every vulnerable host to the identities that can reach it. Agent Tenable, a chat assistant running on a local LLM through Ollama, answers questions about that data, so nothing leaves the environment. It is built for teams that cannot use the cloud features of Tenable One because of regulation or data residency.

A 7-minute demo video is in the repository README.

## What it does

- **Dashboard:** vulnerabilities, risky identities, users reaching critical hosts, hosts under Tier 0 accounts and service accounts on critical hosts, each with an explanation of how it is calculated.
- **Identity-to-host correlation:** parses Nessus plugin output (logged-on users, local administrators, services, sessions) and matches each name to Active Directory by SID, name, UPN and host domain, with the evidence and match quality for every link.
- **Risk:** joins each host's findings, Asset Criticality Rating and AD tier to every identity that can reach it.
- **Asset Details:** one page per identity or host with connected systems, vulnerabilities grouped by host or CVE, a risk score with its factors, correlation evidence and group membership paths.
- **Agent Tenable:** a chat assistant (Turkish or English) that investigates a user or host with read-only database tools and selectable skills (Exposure Analyst, Vulnerability Analyst, AD Administrator, Offensive Security point of view), and links every value to the screen that shows it.
- **Explore:** AD objects, hosts, findings, local users, software inventory and browser extensions.

## How it works

Docker Compose runs PostgreSQL, a Security Center connector (pyTenable, read-only), an Identity Exposure connector, a CTEM worker that extracts identities from plugin output and builds the correlation and risk read models, and a PHP web UI behind nginx. The UI and the connectors communicate through a job table; syncs mirror the sources on a schedule or on demand. Agent Tenable calls a local Ollama server (tested with `gemma4:31b`); its tools are read-only SQL queries with statement timeouts. API keys live in `.env`, Docker secrets or encrypted in the database, never in the repository. Exposure Lens is a community project and is not an official Tenable product.
