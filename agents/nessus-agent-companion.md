---
name: "Nessus Agent Companion"
author: "ethodder"
github_url: "https://github.com/ethodder/nessus-agents-ai"
description: "An autonomous AI agent that monitors the health of Tenable Nessus Agents and reports to Slack."
license: "MIT"
tier: "contributed"
tags: ["monitoring", "nessus-agents", "slack", "vulnerability-management", "tenable", "ai-agent", "security"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-06-15
works_with_tenable_hexa_mcp: true
cta: "T1"
---

Nessus Agent Companion is a focused, single-purpose AI agent for Tenable Nessus Agent health monitoring and maintenance. It connects to Tenable Vulnerability Management via the Tenable MCP server, monitors your agent fleet on a scheduled heartbeat, and uses an LLM to analyze changes, correlate risks, and communicate findings to your team in Slack.

## What it does

- **Intelligent Monitoring**: Scheduled heartbeat audits of your Nessus Agent registry with smart alert suppression to prevent noise
- **Deterministic Change Detection**: Pre-flight diff engine computes exact agent changes (new/removed/status/version/health) before LLM analysis
- **Contextual Alerting**: Enriches alerts with VPR (Vulnerability Priority Rating) and ACR (Asset Criticality Rating) data
- **Agentic Remediation**: Offers to restart agents, unlink stale endpoints, assign groups, and apply configuration changes via natural language Slack commands
- **Operational Health Flags**: Automatically detects missing groups, stale scans, outdated plugins, safe mode, and health score degradation
- **Scale-Ready**: Handles fleets from 5 to 2000+ agents with intelligent templating and token optimization

## How it works

The agent uses a deterministic pre-flight engine that fetches the current agent registry from Tenable MCP, compares it against previous state, and computes structured diffs. It auto-saves agent state to disk (avoiding context bloat) and posts status reports directly to Slack. The LLM receives pre-computed diffs and offers contextual remediation actions. Destructive operations (restart, unlink, group changes) are only available during user-initiated commands - proactive heartbeat cycles are observe-only for safety. Built with LiteLLM for multi-model support (Gemini, Claude, GPT, Azure OpenAI) and runs as an isolated Docker container with persistent state.
