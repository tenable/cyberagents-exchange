---
name: "CyberAgents Exchange Submit for Claude Desktop & Cowork"
author: "jtbuchanan-tenb"
github_url: "https://github.com/jtbuchanan-tenb/cyberagent-exchange-submission-builder-claude-desktop"
description: "Claude Desktop and Cowork skill that validates your repo and opens CyberAgents Exchange PRs, including repos with several listings."
license: "MIT"
tier: "contributed"
tags: ["claude-desktop", "cowork", "exchange", "submission", "automation", "multi-listing"]
domains: ["platform-operations"]
integrations: ["Anthropic"]
date_added: 2026-11-03
contribution_agreement_date: 2026-11-03T23:35:27Z
compatible_platforms: ["Claude Desktop", "Claude Cowork"]
invocation: "/cyberagents-exchange-submit-desktop"
---

The Claude Desktop and Cowork edition of the CyberAgents Exchange submission builder. It takes someone from "I have a project on GitHub" to open Exchange pull requests without a terminal or Claude Code, working inside the cloud sandbox those apps run in. It is the sibling of the Claude Code skill listed as CyberAgents Exchange Submit, and applies the same Exchange rules.

## What it does

- Checks what the current session can reach and walks the person through connecting GitHub: linking GitHub to Claude, installing the Claude GitHub App, or falling back to their own browser, with EMU account detection.
- Clones the project and scans the working tree and full git history for credentials (values always redacted) before any repo is made public, then checks the license (including the Tenable, Inc. copyright rule for Tenable employees), README, install instructions and archive policy.
- Inventories every listable component in a repository: skills and plugin bundles, MCP servers with their runtime, transport and tools, n8n workflows and subagents.
- Recommends one repository per listing; when the person confirms an exceptional case it plans one listing per component with subfolder github_url values and sibling cross-references, following the SentinelOne precedent.
- Interviews for metadata using the live controlled vocabularies, validates each listing with the Exchange's own validator.py plus the Tier 1 checklist, and opens one branch and pull request per listing after the person confirms.

## How it works

The skill is a SKILL.md with reference files that Claude reads at each stage and standard-library Python scripts, so it runs even in sandboxes where package registries are blocked. Scripts probe the environment, detect components, scan for secrets and run the Exchange validator against a clone of tenable/cyberagents-exchange. GitHub work uses the gh CLI where it is fully available and REST-only calls through the session's GitHub gateway otherwise. It is installed by uploading the release zip in Claude's Skills settings, or used directly by asking Claude to fetch the repository and follow its SKILL.md. It only talks to GitHub.
