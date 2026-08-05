---
name: "Chokepoint Finder"
author: "tarhou"
github_url: "https://github.com/tarhou/chokepoint-finder"
description: "Finds the smallest set of remediation actions that removes the largest share of risk, refuses to act on evidence it cannot read, and verifies the result before a change record closes."
license: "MIT"
tier: "contributed"
tags: ["vuln-management", "exposure-management", "remediation", "prioritization", "attack-path-analysis", "set-cover", "change-management", "claude-code"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T02:04:27Z
works_with_tenable_hexa_mcp: false
---

A non-executing remediation decision agent. Security teams do not have a detection
problem, they have a selection problem: a mid-size estate carries thousands of open
findings and capacity for maybe ten changes a week. Every scanner answers *what is
wrong*. This agent answers the question that actually decides Monday morning — **which
few changes are worth making, in what order, and how do we prove they landed.**

## What it does

Findings are ranked one by one almost everywhere. That is the wrong unit, because a
single action — one patch rolled out fleet-wide, one base image rebuilt, one IAM role
scoped, one security group closed — retires hundreds of findings at once. Chokepoint
Finder collapses findings into the actions that fix them, then solves for the shortlist.

It returns four artifacts:

- **A ranked shortlist**, where each action is scored by what it retires *given
  everything above it is already done*. Overlap is priced in exactly once, so the
  numbers sum to the total rather than past it.
- **A pre-flight verdict per action** — `PROCEED`, `HOLD`, or `HOLD_PARTIAL` — carrying
  the evidence behind it: which feed answered, when it was collected, precisely which
  assets it covered, and what it could not see.
- **An approval-bound execution manifest** with an immutable source-scope ID, per-site
  rollout waves ordered by risk, and a SHA-256 plan hash that approval binds to.
- **A verification receipt**: findings before and after, what retired, what reappeared,
  and the measured risk delta.

## How it works

Ranking is greedy weighted maximum coverage over an action-to-findings coverage matrix,
not a sort by severity. Each candidate is scored on marginal weighted coverage, so an
action whose findings are already retired by a higher-ranked action earns nothing for
them. Under a pure cardinality constraint this is the classical greedy with its
(1 − 1/e) approximation guarantee; the repository is explicit about which options
forfeit that bound and which preserve it.

The safety model is fail-closed by construction. Every gate reads typed evidence
carrying its source, collection time, and completeness. Evidence that is unconfigured,
failed, partial, truncated, or stale reads as `UNKNOWN`, and `UNKNOWN` produces `HOLD` —
so forgetting to wire up a feed can only ever make the agent *less* willing to act. An
empty result from a healthy feed is a genuinely different state and does clear the gate.
A server under active attack is not patched over.

The agent holds no external write tools and no credentials. It proposes; separately
authorized tools that you already run — ticketing, patch management, cloud, CI/CD —
execute, and every external mutation takes its own explicit human approval, with the
approval bound to a specific plan hash and step so it cannot be transferred to another
change. Verification then re-queries the authoritative source and diffs against the
recorded baseline, because "we fixed it" is a claim and the delta is evidence.
