---
last_reviewed: 2026-09-03
name: "Tenable SSL & TLS - Compliance Dashboard"
author: "rafansmpj"
github_url: "https://github.com/rafansmpj/tenable-ssl-tls-compliance-dashboard"
description: "SSL/TLS compliance dashboard from Tenable Hexa MCP: flags deprecated protocols, weak ciphers, and certificate issues."
license: "MIT"
tier: "contributed"
tags: ["ssl-tls", "compliance", "certificate", "dashboard", "encryption", "tenable", "pci-dss"]
domains: ["cryptography-pki"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-07-27
contribution_agreement_date: 2026-08-30T23:25:18Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code", "Claude Desktop"]
invocation: "/tenable-ssl-tls-compliance-dashboard"
---

A Claude Code/Desktop skill that connects to your Tenable environment via the Hexa AI MCP and delivers a complete SSL/TLS compliance picture as a standalone HTML dashboard — directly in the conversation. Read-only: no certificates are replaced, no services are restarted, no configuration is modified.

## What it does

Analyzes SSL/TLS configuration across your Tenable environment using eight targeted plugins (56984, 10863, 15901, 42981, 57582, 35291, 86067, 45411). It identifies deprecated protocols (SSLv2, SSLv3, TLS 1.0, TLS 1.1), weak cipher suites (RC4, DES/3DES, NULL, export, anonymous), missing Perfect Forward Secrecy, and certificate issues including expired, self-signed, expiring soon, weak signature/key (SHA-1, MD5, RSA < 2048 bits), and wrong hostname. Crown Jewel assets are surfaced using Tenable tags or ACR scores so remediation can target the highest-impact assets first.

## How it works

The skill orchestrates a multi-step MCP data collection: aggregate finding counts via `workbenches_list_vulnerabilities`, detailed host samples via `workbenches_get_vulnerability_outputs`, Crown Jewel identification via tagging or ACR fallback, and asset enrichment via `tenable_one_search_assets`. Results are rendered into a two-tab standalone HTML dashboard — an Overview tab with summary cards, protocol distribution chart, certificate breakdown donut, and prioritized recommendations; plus an Applicable Assets tab with interactive filters, sortable columns, and per-asset detail drawers.
