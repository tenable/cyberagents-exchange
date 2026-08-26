---
last_reviewed: 2026-08-26
name: "Tenable IaC Finding to PR"
author: "tomabai"
github_url: "https://github.com/tomabai/tenable-iac-finding-to-pr"
description: "A Claude Code skill that turns open Tenable Cloud Security IaC findings into reviewed, mergeable GitHub fix PRs"
license: "MIT"
tier: "contributed"
tags: ["claude-code", "tenable-cloud-security", "iac", "terraform", "remediation", "pull-request"]
integrations: ["Tenable"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T00:00:00Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "/tenable-iac-finding-to-pr"
---

A Claude Code skill that turns open Infrastructure-as-Code (IaC) security findings from Tenable Cloud Security (TCS) into reviewed, mergeable GitHub pull requests. The platform provides the intent of a fix — the policy name and description — and the skill authors the minimal Terraform change itself, then opens a PR whose body links every fix back to the finding in the Tenable console.

## What it does

- Verifies the Tenable Cloud Security MCP server is connected before doing anything, and prints install steps if it isn't
- Fetches open IaC findings for a repository via the TCS MCP (filtered to Open only), asking which repo when you don't name one or letting you sweep all repos with findings
- Surfaces the findings in a compact table — severity, policy, resource/file, and a link back to the platform — so you see exactly what will change before any code is touched
- Authors minimal Terraform fixes targeting the exact named resource, never renaming or removing resources and never fabricating values
- Opens one combined PR or one PR per finding, each with a findings table and per-finding Risk / Remediation Applied sections grounded in the policy

## How it works

The skill is interactive by design and never opens a PR before you've seen the findings and chosen how to split them. It confirms the `TCS` MCP tools are reachable, runs a GraphQL query for `CodeFinding` records, presents them for review, reads each affected file to match the resource by exact name, applies the minimal change the policy requires, then creates the branch, commits, pushes, and opens the pull request — handling common `gh`/`git` gotchas such as account flips and stale credential helpers along the way.
