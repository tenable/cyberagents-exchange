---
name: "AI Secret Scanner"
author: "SDSicuritech"
github_url: "https://github.com/SDSicuritech/TenableAITokenSearch"
description: "Scans authorized web apps for exposed AI and cloud API keys in client-delivered HTML and JavaScript."
license: "MIT"
tier: "contributed"
tags: ["secrets-detection", "api-keys", "appsec", "exposure-management", "vulnerability-assessment"]
integrations: ["Anthropic", "AWS"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T19:02:31Z
compatible_platforms: ["Claude Code"]
invocation: "/ai-secret-scanner"
---

Front-end code routinely ships provider credentials to the browser. This skill
finds those exposures across assets you own and reports them in a form that is
safe to store and act on.

## What it does

Fetches each authorized target's HTML and linked JavaScript, then matches
credential shapes for OpenAI, Anthropic, Google/Gemini, Hugging Face, AWS access
key IDs, Stripe live keys, GitHub tokens, Slack bot tokens, JWTs, and generic
`api_key = "..."` assignments. Results land in a spreadsheet with source asset,
key type, masked value, fingerprint, and a remediation note.

## How it works

Scanning is gated on an explicit `--scope` host allowlist — the skill refuses to
run without one and skips any target or linked script outside it. Findings are
never written in plaintext: each becomes a short non-sensitive prefix, a
length-preserving mask (`sk-ant******(len=53)`), and a truncated SHA-256
fingerprint that lets you correlate the same leaked key across assets. TLS
verification stays on unless explicitly disabled. Detection only — it offers no
way to test whether a discovered key is live.
