---
name: "CyberAgents Exchange Submit"
author: "jtbuchanan-tenb"
github_url: "https://github.com/jtbuchanan-tenb/cyberagent-exchange-submission-builder"
description: "A Claude Code skill that guides you through submitting agents, MCP servers, and playbooks to the Tenable CyberAgents Exchange"
license: "MIT"
tier: "unreviewed"
tags: ["claude-code", "exchange", "submission", "automation", "cybersecurity"]
integrations: ["Anthropic"]
date_added: 2026-05-28
compatible_platforms: ["Claude Code"]
invocation: "/cyberagents-exchange-submit"
---

A Claude Code skill that automates the entire process of submitting your cybersecurity agent, MCP server, or playbook to the Tenable CyberAgents Exchange.

## What it does

- Validates your repository meets Exchange requirements (GitHub remote, README, license)
- Interviews you to generate a complete listing metadata file with auto-detection of fields where possible
- Handles the GitHub workflow: forks the exchange content repo, places your listing, and opens a pull request

## How it works

Install the skill into your Claude Code skills directory, then invoke it from within your agent's repository. The skill walks you through three phases: repo validation, listing generation (with live schema fetching from the exchange repo), and PR submission. It detects EMU accounts, validates integrations against the official list, and confirms before any git operations.
