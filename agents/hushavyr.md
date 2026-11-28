---
name: "Hushavyr"
author: "mathias82"
github_url: "https://github.com/mathias82/Hushavyr"
description: "Local AI code review and defensive application security scanning for VS Code and the terminal."
license: "MIT"
tier: "contributed"
tags: ["local-ai", "code-review", "static-analysis", "devsecops"]
domains: ["application-security"]
integrations: ["GitHub", "Google OSV"]
date_added: 2026-11-28
contribution_agreement_date: 2026-11-28T10:14:46Z
works_with_tenable_hexa_mcp: false
---

## What it does

Hushavyr helps developers and application security teams review source code from VS Code or the terminal. It reports potentially insecure code patterns, exposed secrets and vulnerable dependencies. Findings include source locations and supporting evidence when available, so developers can inspect the result before taking action.

## How it works

Built-in static rules and secret checks can run without a model. Optional local analyzers, including OSV-Scanner, extend dependency and language coverage. For AI-assisted review, Hushavyr uses a locally running Ollama model to add context and propose changes. Developers review a diff and explicitly approve edits before they are applied. External actions such as opening a GitHub pull request require user approval.

The repository README documents setup, analyzer prerequisites, language coverage, model requirements and the data involved in optional external actions.
