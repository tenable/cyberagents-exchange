---
name: "Control-Aware Risk Scoring Engine"
author: "dpickenstenable"
github_url: "https://github.com/dpickenstenable/control-aware-risk-scoring"
description: "Advanced vulnerability prioritization with defense-in-depth analysis across firewalls, EDR, WAF, and network segmentation"
license: "MIT"
tier: "unreviewed"
tags: ["tenable", "risk-scoring", "firewall", "edr", "waf", "defense-in-depth", "compensating-controls", "segmentation"]
integrations: ["Tenable", "Palo Alto", "Fortinet", "Cisco", "CrowdStrike", "SentinelOne", "Microsoft Sentinel"]
date_added: 2026-06-23
compatible_platforms: ["Claude Code"]
invocation: "/control-aware-risk-scoring"
---

The Control-Aware Risk Scoring Engine transforms vulnerability management from theoretical risk to actual exploitability. Traditional VPR and CVSS scores ignore your defenses — this skill integrates with firewalls, EDR, WAF, and network topology to calculate what's truly at risk.

## What it does

- **Defense-in-Depth Calculation** — Quantifies combined effectiveness of layered security controls (firewall, segmentation, EDR, WAF, IDS) using multiplicative risk reduction
- **Multi-Vendor Integration** — Queries APIs from Palo Alto, Fortinet, Cisco, CrowdStrike, SentinelOne, Defender, Cloudflare, AWS WAF, and more to validate actual protection
- **Control Gap Analysis** — Identifies under-protected assets lacking critical controls (EDR, WAF, segmentation) for targeted remediation
- **Adjusted Risk Prioritization** — Ranks vulnerabilities by actual exploitability, not generic severity — same CVE on different assets gets different priorities based on controls
- **Network Segmentation Scoring** — Analyzes VLAN isolation, lateral movement potential, crown jewel reachability, and cloud security groups
- **Control Reliability Factors** — Accounts for real-world control failure rates (firewall 98% reliable, EDR 95%, WAF 90%, IDS 85%)

## How it works

The skill connects to Tenable via MCP Server or Direct API to retrieve vulnerabilities and asset AES scores. It then queries firewall APIs for rule analysis, EDR platforms for agent status, WAF providers for protection coverage, and network topology systems for segmentation data. Each control layer is assigned an effectiveness factor based on configuration quality (e.g., restrictive firewall rules = 0.4, healthy EDR agent = 0.3, OWASP-enabled WAF = 0.4).

The defense-in-depth calculator multiplies these factors to determine remaining risk exposure. A critical vulnerability (base risk 98) behind firewall (0.6) + segmentation (0.5) + EDR (0.3) + WAF (0.4) + IDS (0.7) yields defense factor 0.0252, reducing actual risk to 2.47 (97.5% protected). Control reliability factors (2-15% failure rates) prevent over-confidence. Special handling for zero-days, insider threats, and supply chain vulnerabilities adjusts effectiveness accordingly.
