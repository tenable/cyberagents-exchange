---
last_reviewed: 2026-08-19
name: "Tacklebox"
author: "TL-Chamber"
github_url: "https://github.com/TL-Chamber/tacklebox"
description: "Multi-layered phishing email analysis skill for static analysis, threat intel, blast radius, and IOC extraction. Nothing is executed."
license: "MIT"
tier: "contributed"
tags: ["phishing", "email-analysis", "threat-intelligence", "soc", "ioc", "malware-detection"]
integrations: ["Anthropic", "AWS", "Mimecast", "URLScan.io", "VirusTotal"]
date_added: 2026-08-14
contribution_agreement_date: 2026-08-14T19:45:44Z
compatible_platforms: ["Claude Code"]
invocation: "/tacklebox"
---

A Claude Code skill for triaging reported phishing emails through eight layers of static analysis and threat intelligence. It never executes attachments, visits URLs, or opens suspicious files. All analysis is static parsing, API lookups, hash identification, and pattern matching.

## What it does

Tacklebox walks through up to eight analysis layers: email header parsing and authentication validation (SPF/DKIM/DMARC), static content analysis, obfuscation detection (zero-width characters, CSS hiding, homoglyphs), AI agent targeting detection (prompt injection aimed at mail-reading assistants), VirusTotal and URLScan.io threat intelligence, optional email gateway blast radius via Mimecast, and risk scoring. Output is a 0-13+ risk score with every supporting signal listed, plus blocklists ready to paste into your email gateway and web proxy.

## How it works

Layers 1-5 run fully offline with no configuration. Add API keys for VirusTotal and URLScan.io to unlock threat intelligence. Configure Mimecast credentials to answer who else received the email and whether anyone clicked through. An optional isolated attachment viewer uses AWS SSM to open suspicious files on a remote EC2 instance so they never touch the analyst's workstation.
