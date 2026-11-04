---
last_reviewed: 2026-11-04
name: "ThreatWeave AI"
author: "sreedhar51"
github_url: "https://github.com/sreedhar51/threatweave-ai"
description: "Read-only Claude agent that correlates Tenable vulnerabilities with same-asset CIS failures and verified business context, ranks candidate fixes deterministically, and adds evidence-cited Claude decision briefs and correlation proposals."
license: "MIT"
tier: "contributed"
tags: ["vuln-management", "exposure-management", "compliance", "risk-prioritization", "remediation", "decision-replay", "claude", "mcp"]
domains: ["vulnerability-management", "governance-risk-compliance"]
integrations: ["Tenable", "Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T05:30:00Z
works_with_tenable_hexa_mcp: false
---

ThreatWeave AI is a read-only exposure decision agent. Scanners tell a security team what is wrong on each host; ThreatWeave answers **which candidate fix to investigate first, why that answer changed since last week, and how to prove it**.

It joins Tenable vulnerability findings, failed CIS checks on the *same* asset, and *human-verified* CMDB context. A deterministic policy engine ranks candidate fix groups and writes a **Decision Receipt** for every run. Claude then adds judgment on top: decision briefs, correlation proposals, and investigation. Everything Claude returns is checked by code and stays advisory.

## What it does

- **Ranks candidate fix groups.** Findings are grouped by candidate solution and software family, with affected assets, original Tenable severity and VPR, a contextual priority, the policy rules that fired, and evidence-quality flags. A group is a candidate, not a guarantee that one patch resolves everything.
- **Correlates conservatively.** A vulnerability and a failed CIS check are linked only when they share an authoritative Tenable asset UUID *and* a vetted `software_family` to `control_id` rule says the control is relevant. Co-occurrence alone is never treated as compounded risk.
- **Proves its decisions.** Each Decision Receipt fingerprints the dataset, the policy, and the full ranking; identical inputs give an identical receipt ID. Replay compares two receipts and attributes every rank change to new evidence, a policy change, or both.
- **Claude decision briefs (`brief`).** For each top-ranked group, Claude recommends `INVESTIGATE_NOW`, `SCHEDULE`, `NEEDS_EVIDENCE`, or `MANUAL_REVIEW`, with confidence, cited finding IDs, evidence gaps, and validation steps. Each brief is bound to the receipt ID and never changes a rank or score.
- **Claude correlation proposals (`propose-correlations`).** For same-asset pairs that no rule links yet, Claude judges whether the failed control is a real security relationship and drafts a rule for human review. Drafts are never applied automatically.
- **Investigation and policy drafting.** `ask` runs a bounded Claude tool-use loop over read-only evidence tools; `draft-rule` turns a plain-English request into an unapproved policy rule. A Claude Code subagent and a read-only MCP server expose the same six tools, and an offline guided investigation needs no API key at all.

## How it works

1. **Acquire evidence.** Import authorized CSV, JSON, JSONL, or `.nessus` files, or use the read-only Tenable Vulnerability Management asynchronous export APIs. An on-prem Security Center adapter is included but needs validation in each environment.
2. **Normalize and qualify.** Keep source hashes, original severity and VPR, authoritative asset UUIDs, and audit outcomes. Explicit correlation rules stop unrelated findings being labelled compounded exposure.
3. **Apply verified context.** Import ServiceNow-style CMDB *export files* only after a human approves each asset-to-UUID mapping. There is no live ServiceNow API integration.
4. **Decide deterministically.** The restricted YAML policy evaluates the evidence into ranked fix groups and a Decision Receipt. No language model scores or ranks anything.
5. **Advise with Claude.** Claude receives bounded evidence, scrubbed of credentials and wrapped as untrusted data, and answers in a fixed JSON schema. Code then rejects any output that cites a finding Claude was not shown, recommends action without citing evidence, or proposes a correlation it cannot support from both sides. Correlation candidates whose evidence looks like prompt injection are not sent to Claude at all.

ThreatWeave does not infer cross-host attack paths or network reachability. Its rankings and Claude's briefs support an analyst's decision; they do not establish exploitability, patch success, or measured risk reduction.

## Try it

Python **3.11+** is required. The synthetic demo needs **no Tenable or Anthropic credentials**.

The separate [enterprise contextual-policy demonstration](https://github.com/sreedhar51/threatweave-ai/blob/main/docs/ENTERPRISE_CONTEXT_DEMO.md) uses fictional payment, identity, recovery, administrator-workstation and development evidence to show before/after decisions without changing vendor severity or VPR. Its weights are illustrative and require human validation before production use.

~~~bash
git clone https://github.com/sreedhar51/threatweave-ai.git
cd threatweave-ai
python -m venv .venv
source .venv/bin/activate                    # macOS/Linux; Windows steps are in the README
python -m pip install -e '.[dev,ui,mcp]'

# Offline evidence-to-decision workflow
threatweave --db runtime/demo.db demo
threatweave --db runtime/demo.db investigate
threatweave demo --staged                    # same policy, three evidence stages
python scripts/contextual_policy_demo.py      # fictional enterprise context, same dataset, different policies
python scripts/ship_check.py --repeat 3      # three clean runs, identical receipts

# Claude layers (set ANTHROPIC_API_KEY first)
threatweave --db runtime/demo.db brief --limit 3
threatweave --db runtime/demo.db propose-correlations
threatweave --db runtime/demo.db ask "Which fix group should we investigate first, and why?"

# Interactive dashboard
streamlit run dashboard/app.py
~~~

To use it from Claude Code, launch `claude` from the repository root in the same shell where you activated the Python environment used for installation (see the [Claude Code setup](https://github.com/sreedhar51/threatweave-ai#claude-code-agent-and-mcp-server)): it ships `.mcp.json` and a `threatweave` subagent limited to the six read-only MCP tools.

**Source and documentation:** [ThreatWeave AI](https://github.com/sreedhar51/threatweave-ai) · [Setup and How to Run](https://github.com/sreedhar51/threatweave-ai#setup-and-how-to-run) · [How Claude fits](https://github.com/sreedhar51/threatweave-ai#how-claude-fits) · [Architecture](https://github.com/sreedhar51/threatweave-ai/blob/main/docs/ARCHITECTURE.md)

## Safety and scope

- **Read-only.** No tool initiates scans, patches assets, creates tickets, or writes back to Tenable or any other system.
- **Human approval.** Policy rules, correlation rules, and CMDB identity mappings are drafts until a person approves them.
- **Outbound data.** With Tenable credentials set, ThreatWeave calls `cloud.tenable.com` (or your Security Center URL) read-only. With `ANTHROPIC_API_KEY` set, the Claude commands send the question and bounded evidence (hostnames, finding titles and excerpts, control IDs, CMDB context), with credentials scrubbed, to `api.anthropic.com`. Nothing else leaves the machine; the README lists every flow.
- **Validation status.** Tenable VM ingestion has been exercised on an authorized lab tenant. Security Center and the Claude Code and Claude Desktop clients still need validation in each deployment, and the Claude layers' recommendations are checked for traceability, not correctness.
- **Benchmarks.** Synthetic tests and benchmarks do not establish production throughput or remediation outcomes.
