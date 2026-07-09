---
name: "Tenable SC Agent — Security Center Vulnerability Analyst"
author: "ayuksel-tenb"
github_url: "https://github.com/ayuksel-tenb/sc-agent"
description: "A Chrome extension that adds an in-page AI vulnerability analyst to Tenable Security Center, analyzing findings in any language and triggering your own automation playbooks."
license: "BSD-3-Clause"
type: "agent"
tier: "unreviewed"
tags: ["vulnerability-management", "browser-extension", "chatops", "triage", "remediation", "tenable"]
framework: "Anthropic API"
integrations: ["Tenable", "Anthropic"]
date_added: 2026-07-06
---

**SC Agent** turns any Tenable Security Center vulnerability page into a
conversation. It's a Manifest V3 Chrome extension that injects a floating AI
**vulnerability analyst** into Security Center: open a finding, click the shield
in the corner, and ask anything. The agent answers using the vulnerability data
scraped directly from the page — powered by the Anthropic API.

## What it does

- **Analyzes vulnerabilities in any language.** Ask in English, Turkish,
  Spanish, Japanese — the agent reads the on-page finding (plugin, CVEs, CVSS,
  affected hosts, solution) and replies in the language you wrote in.
- **Triggers your own automation.** Define commands in an editable `tools.md`
  (`triage`, `remediation`, `ticket`, or anything you invent). Ask "triage this"
  or "open a ticket" and the agent runs that playbook against the live
  vulnerability data and returns structured, ready-to-use output.
- **Grounds every answer in page context.** The vulnerability title (from the
  `h2.vuln-title` element) and details (from every `div.detail-section`) are
  handed to the model automatically — no copy-pasting or prompting from scratch.
- **Stays out of the way.** A keyword-gated launcher (e.g. shows only on
  `vulndetails` pages) that expands from a compact modal to a full panel, running
  inside a Shadow DOM so it never clashes with Security Center's own UI.

## How it works

A content script detects matching Security Center pages, scrapes the visible
vulnerability data, and streams the conversation to the Anthropic Messages API
through the extension's background service worker. The agent's persona lives in
an editable `agent.md` (default: *Vulnerability Analyst*) and its automation
commands in `tools.md`, both configurable from the extension's settings page.
Bring your own Anthropic API key; everything runs locally in the browser.

See the repository README for install steps, configuration, and a demo video.
