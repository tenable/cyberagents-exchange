---
name: "Tenable Cloud Exposure PQC Posture Portal"
author: "chanochm"
github_url: "https://github.com/chanochm/Tenable-CloudSecurity-PQCPosture"
description: "Self-hosted web portal showing post-quantum cryptography readiness for cloud resources using Tenable Cloud Exposure's native SSL/TLS PQC telemetry."
license: "MIT"
tier: "contributed"
tags: ["post-quantum-cryptography", "pqc", "tls", "cryptography", "cloud-security", "cloud-exposure", "network-exposure", "dashboard", "vulnerability-management"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-08-04
contribution_agreement_date: 2026-08-04T10:28:43Z
works_with_tenable_hexa_mcp: true
---

A self-hosted web dashboard that answers a single critical question: *which of our internet-reachable cloud resources would survive a quantum adversary?*

## What it does

PQC Posture Portal visualizes post-quantum cryptography readiness across your entire cloud estate by consuming Tenable Cloud Exposure's native `SSL/TLS PQC Support` telemetry. It scores every exposed resource — `Enforced`, `Ready`, `Review`, or `Not quantum-safe` — and presents the results through two views:

- **Dashboard:** Readiness ratio, endpoint lattice visualization, and seven summary widgets mapping to capabilities from Tenable's Cryptographic Inventory dashboard (services using/not using PQC, cipher inventory, TLS weaknesses, certificate expiry, and countdown to Executive Order 14412 migration deadlines)
- **Resource inventory:** Filterable table with cryptographic drill-down per endpoint, showing offered key-exchange groups with post-quantum algorithms highlighted

Zero dependencies beyond Python's standard library. No pip install, no Node, no external network calls. One HTML file, vanilla JavaScript, and direct MCP JSON-RPC communication with Tenable Cloud Exposure via the Tenable Hexa MCP server.

## How it works

The portal runs a local HTTP server (`ThreadingHTTPServer`) that serves a single-page application and queries Tenable Cloud Exposure through the Tenable Hexa AI MCP server. It speaks MCP JSON-RPC over HTTPS directly — no AI client needed at runtime, no model in the data path.

Verdicts are recomputed server-side on every request from raw endpoint fields stored in saved UDM queries (`queries/*.json`). Service account credentials are encrypted at rest with a per-install key file using PBKDF2-derived HMAC-SHA256. Corporate TLS-inspecting proxies are handled automatically by resolving trust from the OS certificate store (macOS keychains via `security`, Windows stores via `ssl.enum_certificates`).

Designed for distribution: works offline with bundled demo data, handles schema drift explicitly with a legacy query fallback, and requires no manual certificate configuration on networks with MDM-installed corporate roots.
