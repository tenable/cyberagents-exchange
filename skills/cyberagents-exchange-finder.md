---
last_reviewed: 2026-11-06
name: "CyberAgents Exchange Finder"
author: "scarnell-tenb"
github_url: "https://github.com/scarnell-tenb/cyberagents-exchange-finder"
description: "Finds and compares live CyberAgents Exchange listings for your security task and tools. Never installs anything."
license: "MIT"
tier: "contributed"
tags: ["exchange", "discovery", "recommendation", "comparison", "trust", "repo-health"]
domains: ["platform-operations"]
integrations: ["Anthropic"]
date_added: 2026-11-06
contribution_agreement_date: 2026-11-06T20:11:16Z
compatible_platforms: ["Claude Code", "Claude Desktop", "Claude Cowork"]
invocation: "/cyberagents-exchange-finder"
---

A finder for the CyberAgents Exchange itself. Describe the security job you're doing and the tools you run, and it returns a short list of live listings worth evaluating, or says plainly that nothing fits.

## What it does

- Reads the Exchange's live index on every request and confirms each pick against its full record. It never answers from memory.
- Maps your words to the Exchange vocabulary ("S1" → SentinelOne, "Tenable.sc" → Security Center), then ranks in a fixed, neutral order: task fit, your tools, security domain, read-only before write-capable, vetted before contributed, runs on your AI tool, lower setup effort. Tenable compatibility never counts as fit by itself.
- Opens with an at-a-glance comparison table (tier, access, setup effort, whether it runs on your AI tool, notes such as "new" or "part of playbook #1"), and an "If you try one" line based only on fit.
- Shows up to 3 **Best matches** as cards (up to 5 on request) and up to 2 **Also related** picks as one-liners that say what each is missing. "details N" expands any pick.
- Expands playbooks: each Exchange step in a playbook's chain gets its own row, and the playbook shows its chain with each step's trust tier.
- For each pick, shows:
  - **Risk:** read-only or what it can change, marked *declared* (from an MCP server's tool list) or *inferred* (from description wording).
  - **Trust:** the Exchange tier. Vetted picks name the exact reviewed commit, and that the review covers that commit only.
  - **Project health** from the Exchange's own repo snapshot: account type, stars, forks, open issues, last push, license.
  - **Warnings:** archived repo, owner differs from the listed author, no recent pushes, code changed since review, reviewed commit missing.
  - **Practical details:** CVEs covered, what you'll need, setup effort and how to invoke it.
- Links only to listing pages on the Exchange. It never installs, configures or asks for credentials.

## How it works

The skill itself is a single `SKILL.md` with no runtime code; the repo's one script only builds the Claude apps zip. It reads the Exchange manifest (`/api/index.json`), fetches every per-type index file it lists in one call, then fetches the detail records for its shortlist. Repo health comes from the Exchange's published snapshot, so a normal search makes no GitHub calls; it checks GitHub's public API only for a pick with no snapshot. It uses `curl` and `jq` where available, other JSON tools or web fetch otherwise, and nothing you type goes into any request.

In Claude Code, `/cyberagents-exchange-finder` runs it on Claude Haiku: typically 45–95 seconds and 1–2 cents per search, with `curl` commands that start with an Exchange or GitHub API URL pre-approved. In Claude Desktop and Cowork, upload `dist/cyberagents-exchange-finder.zip`, which a GitHub Action keeps in step with the repo.

Listing data is treated as untrusted: slugs, repo URLs and commit IDs are pattern-checked before they go into any command, links are built rather than copied, and instructions embedded in listings are ignored. A local copy of the index works on locked-down networks.

It's listed under Platform Operations because its job is helping people find and evaluate Exchange tooling, as an onboarding helper, rather than performing a security function itself.
