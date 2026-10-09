---
last_reviewed: 2026-10-06
name: "Guardrail"
author: "schappi1-byte"
github_url: "https://github.com/schappi1-byte/guardrail-security-change-safety"
description: "Dependency-aware security change impact agent that identifies the real-world consequences of security changes before they reach production."
license: "MIT"
tier: "contributed"
tags: ["security", "iam", "terraform", "change-management", "risk-assessment", "aws", "dependency-analysis", "cloudtrail", "remediation", "exposure-management"]
domains: ["exposure-management"]
integrations: ["AWS", "Terraform", "GitHub", "CloudTrail", "Kubernetes"]
date_added: 2026-10-06
contribution_agreement_date: 2026-10-06T00:00:00Z
works_with_tenable_hexa_mcp: false
---

## The Problem

Security engineers regularly deploy changes to IAM policies and access controls without knowing what services will break. They either over-privilege (to avoid breakage) or accidentally break production deployments.

Most tools answer "what is vulnerable?" — but Guardrail answers the harder question: **"What will this security change actually break?"**

## What It Does

Guardrail analyzes security changes **before deployment** by:

1. **Parsing** Terraform/IAM diffs to extract the exact permissions being changed
2. **Tracing dependencies** from IAM roles through service accounts to workloads
3. **Gathering evidence** from CloudTrail and deployment metadata to confirm actual usage
4. **Assessing impact** by matching removed permissions against observed usage patterns
5. **Recommending safer rollouts** with step-by-step migration plans when high impact is detected

### Example Workflow

You open a PR that removes `s3:GetObject` from a shared IAM role:

```terraform
- Actions = ["s3:GetObject"]
+ Actions = []
```

Guardrail automatically:

- Finds all services using this role (billing-api, invoice-worker, reporting-job)
- Checks CloudTrail and sees that billing-api and invoice-worker actively use this permission
- Identifies billing-api and invoice-worker as production workloads
- Flags this as **HIGH IMPACT** because production services will break
- Recommends: create a new dedicated role, migrate services to it, verify access for 24 hours, then remove the permission

**Output**: A PR comment with evidence, impact assessment, and a step-by-step safer migration plan.

## Key Features

- **Evidence-based impact assessment** — uses CloudTrail and actual usage patterns, not speculation
- **Production vs. staging awareness** — understands environment criticality
- **Confidence levels** — distinguishes between confirmed impact and potential risk
- **Safer rollout plans** — recommends specific steps instead of just flagging changes
- **Dependency tracing** — maps IAM roles to Kubernetes service accounts to workloads to real usage
- **GitHub PR integration** — works in your existing code review workflow

## Repository

- **Code**: https://github.com/schappi1-byte/guardrail-security-change-safety
- **Documentation**: Comprehensive README with examples
- **Demo**: Includes working scenario with realistic Terraform change and CloudTrail data
- **License**: MIT (open source, community-friendly)

## Why This Matters

Security teams spend enormous effort fixing vulnerabilities and implementing controls. But many fixes are temporary — the same vulnerability returns because the underlying cause (wrong image, wrong config, wrong owner, wrong deployment) isn't addressed.

Guardrail shifts the mindset from **"Can I make this change?"** to **"Can I make this change safely, and what's the best way to do it?"**

That's a much stronger contribution to remediation and exposure management.
