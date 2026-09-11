---
name: "PDF Analyzer"
author: "mostafahussein"
github_url: "https://github.com/mostafahussein/pdf-analyzer"
description: "Multi-layered static analysis and sanitization for suspicious PDFs with threat intelligence integration."
license: "MIT"
tier: "contributed"
tags: ["pdf-analysis", "malware-analysis", "static-analysis", "pdf-sanitization", "threat-intelligence", "incident-response", "ioc-extraction"]
integrations: ["VirusTotal"]
date_added: 2026-09-11
contribution_agreement_date: 2026-09-11T18:06:45Z
compatible_platforms: ["Claude Code"]
invocation: "/pdf-analyzer"
---

PDF Analyzer dissects suspicious PDFs through six layers of static analysis and threat intelligence. It never renders a PDF, never executes JavaScript, and never opens embedded files.

## What it does

- **Six analysis layers:** structure parsing, action detection, JavaScript detection, embedded content cataloging, obfuscation detection, and VirusTotal hash reputation lookup
- **Cleaning and sanitization:** strips malicious elements (OpenAction, JavaScript, embedded files, dangerous URI schemes) and outputs a safe copy while preserving document layout
- **IOC extraction:** hashes, URLs, and embedded filenames ready to feed into detection tools
- **Risk scoring:** evidence-based verdict (LOW/MEDIUM/HIGH/CRITICAL) with per-layer breakdown

## How it works

All analysis is static - files are read as raw bytes, parsed with regex and heuristics, and never rendered or executed. VirusTotal integration performs hash-only lookups (the file is never uploaded). Cleaning is powered by pdf-defang for proper PDF parsing, with additional custom sanitization for URL defanging in annotations and content streams.
