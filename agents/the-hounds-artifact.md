---
name: "The Hounds — Artifact"
author: "packetchaos"
github_url: "https://github.com/packetchaos/the-hounds-artifact"
description: "Single-file console artifact that runs The Hounds exposure-management pack over Tenable navi via navi-mcp."
license: "MIT"
tier: "contributed"
tags: [tenable, exposure-management, navi, artifact, console, vulnerability-management]
integrations: [Tenable, Anthropic]
date_added: 2026-07-15
contribution_agreement_date: 2026-07-15T18:28:01Z
---

The Hounds — Artifact packages everything needed to stand up the single-file **navi agent
console**: a self-contained SPA (`navi-agent-console.html`) wired to navi through the
navi-mcp server, plus the routing skills that let an AI assistant switch between the
Tenable official MCP and navi correctly.

## What it does

It provides a ready-to-run console for "The Hounds" — a pack of exposure-management
specialists that hunt CISA KEV exposure, certificates, attack paths, IoT/OT, AI inventory,
EOL software, and more over your Tenable data. The console surfaces per-hound findings and
proposes navi tag/ACR writes for human approval. An `artifact-import-prompt.md` lets you
recreate or import the artifact into a compatible client.

## How it works

Open `navi-agent-console.html` in the client (or import it via the paste-in prompt), then
install the bundled `tenable-toolkit` (toolkit + preflight + tagging) and `the-hounds`
skills so the assistant routes between the Tenable official MCP and navi. All navi queries
stay grounded in real data and every write is gated behind explicit confirmation.
