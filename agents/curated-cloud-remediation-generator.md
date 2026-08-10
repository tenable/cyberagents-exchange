---
name: "Curated Cloud Remediation Generator"
author: "Echo6Bravo"
github_url: "https://github.com/Echo6Bravo/curated-cloud-remediation-generator"
description: "Turns Tenable Cloud Security findings into review-ready CLI and OpenTofu/Terraform remediation artifacts for a curated, safety-tiered set of AWS and Azure policies. Never modifies your cloud."
license: "MIT"
tier: "contributed"
tags: [cloud-security, tenable, remediation, cspm, aws, azure, opentofu, terraform]
integrations: [Tenable, AWS, Azure]
date_added: 2026-08-10
contribution_agreement_date: 2026-08-10T12:50:12Z
---

The Curated Cloud Remediation Generator (`awsremgen` for AWS, `azremgen` for Azure) turns a
Tenable Cloud Security findings export into **review-ready remediation artifacts**: a fail-fast
vendor CLI script and import-aware OpenTofu/Terraform configuration. It is built for cloud
security engineers who want a well-informed first draft of a fix — one they read and run
themselves — rather than an automated actuator.

**It never modifies your cloud.** It holds no cloud credentials, makes no cloud API calls, and
has no code path that mutates a cloud environment. It writes files to a directory; the artifacts
are inert until you run them. There is also **no model in the loop** and nothing is inferred at
runtime — the chain from a finding to an artifact is fixed, hand-written, and inspectable.

## What it does

- **Curated coverage, stated honestly.** 10 AWS recipes and 10 Azure recipes, each written and
  checked individually against that cloud's own API definitions and documentation — none generated
  in bulk. A finding whose policy has no recipe is reported as unsupported rather than guessed at.
- **Safety is a level, not a disclaimer.** Every recipe carries an explicit, derived safety
  classification, and the default run emits only the safest tier. Of the shipped AWS recipes, 5 are
  `safest` and 5 require an explicit `--safety-level caution` opt-in. Irreversibility notes, cost
  notes, and the reversal command are emitted **inside the artifact**, next to the command they
  warn about.
- **Two renderings that cannot disagree.** A fail-fast `aws`/`az` shell script and import-aware HCL
  that adopts the existing resource rather than proposing to create a new one — both rendered from
  the same validated `ApiCall`.
- **Four-axis drift verification.** `verify` re-checks every AWS recipe against the four upstreams
  it depends on, which rot independently: the cloud's service models, the Terraform provider
  schema, the CLI's own flag surface, and your Tenable policy catalog. All four always run, so one
  broken upstream cannot hide another. **A check that could not run is never reported as a pass.**
- **Output split so a human can review it.** Artifacts are split per cloud, then per account, and
  HCL additionally per region — a correctness requirement, since neither a CLI invocation nor a
  Terraform provider can target more than one account at a time.
- **Guards against running the right fix in the wrong place.** Generated AWS scripts run an
  identity preflight and exit non-zero without doing anything if the caller's account does not
  match the file's; HCL sets `allowed_account_ids`. On Azure, a finding whose `accountId`
  contradicts the subscription inside its ARM `resourceId` is rejected and counted separately.
- **Reconcilable runs.** Malformed records are collected as explicit *rejections* rather than
  dropped, and `manifest.json` carries counts that reconcile — so a silently discarded finding
  cannot look like a clean estate.

## How it works

A hand-written recipe maps one Tenable Cloud Security policy UUID to one cloud API call, its
parameters, the equivalent Terraform/OpenTofu resource type and attribute, and a safety
classification. Findings are parsed as untrusted input and validated; two generators render the
same validated call; and `verify` re-checks the recipes against their upstreams on your machine.
New policies found by `policies` are **reported, never auto-remediated** — an unreviewed policy has
no recipe, and inventing one automatically is precisely the failure this design refuses.

The shared pipeline lives in `remgen.core` and each cloud is a provider under `remgen.providers`,
with a test that parses imports to enforce that `core` never depends on a provider and no provider
depends on another. There is deliberately one command per cloud rather than a `--cloud` flag: the
value that selects the cloud also selects the recipe set, the API verifier, and the credential
scope, so reading it from the command name makes "wrong cloud" a state the program cannot reach.

**Runtime Python dependencies: none** — standard library only, deliberately, because a remediation
generator that pulls a dependency tree is a supply-chain surface attached to something that
produces commands you will run against production. Python ≥ 3.10. AWS CLI v2 / botocore, the Azure
CLI, and an OpenTofu-generated provider schema are needed only for `verify`'s axes and to *run* the
output; generation works without them.

## Known limitations

Coverage is partial by design (2 Azure services; GCP and OCI are not implemented). There is no live
Tenable Cloud Security API adapter — findings come from a JSON export. Most importantly, **the tool
does not know about exceptions or accepted-risk decisions configured in Tenable Cloud Security**:
those do not survive a findings export, so scoping the export is yours to do. `verify` confirms
that names still exist and shapes still match; it cannot confirm that a cloud's *behavior* is
unchanged. `examples/` holds a complete committed run per cloud — input, verbatim console output,
and every artifact — regenerated by CI on every push so it cannot quietly go stale.
