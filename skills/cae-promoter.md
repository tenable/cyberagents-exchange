---
name: "CAE Promoter"
author: "nh010"
github_url: "https://github.com/nh010/cae-promoter"
description: "A Claude Code skill that coaches CyberAgents Exchange contributors to promote a published agent, skill, MCP server, or playbook — on-brand copy, video scripts, and leaderboard optimization."
license: "MIT"
tier: "contributed"
tags: ["claude-code", "exchange", "promotion", "marketing", "cybersecurity"]
integrations: ["Anthropic"]
date_added: 2026-07-20
contribution_agreement_date: 2026-07-20T16:00:27Z
compatible_platforms: ["Claude Code"]
invocation: "/cae-promoter"
---

A Claude Code skill whose users are other CyberAgents Exchange contributors. It coaches them to
promote an already-published asset — on the Exchange (win stars, hit Rising 🚀, climb the
leaderboard) and externally — then packages an on-brand promo bundle locally. (Not yet listed? Use
`cyberagents-exchange-submit` first.)

## What it does

- Interviews you for quantifiable value statements, then drafts channel-specific promo copy (LinkedIn, X, Slack, listing/README) led by those results
- Scripts a 30–60s promo clip (your name, title, organization, asset, PR number, and a brief what/why) and a 2–3 min demo outline for you to record through a shared Riverside link; the team edits and hosts it
- Optimizes your listing and README against real leaderboard mechanics (stars, Rising 🚀) and can help you open a promotion-edit PR from your own GitHub account
- Produces on-brand visual-aid guidance (diagrams, annotated screenshots, share cards)
- Pre-fills the Tenable intake form from your session so you just review and submit it — the one place your details reach the team

## How it works

Install the skill, run `/cae-promoter`, paste your Exchange listing URL and GitHub repo URL, pick
what you want, and it writes a `promo/` bundle into your repo, hands you a pre-filled intake form to
review and submit, and points you at the Riverside link to record. It coaches and drafts; it holds
no Tenable credentials and never acts as Tenable. The two actions it helps with — submitting the
pre-filled intake form and opening the listing PR — are yours: you review and click, on your own
accounts, only with your go-ahead.
