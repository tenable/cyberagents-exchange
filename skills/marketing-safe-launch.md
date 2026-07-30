---
name: "Marketing Safe Launch"
author: "Meg-CMO"
github_url: "https://github.com/Meg-CMO/marketing-safe-launch"
description: "Passive, read-only pre-launch attack-surface review of a marketing campaign that outputs an executive launch verdict."
license: "MIT"
tier: "contributed"
tags: ["marketing-security", "attack-surface", "osint", "pre-launch", "lookalike-detection", "passive-recon"]
integrations: []
date_added: 2026-07-30
contribution_agreement_date: 2026-07-30T20:43:30Z
compatible_platforms: ["Claude Code"]
invocation: "/marketing-safe-launch"
---

Marketing teams stand up campaign microsites, landing pages, forms, tracking
pixels, and martech integrations quickly — often outside normal security
workflows. Marketing Safe Launch gives a campaign owner a fast, defensible
answer to *"is this safe to launch?"* using only publicly observable
information, and delivers it as a single self-contained HTML report.

## What it does

Starting from a campaign's primary domain, the skill runs a **passive,
read-only** attack-surface review and produces an executive verdict —
**Ready**, **Ready with exceptions**, or **Hold** — with the reasoning shown:

- **Asset discovery** — enumerates subdomains and third parties (Certificate
  Transparency, DNS, page/header reads) and inventories scripts, tracking
  pixels, forms, and martech vendors.
- **Lookalike detection** — generates typo, omission, homoglyph, TLD-swap, and
  brand-keyword permutations and flags those that resolve or are mail-capable.
- **Passive risk findings** — surfaces observable issues (exposed dev/staging
  subdomains, missing security headers, software disclosure, non-TLS forms,
  certificate problems, risky third-party integrations), prioritized by a
  severity rubric.
- **Owner routing** — suggests an owner (Marketing / IT / Security / vendor) for
  each finding, as a label only — no tickets or email are sent.

## How it works

The skill follows a strict passive OSINT playbook using standard tooling
(`dig`, `whois`, `curl`, `openssl`, and public Certificate Transparency logs).
It never port scans, vulnerability scans, fuzzes, brute forces, or attempts to
exploit anything — every finding is indicative, and each report discloses
exactly which techniques were run against which domains. The output is a
self-contained HTML report (verdict banner, severity counts, asset inventory,
prioritized findings, lookalike domains, an attack-path narrative labeled as
inference, and a methodology/limitations section) that opens in any browser with
no server or network access required.
