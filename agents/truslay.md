last_reviewed	2026-11-06
name	truslay
author	cochinoraptor
github_url	https://github.com/cochinoraptor/Truslay-Showcase
description	An AI Agent Firewall that intercepts agent intents at the OS level to enforce deterministic spending policies and prevent unauthorized transactions.
license	AGPL-3.0
tier	contributed
tags	
ai-security
agent-firewall
zero-trust
sui
prompt-injection
domains	
ai-security
web3
integrations	
Sui
date_added	2026-11-06
contribution_agreement_date	2026-11-06 12:00:00 UTC
works_with_tenable_hexa_mcp	false
cta	T2

# Truslay

## What it does
Truslay is an AI Agent Firewall designed to protect autonomous AI agents from making unauthorized payments, falling victim to prompt injection, or violating spending policies. It sits between the agent and the blockchain/API, evaluating intent at the OS level in milliseconds. If an action violates the user's whitelist or spending limits, Truslay blocks it deterministically (fail-closed) and generates a cryptographic audit trail of the decision.

## How it works
Truslay operates on a local-first architecture using a highly optimized INT4 Decision Engine. When an AI agent requests an action (e.g., a USDC transfer), Truslay intercepts the payload before it reaches the network. The engine evaluates the intent against strict policies (allowed recipients, max per transaction, daily budgets). If the action is safe, Truslay signs the decision cryptographically and allows the execution. If it is risky, it blocks the action and logs the reason. The system provides a dashboard (Trust Console) for developers to manage whitelists and view real-time audit logs, and it integrates with Sui Move contracts for on-chain enforcement.
