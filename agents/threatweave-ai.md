---
name: "ThreatWeave AI"
author: "sreedhar51"
github_url: "https://github.com/sreedhar51/threatweave-ai"
description: "Correlates Tenable vulnerabilities, relevant CIS compliance failures, and verified business context to produce explainable remediation priorities and reproducible decisions."
license: "MIT"
tier: "contributed"
tags: ["vuln-management", "exposure-management", "compliance", "risk-prioritization", "remediation", "decision-replay"]
domains: ["vulnerability-management", "governance-risk-compliance"]
integrations: ["Tenable", "Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T05:30:00Z
works_with_tenable_hexa_mcp: false
---

ThreatWeave AI is a read-only exposure investigation and prioritization agent. Vulnerability scanners tell security teams what is wrong, but a large inventory also needs an evidence-based answer to **what should be reviewed and remediated first, and why**.

ThreatWeave connects Tenable vulnerability findings, related failed CIS host-configuration checks, and *human-verified* CMDB business context. It applies a transparent organizational policy and produces ranked **candidate Fix Groups** with **Decision Receipts** that let an analyst reproduce and explain a prioritization decision.

## What it does

ThreatWeave produces four practical outputs:

- **Candidate remediation shortlist.** Groups findings by candidate solution and software family where supported, with affected assets, original Tenable severity/VPR, contextual score, priority, and evidence-quality flags. Grouping is not a guarantee that one patch resolves everything.
- **Same-asset vulnerability/CIS correlation.** Applies explicit technology-to-control rules only when the vulnerability and failed audit relate to the **same authoritative Tenable asset UUID**. Unknown or incomplete compliance data is not counted as a passing control.
- **Explainable asset investigation.** Shows supporting vulnerability findings, relevant CIS failures, policy-rule contributions, ingestion coverage and freshness, and any verified business classification.
- **Reproducible Decision Receipts and Replay.** Records evidence and policy fingerprints, supporting finding references, and deterministic rankings. Comparing receipts exposes priority movements attributable to new evidence or changed policy.

An offline guided investigation works without an LLM. An optional Claude integration can explain bounded findings and suggest **draft-only** policy rules. An optional local MCP server exposes read-only evidence and dry-run tools. Neither the LLM nor MCP tools directly executes remediation.

## How it works

1. **Acquire evidence:** import authorized CSV/JSON/JSONL or Nessus files, or use the read-only Tenable Vulnerability Management asynchronous asset, vulnerability, and compliance export APIs. The on-prem Security Center adapter is optional and requires environment-specific validation.
2. **Normalize and qualify:** retain source hashes, original severity and VPR, authoritative asset UUIDs, and audit outcomes. Explicit correlation rules prevent unrelated findings from being labeled a compounded exposure.
3. **Apply verified context:** import ServiceNow-style CMDB *export files* only after a human approves the asset-to-Tenable UUID mapping. There is **no live ServiceNow API synchronization**.
4. **Prioritize and trace:** the deterministic YAML policy evaluates evidence into candidate Fix Groups, then DecisionTrace creates stable receipts for review and before/after comparison.

ThreatWeave does not infer cross-host attack paths or network reachability from scanner data. Its rankings support analyst decisions; they do not establish exploitability, confirmed patch success, or measured risk reduction.

## Try it

Python **3.11+** is required. The synthetic demo needs **no Tenable or Anthropic credentials**.

~~~bash
git clone https://github.com/sreedhar51/threatweave-ai.git
cd threatweave-ai
python -m pip install -e '.[dev,ui]'

# Offline evidence-to-decision workflow
python -m threatweave.cli --db runtime/demo.db demo
python -m threatweave.cli --db runtime/demo.db investigate

# Three-stage synthetic evidence replay, same policy each stage
python -m threatweave.cli demo --staged
python scripts/ship_check.py --repeat 3

# Optional interactive dashboard
python -m streamlit run dashboard/app.py
~~~

For real Tenable exports, configure authorized API credentials locally, scope exports appropriately, and avoid committing raw tenant findings. The Streamlit dashboard keeps tenant and synthetic databases separate.

**Source and documentation:** [ThreatWeave AI](https://github.com/sreedhar51/threatweave-ai) · [Setup and How to Run](https://github.com/sreedhar51/threatweave-ai#setup-and-how-to-run) · [Architecture](https://github.com/sreedhar51/threatweave-ai/blob/main/docs/ARCHITECTURE.md)

## Safety and scope

- Analysis and tool integrations are read-only with respect to Tenable and other vendors: no scan initiation, patching, ticket creation, or source-system write-back.
- Policy changes and CMDB identity mappings require human review; source evidence is treated as untrusted input and agent outputs are bounded and scrubbed for common secret patterns.
- Tenable VM integration has been exercised with an authorized lab; Security Center and optional Claude/MCP interoperability need validation in each deployment.
- Local synthetic tests and benchmarks do not establish production throughput or remediation outcomes.
