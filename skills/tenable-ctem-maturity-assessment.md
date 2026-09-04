---
name: "Tenable CTEM Maturity Assessment"
author: "mrovere1"
github_url: "https://github.com/mrovere1/tenable-ctem-mcp"
description: "Classifies a Tenable One tenant across the five CTEM maturity stages and delivers a three-quarter roadmap"
license: "MIT"
tier: "contributed"
tags: ["ctem", "exposure-management", "maturity-assessment", "security-posture", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-09-04
contribution_agreement_date: 2026-09-04T17:46:23Z
compatible_platforms: ["Claude Code"]
invocation: "/tenable-ctem-maturity-assessment"
---

Measures a Tenable One tenant, classifies it across the five stages of the Exposure Management
Maturity Model — Ad Hoc, Defined, Standardized, Advanced, Optimized — and delivers a three-quarter
improvement roadmap plus a self-contained HTML dashboard. Read only: no write tool is ever called.

It consumes the `tenable-ctem-mcp` server in the same repository, which does the measuring. The
skill does the judging. That separation is deliberate: the numbers stay auditable and the thresholds
stay configurable, and neither can quietly contaminate the other.

## What it does

Nineteen indicators across the five CTEM stages. Seventeen score a stage; two are informational and
carry context without being converted into maturity. The report publishes two numbers side by side —
the **effective stage**, which is the lowest of the five, and the **average stage** — because the
difference between them is the finding. A customer averaging Standardized with an effective stage of
Ad Hoc has capability that one blocking stage is preventing from producing results, and the report
names that stage and the indicator responsible in prose.

Step 0 discovers the tenant and proposes a mapping — which tag category is criticality, which is
owner, which scans represent the recurring assessment — then asks the operator to confirm before
measuring anything. It never guesses from a keyword alone, because customers use their own
nomenclature: `Tier`, `BIA`, `Classificação`, `Gold/Silver/Bronze`, or the name in another language.

The report language is chosen at Step 0 — English, Portuguese or Spanish — and governs the operator
dialogue, the report prose and the dashboard. Data read from the tenant is printed exactly as it
exists there, in whatever language it was created.

## How it works

**No threshold here is official Tenable.** The maturity model is qualitative and publishes no numeric
threshold per stage. Every cutoff appears in the report labelled with its origin: skill default,
cited external standard, or operator override. The report is built so that distinction is impossible
to miss.

**A gap is not a zero.** A query that fails becomes a declared gap with a named cause and leaves the
calculation. A confidence gate runs before any stage is published: below a proportional threshold of
measured indicators, the skill declines to classify and delivers the indicators plus what needs
enabling in the tenant instead.

**Some results are gaps on purpose.** Time-to-fix measures detection to detection, not time to act.
When the measurement windows turn out to be made only of scan dates, the skill declares MTTR a gap
rather than scoring it — scoring would measure the same thing the cadence indicators already measure,
counting assessment cadence twice and calling it remediation maturity. The finding is written into
the report in prose, because it is worth more than the lost number.

## Requirements

The `tenable-ctem-mcp` server registered and connected — see the repository README. Credentials live
in the server's environment; the skill never asks for a key.
