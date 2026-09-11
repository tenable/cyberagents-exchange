---
name: "Agent Behaviour Drift Sentinel"
author: "SweetKenneth"
github_url: "https://github.com/SweetKenneth/shpbl-drift-sentinel"
description: "Signs a baseline of how an agent normally behaves, then reports divergence with dimension-level attribution, episode replay, honest confidence and operator-approved calibration."
license: "MIT"
tier: "contributed"
tags: ["ai-agent-security", "drift-detection", "behavioural-baseline", "detection-engineering", "anomaly", "governance", "deterministic", "mcp"]
integrations: []
date_added: 2026-09-11
contribution_agreement_date: 2026-09-11T21:33:55Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "bun"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor"]
tools_exposed:
  - name: "ingest_traces"
    description: "Ingest caller-supplied agent execution traces and return a trace set reference"
  - name: "set_baseline"
    description: "Sign and store a behaviour profile as a named baseline version"
  - name: "check_drift"
    description: "Compare a trace set against a signed baseline and report divergence"
  - name: "explain_drift"
    description: "Dimension-level attribution plus replay of the most divergent episode"
  - name: "calibrate"
    description: "Propose a calibration profile from labelled findings; never mutates thresholds"
  - name: "apply_calibration"
    description: "Create a new signed baseline version carrying an approved calibration profile"
  - name: "configure_suppression"
    description: "Declare maintenance windows and known change markers"
resources_exposed: []
prompts_exposed: []
---

A compromised or manipulated agent rarely announces itself with a single malicious call. It starts reaching for different tools, touching different resources, running longer, failing differently. This server captures what normal looked like — signed, versioned, and immutable — so the change is visible and arguable.

## What it does

Operators hand in execution traces, freeze a behaviour profile as a signed baseline version, and afterwards compare fresh traces against it. A drift finding says which behavioural dimensions moved, by how much, and which single episode diverged most, and it can replay that episode for review. Confidence is reported honestly: when the sample is too small to support a conclusion, the finding still carries a severity but the severity is capped at informational rather than inflated. False positives are handled the way detection engineering actually works — an analyst labels findings, `calibrate` proposes a profile without changing anything, and only `apply_calibration` creates a new signed baseline version carrying that profile, so every threshold change is attributable. Maintenance windows and known change markers can be declared so an expected deployment does not read as an attack.

## How it works

A zero-dependency stdio MCP server written from a public behaviour specification. Baselines are signed through a caller-registered key adapter and are versioned rather than edited, so history cannot be rewritten to make a finding disappear. Comparison is deterministic: the same traces against the same baseline yield the same finding, which is what makes replay and review meaningful. No model call, no network egress, no telemetry; traces are supplied by the caller rather than collected by the server. Known limitation stated in the repository — a baseline captures only what the supplied traces contained, so behaviour that was already abnormal when the baseline was taken will look normal afterwards. Conformance tests cover the numbered specification properties, including the insufficient-confidence severity cap.
