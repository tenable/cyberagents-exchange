---
name: "GORR (Game Over Risk Reduction)"
author: "rafansmpj"
github_url: "https://github.com/rafansmpj/GORR"
description: "30-day phased plan and ticket tracker to cut the Tenable One Exposure Score with verified Quick Wins."
license: "MIT"
tier: "contributed"
tags: ["tenable-one", "exposure-management", "quick-wins", "remediation-tracking", "exposure-score", "executive-dashboard", "vulnerability-prioritization"]
domains: ["vulnerability-management", "governance-risk-compliance"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-11-23
contribution_agreement_date: 2026-11-23T16:08:38Z
works_with_tenable_hexa_mcp: true
compatible_platforms: ["Claude Code", "Claude Desktop"]
invocation: "/gorr"
---

GORR builds an interactive executive dashboard that shows which vulnerabilities to close, in which order and by which date, to cut the Tenable One Exposure Score across N cumulative phases (2–6, default 4: 10-20-30-40%) inside a 30-day cycle. It ships a CSV/JSON ticket tracker that is re-imported on later runs to verify what was really fixed.

## What it does

- Targets the official Exposure Score from the Tenable One Exposure View API (an uploaded JSON or a fresh pull with the bundled collector), with the computed score as a cross-check.
- Models how each module moves the Global score, Identity Exposure IoEs included.
- Ranks Quick Wins by projected score drop per unit of effort, with Crown Jewel and attack path chokepoint bonuses, keyed on real Tenable plugin IDs.
- Takes the owner of each asset from its Tenable tag, re-read on every run.
- Tracks tickets (owner, ticket #, assignee, status) and, on follow-up runs, shows what is fixed, still open, reopened, new or overdue.
- Flags carry-over from past-due phases with its impact on each phase target and a recovery plan.
- Delivers a gauge, phase cards, progression chart, per-asset, per-plugin, per-owner and carry-over views, peer benchmark and a board-ready summary, in English or Portuguese.

## How it works

The skill reads findings, assets, tags, Crown Jewels and attack paths through the Tenable Hexa AI MCP. It reproduces Tenable's scoring structure (VPR-band severity drives each asset's AES, and the Exposure Score is the average AES), calibrates it against the official score, and greedily assembles the actions that remove the most score points for the least effort into dated phases. Tracker merges are deterministic (`scripts/tracker.py`). The skill is read-only toward Tenable: tickets live in the tracker the team maintains.
