---
name: "Tenable Asset EOL Tracker"
author: "djames-tenb"
github_url: "https://github.com/djames-tenb/tenable-asset-eol-tracker"
description: "Self-hosted web portal that syncs Tenable VM assets and tracks OS and application end-of-life status across five interactive views — zero dependencies, instant load, encrypted credentials"
license: "MIT"
type: "tool"
tier: "unreviewed"
tags: ["eol", "vulnerability-management", "asset-management", "end-of-life", "tenable-vm", "python", "endoflife-date", "lifecycle", "patch-management", "dashboard", "software-inventory", "cpe", "os-lifecycle", "security-operations"]
framework: "Python + SQLite"
integrations: ["Tenable"]
date_added: 2026-06-20
---

A self-hosted web dashboard that pulls all assets from a Tenable VM or Tenable One tenant and correlates them with lifecycle data from [endoflife.date](https://endoflife.date), giving security teams instant visibility into which assets are running end-of-life operating systems or applications.

## What it does

- Syncs all assets from one or more Tenable VM / Tenable One tenants using the Assets Export API (no 5 000-asset cap) — scoped to VM scanner sources only, assets last seen within 90 days, including OS strings, installed-software CPE data, and asset tags
- Maps each OS and application to the corresponding endoflife.date product lifecycle entry and classifies assets as **EOL**, **EOL Soon** (within 90 days), **Supported**, or **Unknown**
- Caches all Tenable data and EOL cycle data in a local SQLite database so every page loads instantly with no live API calls
- Supports multiple tenants in a single instance with credentials encrypted at rest using PBKDF2 + XOR with a per-install key file
- Provides **five views**, all filterable by asset tag: an interactive OS EOL dashboard, an Asset Inventory with per-asset drill-down, an OS EOL page, an Application EOL page, and a Software Inventory page

## How it works

The app is a single Python file (`app.py`) that runs a `ThreadingHTTPServer` — no framework, no external libraries, no pip install. On **Sync**, it:

1. Calls Tenable's `POST /assets/export` API to download all assets in parallel chunks
2. Fetches asset tags from the Tenable Tags API and joins them to each asset
3. Refreshes lifecycle data from endoflife.date for every mapped OS and application product
4. Parses OS strings and CPE 2.3/2.2 strings using a curated mapping of 100+ vendor:product entries, with per-product version normalizers to handle quirks (build numbers, CalVer dates, service-pack suffixes)
5. Runs a four-pass matching algorithm (exact → prefix → qualifier-stripped → reverse prefix) against endoflife.date cycle data
6. Persists everything to SQLite — surviving restarts with no re-fetch needed

The frontend is a single-page `index.html` with vanilla JavaScript — no build step, no Node.js.

## Dashboard highlights

The **OS EOL Overview** dashboard gives security teams three analytical widgets beyond the basic summary counts:

- **Upcoming EOLs** — OS versions expiring within 180 days, sorted by urgency with colour-coded countdowns (red ≤ 30 days, orange ≤ 90 days)
- **Top EOL OS Versions** — ranked list of the OS versions with the most EOL / EOL-Soon assets, with a split bar showing proportion
- **EOL by Tag** — stacked bar comparing EOL status across tag values for any selected tag category (e.g., Production vs Dev vs Staging)

Each summary card is clickable and navigates to the OS EOL page with the matching status and tag filter pre-applied.

## Asset drill-down

Clicking any row in the Asset Inventory opens a full detail panel showing identity attributes, scan metadata, ACR and AES risk scores, the complete EOL analysis (one row per matched product/cycle), Tenable asset tags, and the raw CPE software inventory.
