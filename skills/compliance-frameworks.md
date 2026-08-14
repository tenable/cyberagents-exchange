---
name: "Compliance Frameworks"
author: "jchristian-tenb"
github_url: "https://github.com/jchristian-tenb/compliance-frameworks"
description: "A reference guide explaining major security audits and compliance frameworks — what they are, who needs them, and what they cover."
license: "MIT"
tier: "contributed"
tags: ["compliance", "security-audits", "frameworks", "governance", "risk-management", "GRC"]
integrations: ["Anthropic"]
date_added: 2026-07-22
contribution_agreement_date: 2026-07-22T00:00:00Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "/compliance-frameworks"
---

Provides on-demand, structured reference guides for 22 major security audit and compliance frameworks.

## What it does

When invoked with a framework name (e.g., `/compliance-frameworks FedRAMP`), it delivers a practitioner-focused breakdown covering what the audit is, who needs it, what it covers, and key operational details including frequency, cost, duration, and common pitfalls.

When invoked without arguments, it presents a numbered menu of all supported frameworks and asks the user to select one.

## How it works

The skill uses a prompt-driven approach — no external API calls or tools required. It encodes structured guidance for each framework and generates detailed explanations following a consistent format: What It Is, Who Needs It, What It Covers, and Key Details. It covers frameworks spanning attestations (SOC 2), certifications (ISO 27001), regulations (GDPR, HIPAA), and government authorizations (FedRAMP, CMMC).
