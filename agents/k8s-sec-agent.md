---
last_reviewed: 2026-09-03
name: "k8s-sec-agent"
author: "mostafahussein"
github_url: "https://github.com/mostafahussein/k8s-sec-agent"
description: "Kubernetes security audit agent for kagent that checks CIS benchmarks, pod security, RBAC, and network policies with privacy-preserving pseudonymization"
license: "Apache-2.0"
tier: "contributed"
tags: ["kubernetes", "security", "cis-benchmark", "kube-bench", "rbac", "network-policy", "audit", "mcp", "kagent"]
integrations: []
date_added: 2026-09-03
contribution_agreement_date: 2026-09-03T17:58:45Z
---

A Kubernetes security audit agent that runs as a declarative agent in [kagent](https://github.com/kagent-dev/kagent). It audits clusters against CIS security benchmarks using MCP tools, with built-in privacy-preserving pseudonymization so sensitive cluster data never reaches the LLM in plain text.

## What it does

- Runs CIS Kubernetes Benchmark checks via [kube-bench](https://github.com/aquasecurity/kube-bench) as in-cluster Jobs
- Scans all pods for security issues: privileged containers, running as root, missing resource limits, writable root filesystems
- Checks network policy coverage per namespace to find unprotected workloads
- Analyzes RBAC bindings for cluster-admin usage and overpermissive service accounts
- Executes arbitrary kubectl commands (with human-in-the-loop approval) for deep-dive investigations
- Produces a scored security posture report with prioritized findings and copy-pasteable remediation

## How it works

The agent exposes five MCP tools through a FastMCP server. All tool outputs are pseudonymized before the LLM sees them — namespace names, pod names, IPs, service accounts, and secrets are replaced with scoped tokens (e.g., `ns-a3f2-1`, `pod-a3f2-3`). An OpenAI-compatible reverse proxy sits in front of the upstream LLM, rehydrating pseudonymized tokens in the response before it reaches the user. Each session gets its own sanitizer with a unique scope, ensuring multi-tenant isolation. Deployed via Helm chart into any kagent-enabled cluster.
