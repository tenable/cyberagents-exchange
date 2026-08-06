---
name: "Tenable SSL & TLS - Compliance Dashboard"
author: "rafansmpj"
github_url: "https://github.com/rafansmpj/tenable-ssl-tls-compliance-dashboard"
description: "Interactive read-only SSL/TLS and certificate compliance dashboard built from Tenable scan data."
license: "MIT"
tier: "contributed"
tags: ["tenable", "ssl-tls", "compliance", "certificate-management", "pci-dss", "dashboard"]
integrations: ["Tenable Hexa AI MCP"]
date_added: 2026-07-27
contribution_agreement_date: 2026-07-27T15:59:16Z
works_with_tenable_hexa_mcp: true
compatible_platforms: ["Claude Code", "Claude Desktop"]
invocation: "/tenable-ssl-tls-compliance-dashboard"
---

The Tenable SSL & TLS Compliance Dashboard is a read-only Claude skill that turns
Tenable scan data into an interactive, standalone-HTML executive dashboard for
encryption and certificate compliance. It targets infrastructure and security
engineers, PKI/certificate owners, compliance teams, and CISOs who need an
actionable fix list before an auditor forces the issue.

## What it does

- Analyzes SSL/TLS posture using Plugin 56984 (protocols/ciphers) plus certificate
  plugins 10863, 15901, 42981, 57582, 35291, 86067, and 45411.
- Flags deprecated protocols (SSLv2, SSLv3, TLS 1.0/1.1), weak ciphers (RC4,
  DES/3DES, NULL, export, anonymous), and missing Perfect Forward Secrecy.
- Surfaces certificates that are expired, self-signed, expiring soon, or signed
  with a weak algorithm/key (SHA-1, MD5, RSA under 2048 bits).
- Delivers a compliance overview plus an affected-assets tab, useful for PCI DSS
  4.0, SOC 2, and ISO 27001 preparation.

## How it works

Connects to a Tenable One / Hexa AI MCP server (read-only) to pull live protocol,
cipher, and certificate findings, then renders a standalone HTML dashboard right
in the conversation. It never replaces certificates, disables protocols/ciphers,
or restarts services — every recommendation is text, not an action. With no active
MCP connection it falls back to a clearly labeled DEMO dashboard.
