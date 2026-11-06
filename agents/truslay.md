last_reviewed	2026-11-06

name	truslay

author	cochinoraptor

github_url	https://github.com/cochinoraptor/Truslay-Showcase

website	https://truslay.com

description	An AI Agent Firewall that intercepts agent intents at the OS level to enforce deterministic security policies and prevent unauthorized actions (payments, data exfiltration, and command execution).
license	AGPL-3.0
tier	contributed
tags	
ai-security
agent-firewall
zero-trust
sui
prompt-injection
action-control
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
Truslay is an AI Agent Firewall designed to protect autonomous AI agents from making unauthorized actions. It doesn't just block payments; it intercepts the agent's intent at the OS level and evaluates it against a strict security policy before execution. This covers financial transactions (whitelists, spending limits), data access (preventing exfiltration), and command execution. If an action is deemed risky or violates the policy, Truslay blocks it deterministically (fail-closed) and generates a cryptographic audit trail of the decision.

## How it works
Truslay operates on a local-first architecture using a highly optimized INT4 Decision Engine. When an AI agent requests any real-world action (e.g., a USDC transfer, an API call, or a system command), Truslay intercepts the payload before it reaches the network or OS. The engine evaluates the intent against strict policies. If the action is safe, Truslay signs the decision cryptographically and allows execution. If it is risky (e.g., prompt injection, unknown recipient, excessive data access), it blocks the action and logs the reason. The system provides a dashboard (Trust Console) for developers to manage policies and view real-time audit logs, and it integrates with Sui Move contracts for on-chain enforcement of agent identity and spending rules.
