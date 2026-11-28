---
name: "Tool Guard"
author: "acencyril"
github_url: "https://github.com/acencyril/tool-guard-bundle"
description: "Code-level guardrails on the tools an AI agent can call: permissions, limits, human approval, stop button and a tamper-evident journal, so a manipulated model cannot run a refused action."
license: "MIT"
tier: "contributed"
tags: ["guardrails", "mcp", "human-in-the-loop", "least-privilege", "audit-log", "prompt-injection", "symfony", "php"]
domains: ["ai-security"]
integrations: []
date_added: 2026-11-28
contribution_agreement_date: 2026-11-28T16:54:00Z
works_with_tenable_hexa_mcp: false
---

## What it does

When an AI agent can refund, send email or delete records, its rules cannot live in its prompt: a persuasive user, a fake manager or an instruction hidden in a document talks the model out of them. Tool Guard moves those rules into code, on the tools themselves. Each tool an agent can call gets declared rules (who may call it, numeric limits, rate limits, which agent may use it); a call that breaks a rule is refused before it runs, and a risky one is held until a human approves it. Whatever the model was talked into, a refused call never executes.

It covers Symfony AI agents, MCP servers built with the official PHP MCP SDK, an MCP server you did not write (as a guard in front of it), and any hand-written agent loop. Ports for Python and Node exist as separate repositories.

## How it works

Rules are PHP attributes on the tool methods (`#[Limit]`, permission and approval rules, agent roles). Every tool call, whatever path it takes, goes through one policy check that returns run, refuse or hold, with a plain reason the model and the operator both see. Held calls wait on an approvals page or a notification (Symfony Notifier channels, or optionally an ntfy topic you configure). A stop button halts every AI caller at its next call. Every decision is written to a hash-chained journal, shown in the Symfony profiler and listed by `debug:tool-guard`; an observe mode logs what would be blocked before you enforce.

It does not detect prompt injection or filter what the model says: it decides what the model's tool calls are allowed to do. The repository ships a one-command demo (no API key, no model, no database) where a scripted hostile agent attacks a demo shop over MCP with and without Tool Guard, and a corpus of 25 attacks replayed by the test suite on both paths.

Outbound calls: none by the bundle itself. Optional, and only if you configure them: an ntfy topic for approval notifications, your own Notifier channels, and, for the real-model demo only, OpenRouter or Hugging Face with your own key.
