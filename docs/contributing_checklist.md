# Contributing Checklist

This is the checklist every submission to the CyberAgents Exchange is verified against. It is written for contributors — so you know exactly what we confirm before your listing is accepted — and it is the runbook reviewers execute, item by item, when reviewing your pull request.

Field vocabularies (which integrations, platforms, clients, etc. are allowed) are **not** duplicated here. The canonical source is [`validator.py`](../validator.py) in this repository. This document is the source of truth for *policy*; `validator.py` is the source of truth for *allowed values*.

## Rejected at Submission (regardless of tier)

A submission is rejected outright, at any tier, if it involves any of the following:

- **Offensive or weaponized agents** — designed to exploit, move laterally, or exfiltrate data.
- **Hardcoded secrets** — any submission whose linked repository contains committed credentials or API keys is rejected outright.
- **Undisclosed outbound calls** — all outbound data flows must be documented in the linked repository.
- **Competitor targeting** — anything designed to disrupt or surveil a third party.
- **Weakening security controls** — disabling logging, EDR, or firewalls without justification.

## Trust Tiers (overview)

| Tier | Label | `tier` value in frontmatter | Status |
|------|-------|------------------------------|--------|
| 1 | Unreviewed / Contributed | `unreviewed` | Active |
| 2 | Community Reviewed | `community-reviewed` | Criteria TBD |
| 3 | Tenable Vetted | `certified` | Criteria TBD |

## Shared / Controlled Vocabularies

Several frontmatter fields must use values from a controlled vocabulary. These fields are: `tier`, `type` (agents), `integrations`, `compatible_platforms` (skills), `compatible_clients` / `transport` / `auth_method` / `runtime` (MCP servers), and the playbook `playbook_type` and `agents_used[].type`.

**Policy:** every controlled-vocabulary value must match the current vocabulary defined in [`validator.py`](../validator.py). A genuinely new value (e.g., a vendor or platform not yet listed) is allowed **only if the same pull request also updates `validator.py`** to add it, inserted alphabetically. Reviewers verify field values against the live `validator.py` at review time, so this document never lists the values themselves.

## Tier 1 — Unreviewed / Contributed

**What it signals:** this submission has been received and meets the minimum listing bar. Two Tenable employees, working from this checklist, must both sign off — as sequential GitHub reviews. Reviewer 1 reviews and approves, then requests a second reviewer via GitHub. Reviewer 2 independently reviews and, on approval, notes that two approvals are met and the pull request will be merged. Any missing requirement is returned as a `REQUEST_CHANGES` review with specific feedback. The official decision log is the GitHub pull request review(s).

> **Baseline review disclaimer (recorded verbatim in every Tier 1 review):**
> Contributed Agents have undergone a baseline review to confirm adherence to structural and coding standards and to identify overtly malicious, deceptive, or unauthorized behavior. This review does not constitute a comprehensive security audit and should not be interpreted as an assurance that the component is free from defects, vulnerabilities, or unintended functionality.

### Phase 1 — Automated Screening

Runs before human judgment. Any failure stops the review and is returned as `REQUEST_CHANGES`.

- [ ] **Secret scanning** — the linked repository is scanned with `gitleaks` across full git history. Any detected credential is an immediate rejection.
- [ ] **License detection** — the linked repository has a detectable open-source license. No license = rejected at submission.
- [ ] **Repository accessibility** — the linked repository is public, active (not archived or disabled), and reachable.

### Phase 2 — Listing Requirements

Both reviewers confirm all of the following are present.

**The submission (the pull request itself):**

- [ ] Adds exactly ONE new markdown file.
- [ ] The file is in the correct content directory for its kind: agents → `agents/`, MCP servers → `mcp-servers/`, skills → `skills/`, playbooks → `playbooks/`. The kind is determined by the directory (and validated by that directory's schema in `validator.py`). Only `agents/` listings carry a frontmatter `type` field (`agent`, `tool`, or `mcp-server`); note that an agent with `type: mcp-server` still lives in `agents/`, not `mcp-servers/`.
- [ ] Filename is a valid slug (lowercase, hyphens, no spaces or special characters) with no conflict against existing files.
- [ ] Pull request title follows `Add listing: <Name>`.
- [ ] Frontmatter passes `validator.py` schema validation for its type (all required fields present and valid).
- [ ] All controlled-vocabulary fields validate against the live `validator.py` (see Shared / Controlled Vocabularies).
- [ ] `tier` is `unreviewed`.
- [ ] `date_added` is a real, plausible date (not the `2026-01-01` template default, not absurdly in the future).
- [ ] No leftover template placeholders remain (e.g., `your-github-username`, `tag1`/`tag2`, example URLs, stub body text).
- [ ] The body contains real "What it does" / "How it works" content, not the template stub.

**The linked repository:**

- [ ] Public GitHub repository owned by a verifiable account (not an Enterprise Managed User account — the `<org>_<name>` underscore pattern; hyphens like `name-tenb` are fine).
- [ ] README describes: what the agent does, prerequisites, how to run it, what it outputs, and known limitations.
- [ ] Installation instructions are present, are not hallucinated, follow best practices, and are straightforward for an end user to follow — congruent with the actual repository (declared dependencies, entry points, and commands actually exist).
- [ ] A detectable open-source LICENSE file is present and matches the declared `license` SPDX identifier; manifest license fields (`package.json`, `pyproject.toml`, `Cargo.toml`) do not contradict it.

### Phase 3 — Congruence

The submission file must be congruent with the linked repository.

- [ ] `github_url` and `author` match the actual repository remote and owner.
- [ ] `name`, `description`, `type`, and `integrations` match what the repository actually is.
- [ ] Type-specific fields are congruent with the repository:
  - **Skill** — declared `compatible_platforms` and `invocation` are supported by repository signals (e.g., `SKILL.md`, platform rule files).
  - **MCP server** — `runtime` matches the manifest (node → `package.json`, python → `pyproject.toml`, etc.); `transport` matches the code (a stdio/http server transport is actually present); `tools_exposed` and `auth_method` are congruent with the code.
  - **Playbook** — `agents_used` references resolve; vendor-type agents appear only in sponsored playbooks.
- [ ] Claims in the listing body trace back to the README or repository content (no unsupported claims).

### Phase 4 — Baseline Behavioral Review

Human judgment, assisted by the reviewer skill. Records the disclaimer above.

- [ ] The tier-independent rejection criteria (offensive/weaponized, undisclosed outbound calls, competitor targeting, weakening controls) are re-checked in context of the actual repository.
- [ ] The repository adheres to reasonable structural and coding standards.
- [ ] No overtly malicious, deceptive, or unauthorized behavior is present.

## Tier 2 — Community Reviewed

*Criteria to be defined. Not yet active. When active, this tier's requirements are additive on top of Tier 1.*

## Tier 3 — Tenable Vetted

*Criteria to be defined. Not yet active. When active, this tier's requirements are additive on top of Tiers 1 and 2.*
