---
name: "Tenable Tag Optimizer"
author: "dpickenstenable"
github_url: "https://github.com/dpickenstenable/tenable-tag-optimizer-agent"
description: "AI-powered tag recommendation skill that analyzes Tenable assets and creates intelligent, environment-specific tag taxonomies automatically"
license: "MIT"
tier: "unreviewed"
tags: ["asset-management", "tag-automation", "taxonomy", "pattern-recognition", "tenable", "compliance-scoping", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-06-23
compatible_platforms: ["Claude Code"]
invocation: "/tenable-tag-optimizer"
---

The **Tenable Tag Optimizer** is an AI-powered asset intelligence system that analyzes your Tenable environment and automatically recommends a clean, consistent tag taxonomy tailored to your actual infrastructure. It identifies natural asset groupings from operating systems, hostnames, network locations, software installations, and criticality patterns, then generates intelligent tag categories and values that enable real business workflows like compliance scoping, risk prioritization, and automated patch management.

## What it does

This skill performs comprehensive asset landscape analysis across your Tenable Vulnerability Management or Tenable One environment, examining thousands of assets to detect naming conventions, network segmentation patterns, software distributions, and infrastructure characteristics. It reviews your existing tags to avoid duplicates and identify gaps, then recommends 5-8 core tag categories with specific values based on what it actually finds in your environment—not generic templates.

The skill focuses on **8 high-value tag categories**: Environment (production/dev/qa), Operating System (Windows/Linux/network devices), Function (web-server/database/domain-controller), Location (data centers, cloud regions), Business Unit (department ownership), Criticality (risk-based tiers), Compliance Scope (PCI-DSS/HIPAA/SOX), Patch Window (maintenance schedules), Cloud Provider (AWS/Azure/on-premises), and Lifecycle Status (supported/end-of-life). Each recommended tag includes business value justification, estimated asset coverage, and workflow enablement examples.

After you approve recommendations, the skill automates tag creation via the Tenable API or MCP Server, applying consistent naming conventions (Capitalized categories, lowercase-hyphenated values). It can optionally bulk-apply tags to hundreds of assets based on detected patterns, supports dynamic tags that auto-update with filters, and generates summary reports with coverage metrics. The skill is designed for **quarterly re-runs** to evolve your taxonomy as infrastructure changes.

## How it works

The skill operates in three phases: **Asset Discovery & Pattern Recognition**, **Intelligent Recommendation**, and **Tag Creation & Application**.

**Phase 1** retrieves your complete asset inventory and software catalog from Tenable, analyzing operating system families and versions, network subnet groupings, hostname patterns (environment prefixes like `prod-`, location indicators like `nyc-`, function indicators like `web-`), installed application distributions, and high-criticality assets with elevated AES scores. It cross-references these patterns to identify natural asset groupings that warrant tagging.

**Phase 2** applies data-driven recommendation principles: only suggests tags that apply to 20+ assets, requires each value to cover 5+ assets minimum, enforces clean naming conventions, and focuses on tags that enable specific business workflows rather than theoretical categorization. For each recommended category, the skill explains the business value (e.g., "Environment tags let you exclude dev/qa from PCI DSS audits, reducing compliance scope by 30%"), estimates asset coverage, and provides workflow integration examples.

**Phase 3** creates tag categories and values through the Tenable API after your approval, handling duplicate conflicts gracefully, implementing exponential backoff for rate limits, and tracking creation progress. It can optionally apply tags to assets in bulk based on the detected patterns (e.g., all assets with "Windows" OS get the "Operating System:windows" tag), supports dynamic tag creation with automatic asset filters, and generates a comprehensive summary report showing tags created by category, assets tagged vs. total, coverage percentages, and next-step recommendations.

**Key differentiator:** Unlike manual tagging or generic taxonomy templates, this skill creates an **environment-specific** taxonomy that matches your actual infrastructure. It learns from your naming conventions, network design, and software distributions to recommend tags that are immediately useful. The quarterly re-run capability means your taxonomy evolves with your infrastructure—new cloud providers, container platforms, or business units are automatically detected and tagged.

Ideal for security teams managing large Tenable environments (1,000+ assets), compliance teams needing to scope audits efficiently, IT operations teams implementing patch management workflows, and cloud/infrastructure teams tracking multi-cloud or hybrid environments. The skill dramatically reduces the manual effort of creating and maintaining tag taxonomies while ensuring consistency and completeness.
