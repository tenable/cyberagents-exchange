---
playbook_type: "n8n"
name: "KnowBe4 PhishER Email Analysis"
author: "disassembledd"
github_url: "https://github.com/disassembledd/knowbe4-phisher-email-analysis"
description: "Agent-empowered n8n workflow that pulls outstanding reported emails from PhishER for AI-driven analysis, tagging, and comment submission."
license: "MIT"
tier: "contributed"
tags: ["knowbe4", "phisher", "email-analysis", "n8n"]
integrations: ["KnowBe4"]
workflow_diagram: |
  flowchart LR
    A[Scheduled Trigger] --> B[Retrieve Messages]
    B --> C[Filter Unresolved]
    C --> D[AI Email Analysis]
    D --> E[Post Comment]
    D --> F[Apply Tag]
date_added: 2026-07-01
---

This is an agent-empowered n8n workflow that pulls outstanding reported emails from the KnowBe4 PhishER platform for AI-powered analysis. It assesses whether each email is a threat, spam, or clean, then submits a verdict tag and detailed comment back to PhishER.

## What it does

Analyzes the contents of reported emails — including embedded images, attachments, and body text — to determine whether they represent a genuine phishing threat, spam, or a clean message. Results are automatically posted back to PhishER as comments and classification tags.

## How it works

The workflow runs on a 5-minute schedule, pulling unprocessed messages from PhishER via GraphQL API. Each email is parsed (including MIME decoding, image extraction, and attachment handling) and sent to Claude on AWS Bedrock for multimodal analysis. The AI verdict and confidence score are posted back as a comment and tag on the original PhishER message.

## Setup

Requires an n8n instance with `mailparser`, `htmlparser2`, `domutils`, and `dom-serializer` installed in the runner environment. Configure credentials for KnowBe4 PhishER API (bearer token) and AWS Bedrock (for Claude access). See the repository README for detailed deployment instructions.
