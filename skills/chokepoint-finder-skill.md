---
last_reviewed: 2026-08-05
name: "Chokepoint Finder Skill"
author: "tarhou"
github_url: "https://github.com/tarhou/chokepoint-finder-skill"
description: "A dependency-free Claude skill that groups vulnerability findings by the fix they share and ranks the shortest set of actions that retires the most weighted risk."
license: "MIT"
tier: "contributed"
tags: ["vuln-management", "exposure-management", "remediation", "prioritization", "set-cover", "no-dependencies", "claude-code"]
integrations: ["AWS", "Tenable"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T02:04:27Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "chokepoint-finder"
---

The portable form of the Chokepoint Finder method: a folder copy into
`~/.claude/skills/chokepoint-finder/`, no packages to install, no credentials held, and
a bundled ranking script that imports only the Python standard library.

## What it does

Ask "what should we fix first?" and Claude runs a remediation decision loop rather than
handing back a sorted severity list. Findings are grouped by the fix they share — a
patch, a base image, an IAM role, a security group — and the skill returns the shortest
ordered set of actions that retires the most weighted risk, with each action scored on
what it removes *given everything above it is already done*.

Data access happens through whatever MCP servers the operator already runs (Tenable,
AWS, or plain CSV and JSON exports). The skill itself reaches nothing and holds nothing.

## How it works

The bundled `scripts/chokepoint.py` is a single stdlib-only file that does exactly one
job: it groups findings by fix-sharing keys and ranks the result by marginal weighted
coverage — the classical greedy for weighted maximum coverage, with its (1 − 1/e)
approximation guarantee under a cardinality constraint. An effort-weighted mode is
offered separately and documented as a cost-benefit heuristic that carries no such
guarantee, because claiming a bound the code does not satisfy would be worse than
claiming none.

Everything the script does *not* do is the skill's operating discipline in `SKILL.md`:
gathering data, pre-flight safety checks, the out-of-band threat-intel policy, per-step
human approval, per-site rollout waves, and verification before a change record closes.
That separation is deliberate and stated in the repository's limitations — the script
ranks and nothing else, it never holds credentials, it never mutates anything, and both
of its output modes explicitly report that no approval artifact exists and execution is
unauthorized.

Site mapping fails closed: missing or nonconforming site names, absent crown-jewel or
criticality classifications, or an all-crown-jewel target set produce a hold and no
execution waves, rather than a confident guess. Bundled threat-intel flags are a pinned,
dated snapshot, and the demo estate is synthetic — its convergence is realistic in
shape, but every number it produces is labelled illustrative.

Run `python3 scripts/chokepoint.py --demo` for a deterministic worked example, or
`--sample` to see the input schema by example. The test suite covers the ranking
mathematics and the fail-closed behaviours.
