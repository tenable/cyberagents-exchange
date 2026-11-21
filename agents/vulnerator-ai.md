---
name: "Vulnerator AI"
author: "irraz"
github_url: "https://github.com/irraz/vulnerator-ai"
description: "Autonomous OODA agent for authorized pentesting: a demonstrate-impact mode that stops at proof, scope-guarded to targets you may test."
license: "MIT"
tier: "contributed"
tags: ["pentest", "ooda", "mcp", "kali", "authorized-testing", "scope-guard", "llm-agent"]
domains: ["application-security", "vulnerability-management"]
integrations: ["AWS"]
date_added: 2026-10-19
contribution_agreement_date: 2026-10-19T16:01:27Z
---

Vulnerator AI is a minimal, containerized agent for **authorized security testing**. It runs an
OODA (Observe–Orient–Decide–Act) loop where Hermes (Nous Research) reasons about the engagement and
drives a curated Kali toolset through an MCP server. It is built for engagements you own or have
explicit written permission to test, run in a controlled environment.

## What it does

- Automates an authorized-pentest OODA loop end to end — reconnaissance, web testing, and
  vulnerability discovery — using ATT&CK as the orientation language of the loop.
- Supports an explicit engagement mode. In **pentest mode** the agent's goal is to demonstrate
  impact, not to exploit: it advances only until it has evidence of exploitability (a confirmed
  crash, a verified CVE, a documented CVSS) and then stops to produce a report with the vulnerability,
  the vector, the affected and patched versions, and a recommendation — it does not build exploits or
  obtain a root shell unless the operator explicitly asks. A separate red-team/CTF mode is available
  for full-compromise lab and CTF work.
- Runs a curated Kali toolset (nmap, whatweb, nuclei, ffuf, sqlmap, Prowler, and more) over a
  `kali-mcp` server, plus a real headless-Chromium browser over `playwright-mcp` for web testing.
- Keeps the operator in control through a thin `vulnerator-mcp` front door: MCP clients
  (Claude Code, Kiro, and similar) can trigger, observe, steer, and stop a run through the runs
  lifecycle only — never raw tool execution.
- Includes a built-in practice lab (OWASP Juice Shop) and a sample redacted deliverable so the
  workflow can be exercised safely before any real engagement.

## How it works

Four containers cooperate: `ooda-agent` (Hermes as the OODA driver), `kali` (the deterministic
tool runtime over `kali-mcp`), `playwright-mcp` (browser surface), and `vulnerator-mcp` (the MCP
front door over Hermes' runs API). Hermes reasons over an OpenRouter-hosted model and acts through
the MCP servers against targets the operator declares as authorized at the start of the engagement.

To keep testing within authorized bounds, the engine ships an **opt-in scope-guard**: an
allow/deny policy by CIDR, host, and port that every `kali_run`/`kali_exec` call is validated
against before execution. With the scope active, the agent must declare its authorized `targets`,
and any destination outside the allow-list (or in the deny-list) is blocked without running. A
separate inbound token gates reachability of the MCP front door. Responsibility for defining scope
and for lawful, authorized use rests with the operator.
