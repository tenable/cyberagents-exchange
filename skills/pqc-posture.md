---
name: "PQC Posture"
author: "knethteo"
github_url: "https://github.com/knethteo/pqc-posture"
description: "Post-Quantum Cryptography readiness skill and dashboard for Tenable Vulnerability Management — type /pqc-posture in Claude Code for an instant fleet posture summary"
license: "MIT"
tier: "contributed"
tags: ["pqc", "post-quantum", "cryptography", "vulnerability-management", "dashboard", "tenable"]
integrations: ["Tenable"]
date_added: 2026-06-22
compatible_platforms: ["Claude Code"]
invocation: "/pqc-posture"
---

PQC Posture is a Claude Code skill (`/pqc-posture`) and web dashboard that gives security teams visibility into Post-Quantum Cryptography readiness across their asset fleet, powered by Tenable Vulnerability Management data.

## What it does

- `/pqc-posture` slash command — starts the server, fetches the fleet, and prints a live PQC posture summary (not-safe / safe / review counts and top at-risk hosts) directly in Claude Code
- Fleet-level web dashboard of assets with PQC-related vulnerability findings
- Per-asset detail showing specific PQC plugin hits
- Truncated plugin outputs with direct links to the Tenable console

## How it works

PQC Posture queries the Tenable Workbench API using a configurable set of PQC plugin IDs. Results are cached in memory for 10 minutes and served via a FastAPI backend. The skill starts the server automatically and can also be run standalone with `uvicorn` or packaged as a Docker container.
