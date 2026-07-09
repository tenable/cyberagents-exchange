---
name: "ExposureIQ for Tenable One"
author: "nreynolds-pub-git"
github_url: "https://github.com/nreynolds-pub-git/exposureiq"
description: "AI-powered mitigation guidance for Tenable One vulnerabilities with privacy-preserving, self-hosted architecture"
license: "MIT"
type: "tool"
tier: "unreviewed"
tags: ["vulnerability-management", "cve-enrichment", "tenable", "mitigation-guidance", "self-hosted", "privacy-preserving", "fastapi"]
framework: "Custom"
integrations: ["Tenable", "Anthropic", "CrowdStrike", "SentinelOne", "Wiz"]
date_added: 2026-06-30
---

ExposureIQ enriches vulnerability findings from third-party security connectors in Tenable One with AI-powered mitigation guidance. Designed for self-hosted deployment with privacy-preserving architecture—asset identifiers never leave your environment, vendor names are anonymized, and you bring your own LLM API key.

## What it does

- Discovers third-party connectors and assets in Tenable One via documented APIs
- Pulls CVE findings and presents them in a filterable, sortable, exportable React web UI
- Generates structured AI explanations with mitigation-first guidance and source citations
- Caches CVE intelligence and Tenable plugin data locally for faster analysis
- Supports Anthropic Claude and Google Gemini as LLM providers (BYOK)

The killer feature: **mitigation-first AI guidance**. While most vulnerability tools focus on remediation (what to patch), ExposureIQ leads with what defenders can do *right now* to reduce risk before patches can be deployed—addressing the gap between "we know the fix" and "the fix is in production."

## How it works

Built as a FastAPI backend + React frontend, packaged in Docker. The pipeline fetches assets and findings from Tenable One, enriches CVE records by scraping tenable.com/cve/{ID}, matches findings to Tenable plugin remediation data, and stores everything in local SQLite. Privacy guarantees are code-enforced: asset identifiers are stripped before any LLM call, vendor names are mapped to generic categories (EDR, CNAPP, etc.), and API keys live in browser localStorage—never touching the backend.
