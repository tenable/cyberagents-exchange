---
last_reviewed: 2026-10-13
name: "Patronus Security"
author: "patronus-protect"
github_url: "https://github.com/patronus-protect/patronus-security-cli"
description: "Local-first prompt injection, PII and DLP checks for AI agents, with CLI scans and runtime protection."
license: "Apache-2.0"
tier: "contributed"
tags: ["prompt-injection", "ai-agent-security", "mcp-security", "pii", "dlp", "local-first"]
domains: ["ai-security", "data-security"]
integrations: ["Anthropic"]
date_added: 2026-10-12
contribution_agreement_date: 2026-10-12T07:50:03Z
---

Patronus Security is a Rust CLI for inspecting text used by AI agents. It combines explicit security scans with optional runtime integrations for OpenAI Codex, Anthropic Claude Code and DeepSeek Harness. Detection is powered by Patronus Ark.

## What it does

- Checks supported text for prompt injection, personally identifiable information and data loss prevention signals.
- Scans explicitly selected files, directories and repositories, with local extraction of UTF-8/UTF-16 text and text from PDF and DOCX documents.
- Provides runtime hooks for user-prompt text, tool-result text and MCP-result text in supported hosts. Completed dangerous findings remain behind receipts; verified redacted reads let the agent continue with masked content.
- Provides coverage and finding reports, runtime receipts and a loopback dashboard for reviewing activity and configuring protection.
- Supports explicit public URL and authenticated public MCP-server audits through the Patronus API.

## How it works

The CLI uses the configured Local, Hybrid or API processing mode. Local analysis of files and runtime text stays on the device. API mode sends scan text to `https://control.patronus.studio/api/v1/scan`. Hybrid keeps user prompts and files or tool/MCP results of at most 2,048 tokens local; larger files and results send every analysis chunk to that API. Repository scans make this decision per file. Explicit URL and MCP-server audits use the API in every processing mode. The [privacy documentation](https://github.com/patronus-protect/patronus-security-cli/blob/main/docs/privacy.md) describes these data flows and the optional document-upload path.

Runtime integrations inspect text before delivery to the model. They do not scan tool requests, envelope metadata or media bytes. If scanning infrastructure is unavailable, runtime protection preserves tool execution and identifies the content as unverified. Installation alone does not establish coverage: the project's [runtime text contract](https://github.com/patronus-protect/patronus-security-cli/blob/main/docs/runtime-text-contract.md) explains host verification and receipt limitations.

## Getting started

Follow the [installation runbook](https://github.com/patronus-protect/patronus-security-cli/blob/main/INSTALL.md), including its checksum-first installation option, on macOS or Linux. The release installer requires `curl` and a SHA-256 tool; prebuilt releases do not require Rust. Run onboarding to choose processing mode and supported host integrations:

```sh
patronus-security-scanner onboarding
patronus-security-scanner dashboard
```

Local protection requires no account. Authenticated cloud features require sign-in; anonymous public URL scans have a limited allowance. Local L3 analysis requires the corresponding Ark assets prepared during setup. Start a new agent chat after installing runtime integrations.

Patronus does not perform general SAST, dependency, CVE or malware analysis. Image-only PDFs require OCR and are reported as unsupported. Review findings and coverage in context; a clean scan does not establish that arbitrary software is safe. The CLI and first-party integrations use Apache-2.0; the engine and third-party assets have separate terms described in the [licensing notes](https://github.com/patronus-protect/patronus-security-cli/blob/main/docs/licensing.md).
