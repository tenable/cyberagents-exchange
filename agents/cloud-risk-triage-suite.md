---
name: "Cloud Risk Triage Suite"
author: "wingchurn-tenable"
github_url: "https://github.com/wingchurn-tenable/cloud-risk-triage"
description: "Autonomous Tenable Cloud Security posture sweep: critical findings, cleanup, AI risk & toxic combinations."
license: "MIT"
tier: "unreviewed"
tags: [cloud-security, tenable, cspm, ai-spm, soc, posture, cnapp]
integrations: [Tenable, AWS, Azure, GCP]
date_added: 2026-06-30
---

The Cloud Risk Triage Suite is an autonomous cloud security posture agent for Tenable
Cloud Security, built for cloud security architects and SOC analysts who want a fast,
repeatable daily posture read. It runs a multi-section sweep against live Tenable Cloud
Security data and writes a SOC-ready report — every check is always reported, even when
it returns nothing (marked EMPTY).

It ships in two editions: an **MCP edition** that runs through the Tenable Cloud Security
(`tcs`) MCP connector for the richest results, and an **API-token edition** that uses
the public GraphQL API with a Bearer token and no connector.

## What it does

The agent produces four report sections:

1. **Address critical findings** — AWS root users without MFA; third-party identities
   with access to sensitive data; publicly exposed resources (with a network-endpoint
   flag); exposed secrets (with a network-endpoint flag).
2. **Address low-hanging fruits** — inactive identities; unused credentials (inactive
   IAM users with an enabled access key); unused security groups (no attached resources).
3. **Discover AI risk** — inventory of AI assets (Bedrock, SageMaker, Azure Cognitive
   Services/OpenAI, GCP Vertex), then correlation of fine-tuned/custom models to their
   training-input and output data buckets.
4. **Toxic combination** — public workloads that are simultaneously internet-exposed
   (network exposure + scope), carry a Critical-VPR vulnerability, and hold high-privilege
   permissions, with network-exposure-scope and confirmed-network-endpoint columns.

Each run ends with a prioritized remediation order (toxic combinations first) and
verification notes listing the exact filters and counts used. It never fabricates data —
every value is quoted from query results — and it flags demo/test environments.

## How it works

The MCP edition queries Tenable Cloud Security's Explore / UDM data model via the `tcs`
MCP tools (object types such as `AwsIamRootUser`, `IIdentity`, `IEntity`, `IDataEntity`,
`IAiResource`, `AwsBedrockCustomModel`, and `IVirtualMachine`), using count queries for
totals and flagged subsets, relation rules for toxic-combination chaining, and joins to
resolve network endpoints. The API-token edition calls the public GraphQL `/graphql`
endpoint with `Authorization: Bearer`, mapping each check onto Findings/Entities. Both
write a dated markdown report and can be scheduled to run automatically each morning.
A marketplace manifest lets either edition be installed directly from the repo.
