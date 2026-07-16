---
name: "Company Intel Studio"
author: "pramseier-tenb"
github_url: "https://github.com/pramseier-tenb/company-intel-studio"
description: "Generate competitive company intelligence briefs with live HTML dashboards and polished PDFs."
license: "MIT"
tier: "contributed"
tags: ["company-intelligence", "competitive-analysis", "research", "dashboard", "pdf-generation", "briefing"]
integrations: ["Anthropic"]
date_added: 2026-06-22
compatible_platforms: ["Claude Code"]
invocation: "/company-intel-brief"
---

Company Intel Studio is a Claude skill that transforms company research into actionable intelligence. Pick any company, and the skill generates a comprehensive intelligence brief in two formats: a live HTML dashboard artifact and a polished, print-ready PDF — both rendered from a single JSON content file.

## What it does

The skill prompts for a company name, then researches current news, product launches, financial data, and competitive positioning through automated web searches. It automatically detects whether a company is public or private to shape the financial snapshot appropriately, generates a branded dashboard with the company's color palette, and sets up a daily 7 AM auto-refresh to keep intelligence current. Output includes a financial bar, news & announcements, product updates, and a competitive landscape table with threat-level assessments.

## How it works

Company Intel Studio runs four parallel web searches targeting recent announcements, product updates, financials (public: earnings/analyst targets; private: valuation/funding), and competitive analysis. It assembles findings into a structured JSON file with theme colors, financial metrics, news items, product highlights, and competitor comparisons. A bundled Python generator (`build_brief.py`) renders both the HTML dashboard and PDF from the same source, ensuring consistency. The skill creates a live artifact via the Cowork MCP server and schedules daily refreshes using the scheduled-tasks MCP server.
