---
name: "Microsoft Copilot Prompt API Harness"
author: "sbarasch-pub-git"
github_url: "https://github.com/sbarasch-pub-git/msft_copilot_prompt_api_harness"
description: "AWS Lambda harness that injects test prompts into M365 Copilot for Tenable AI Exposure security testing"
license: "MIT"
tier: "contributed"
tags: ["microsoft-copilot", "m365", "security-testing", "ai-exposure", "prompt-testing", "aws-lambda", "graph-api"]
integrations: ["AWS", "Azure", "Tenable"]
date_added: 2026-07-27
contribution_agreement_date: 2026-07-27T19:50:32Z
compatible_platforms: ["Claude Code", "Claude Desktop", "Claude Cowork", "Cline", "Codex", "Cursor", "Gemini CLI", "GitHub Copilot", "Windsurf"]
invocation: "/copilot-prompt-harness"
---

The Microsoft Copilot Prompt API Harness is an AWS Lambda-based security testing tool that programmatically injects test prompts into Microsoft 365 Copilot via the Microsoft Graph API. Designed to work alongside Tenable AI Exposure, it provides automated, repeatable coverage for validating AI threat detection in M365 environments.

## What it does

- Authenticates to Microsoft 365 using Azure AD (MSAL ROPC flow) with configurable service account personas
- Creates Copilot conversations and injects categorized test prompts spanning data exfiltration, system prompt disclosure, and jailbreak scenarios
- Runs on schedule via AWS EventBridge or on-demand via direct Lambda invocation
- Returns structured per-prompt results with conversation IDs for cross-referencing with M365 audit logs and Tenable AI Exposure alerts

## How it works

The harness is deployed as an AWS Lambda function triggered by EventBridge. It authenticates to the Microsoft Graph API using MSAL's Resource Owner Password Credential (ROPC) flow with a pool of M365 service account personas. Each invocation creates Copilot conversations in batches, injects prompts with configurable delays, and returns a structured JSON summary. The built-in prompt categories (data exfiltration, system prompt disclosure, jailbreak) serve as a starting template — operators replace them with their actual test prompt library.
