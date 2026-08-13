---
last_reviewed: 2026-08-13
name: "curb"
author: "amcdonnell-dot"
github_url: "https://github.com/amcdonnell-dot/CURB"
description: "Enumerates the Tenable Hexa AI MCP tool surface, classifies each tool's privilege tier, and emits the minimum tool set, Tenable role, and MCP client config a described workflow needs."
license: "MIT"
tier: "contributed"
tags: ["mcp", "least-privilege", "api-key-scoping", "governance", "tenable-one"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-08-06
contribution_agreement_date: 2026-08-06T14:54:48Z
works_with_tenable_hexa_mcp: true
cta: "T1"
---

## What it does

curb enumerates the tool surface of the Tenable Hexa AI MCP server on a Tenable One Foundation or Advanced tenant, classifies each tool by the privilege tier it requires (Read, Write, or Manage), and turns a plain-English description of one real workflow into the smallest tool set that workflow needs -- plus a Tenable custom role recommendation and ready-to-paste MCP client config fragments for Claude Code, Claude Desktop, VS Code, and Cursor. It also diffs two tool-surface snapshots to catch drift between runs.

## How it works

curb never sits in an agent's runtime path and never proxies a tool call -- it runs at design time, offline except for one documented request. curb enumerate makes a single `tools/list` call against the Hexa AI MCP endpoint using your own Tenable API keys and writes the result to a surface file. Every other command -- map, scope, diff -- reads that file locally and never touches the network, calls a Tenable tool, or holds a credential. Classification is a verb-signal heuristic over tool names and descriptions, never a model call, producing a privilege tier and confidence score per tool, with unknown returned instead of a guess whenever the signal is genuinely absent. scope maps a workflow's plain-English intents onto the classified tool set and reports an ambiguity rather than resolving it when more than one tool could satisfy an intent. curb never creates or modifies anything in a Tenable tenant, and has no telemetry -- every recommendation is applied by hand, in the Tenable UI.
