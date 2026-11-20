---
name: "VespaFlow — CI/CD Remediation Swarm"
author: "brainborg"
github_url: "https://github.com/brainborg/VESPAFLOW"
description: "A four-stage remediation swarm that intercepts failed CI/CD builds, injects safe security context, and autonomously engineers code or infrastructure fixes — no cloud credentials required."
license: "MIT"
tier: "contributed"
domains: ["application-security", "vulnerability-management"]
integrations: ["Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T00:00:00Z
works_with_tenable_hexa_mcp: false
playbook_type: "standard"
agents_used:
  - name: "VespaFlow Swarm Coordinator"
    role: "Orchestrates the remediation loop, manages LLM iterations, enforces human-in-the-loop gate."
    type: "exchange"
  - name: "VespaFlow Context Injector"
    role: "Classifies CI errors, extracts signal-rich log lines, injects security hints."
    type: "exchange"
  - name: "VespaFlow MCP Server"
    role:
