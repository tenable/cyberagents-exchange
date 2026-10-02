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
| 1 | Contributed | `contributed` | Active |
| 2 | Vetted | `vetted` | Active — Tenable-initiated, not contributor-submitted |

A tier 2 listing is additionally required to carry `vetted_on` and `vetted_commit_sha`, which
anchor the review to the exact commit it covered. `validator.py` rejects a `vetted` listing
missing either, and rejects both fields on a listing at any other tier.

## Shared / Controlled Vocabularies

Several frontmatter fields must use values from a controlled vocabulary. These fields are: `tier`, `integrations`, `domains`, `compatible_platforms` (skills), `compatible_clients` / `transport` / `auth_method` / `runtime` (MCP servers), and the playbook `playbook_type` and `agents_used[].type`.

**Policy:** every controlled-vocabulary value must match the current vocabulary defined in [`validator.py`](../validator.py). A genuinely new value (e.g., a vendor or platform not yet listed) is allowed **only if the same pull request also updates `validator.py`** to add it, inserted alphabetically. Reviewers verify field values against the live `validator.py` at review time, so this document never lists the values themselves.

`domains` is the exception to that addition path. The taxonomy is closed — the website mirrors it to build its browse filters and labels — so a submission PR may not introduce a new domain value. Route proposals to a GitHub issue and have the contributor pick the closest existing domain.

## Tier 1 — Contributed

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
- [ ] The file is in the correct content directory for its kind: agents → `agents/`, MCP servers → `mcp-servers/`, skills → `skills/`, playbooks → `playbooks/`. The kind is determined by the directory (and validated by that directory's schema in `validator.py`).
- [ ] Filename is a valid slug (lowercase, hyphens, no spaces or special characters) with no conflict against existing files.
- [ ] Pull request title follows `Add listing: <Name>`.
- [ ] Frontmatter passes `validator.py` schema validation for its type (all required fields present and valid).
- [ ] All controlled-vocabulary fields validate against the live `validator.py` (see Shared / Controlled Vocabularies).
- [ ] `tier` is `contributed`.
- [ ] `vetted_on` and `vetted_commit_sha` are absent. Both are set by Tenable when a listing is promoted to tier 2, never on a new submission.
- [ ] `partner_contribution` is absent unless the reviewer is adding it. It is set by Tenable, not the submitter, and marks a listing from a Tenable partner so it surfaces under Ecosystem → Partner AI Listings on the website. A submitter-supplied value is removed.
- [ ] `date_added` is a real, plausible date (not the `2026-01-01` template default, not absurdly in the future).
- [ ] `contribution_agreement_date` is present and is a valid ISO 8601 datetime (e.g., `2026-07-09T14:30:00Z`). Must not be the template default (`2026-01-01T00:00:00Z`), not absurdly in the future, and not before the repository was created.
- [ ] If `works_with_tenable_hexa_mcp` is present, it is a boolean (`true` or `false`). If `true`, the linked repository should demonstrate integration with the Tenable Hexa MCP (not other Tenable APIs such as VM or Security Center).
- [ ] `domains` is present with 1-2 unique values from the live vocabulary, first value primary. The schema treats the field as optional, but a listing merged without it is excluded from the website's domain filters — so it must be populated before merge. If the contributor omitted it, the reviewer proposes values and adds the field to the listing.
- [ ] No leftover template placeholders remain (e.g., `your-github-username`, `tag1`/`tag2`, example URLs, stub body text).
- [ ] The body contains real "What it does" / "How it works" content, not the template stub.
- [ ] If `visibility: example` is present in frontmatter, this is flagged prominently for maintainer attention (example listings are hidden from browse, leaderboard, and home page — only accessible via direct link).

**The linked repository:**

- [ ] Public GitHub repository owned by a verifiable account (not an Enterprise Managed User account — the `<org>_<name>` underscore pattern; hyphens like `name-tenb` are fine).
- [ ] README describes: what the agent does, prerequisites, how to run it, what it outputs, and known limitations.
- [ ] Installation instructions are present, are not hallucinated, follow best practices, and are straightforward for an end user to follow — congruent with the actual repository (declared dependencies, entry points, and commands actually exist).
- [ ] A detectable open-source LICENSE file is present and matches the declared `license` SPDX identifier; manifest license fields (`package.json`, `pyproject.toml`, `Cargo.toml`) do not contradict it.

### Phase 3 — Congruence

The submission file must be congruent with the linked repository.

- [ ] `github_url` and `author` match the actual repository remote and owner.
- [ ] `name`, `description`, and `integrations` match what the repository actually is.
- [ ] The primary domain (first value in `domains`) reflects what the listing actually does — not a template leftover, and not a reflexive `vulnerability-management` or `platform-operations`.
- [ ] Type-specific fields are congruent with the repository:
  - **Skill** — the repository must be structured so that each declared `compatible_platform` can actually load the skill. At minimum, a `SKILL.md` with `name`/`description` YAML frontmatter must exist at the repo root. All files referenced within SKILL.md (e.g., `references/`) must exist. Installation instructions must be specific and actionable for each declared platform (not generic "install the skill"). Declared `invocation` must appear in SKILL.md or README.
  - **MCP server** — `runtime` matches the manifest (node → `package.json`, python → `pyproject.toml`, etc.); `transport` matches the code (a stdio/http server transport is actually present); `tools_exposed` and `auth_method` are congruent with the code.
  - **Playbook** — `agents_used` references resolve; vendor-type agents appear only in sponsored playbooks.
- [ ] If the repository contains archive files (e.g., `.skill`, `.zip`, `.tar.gz`), the skill content must ALSO exist in unpacked form at the repo root (`SKILL.md` + any referenced files). Repos where the skill is only accessible by extracting an archive will be rejected — the repo must be directly installable without extraction. Archives as supplementary convenience downloads are acceptable but will be extracted and inspected for congruence and safety.
- [ ] Claims in the listing body trace back to the README or repository content (no unsupported claims).

### Phase 4 — Baseline Behavioral Review

Human judgment, assisted by the reviewer skill. Records the disclaimer above.

- [ ] The tier-independent rejection criteria (offensive/weaponized, undisclosed outbound calls, competitor targeting, weakening controls) are re-checked in context of the actual repository.
- [ ] The repository adheres to reasonable structural and coding standards.
- [ ] No overtly malicious, deceptive, or unauthorized behavior is present.

## Tier 2 — Vetted

**What it signals:** this listing passed a review by the CyberAgents Exchange AI Inspector — the
highest level of review a listing can receive on the Exchange. The requirements below are
**additive on top of Tier 1**, which must already be satisfied.

Vetting is a **promotion review for a listing already live at Tier 1**, not a separate submission
path. Tenable selects listings for review at its discretion as the Exchange grows, and each review
is pinned to an exact commit.

**Tier 2 is not contributor-initiated, and promotion is not a contributor task.** `tier`,
`vetted_on` and `vetted_commit_sha` are Tenable-set, as recorded in `CONTRIBUTING.md`. On approval
Tenable writes all three into the listing's frontmatter itself, using its push access — the
contributor is not asked to make the edit, and promotion is not held open as a change request.
This is the same mechanism that already records `last_reviewed` at Tier 1. `validator.py` enforces
the pairing: it rejects a `vetted` listing missing either field, and rejects either field on a
listing at any other tier.

> **Vetted review disclaimer (recorded verbatim in every Tier 2 promotion):**
> This listing passed the CyberAgents Exchange AI Inspector security review at the commit recorded
> in `vetted_commit_sha`. The review covers that commit only. It is not a standing approval of a
> branch, a future release, or the repository as a whole, and it is not a warranty, a
> certification, or an endorsement of the contributor.

### Eligibility

- [ ] The listing is already live at Tier 1, with both Tier 1 approvals on record.
- [ ] Tenable has selected the listing for Exchange Inspector review.
- [ ] The exact commit under review is identified, and the review is pinned to it.
- [ ] The contributor has a completed contributor profile on the Exchange.
- [ ] A contact route exists — an email address, or a linked account in the Exchange Discord server — so the contributor can be reached if issues arise.
- [ ] **Independence:** the security reviewer and the promotion approver have each neither authored the contribution, nor own the repository, nor hold any other conflict of interest. This applies identically to Tenable's own listings and to partner listings.

### Stage 1 — Automated inspection (Tenable One AI Exposure)

The skills inspection engine parses the component's instructions, the tools it can invoke, and the
data it can reach. It clears the obviously safe, blocks the obviously unsafe, and passes everything
else forward with its findings attached.

- [ ] The component has been through the inspection engine, and its findings are attached to the review record. The engine covers, at minimum:
  - prompt injection and jailbreak attempts
  - hidden or invisible instructions
  - hardcoded secrets
  - PII exposure
  - sensitive data access

### Stage 2 — Frontier assessment (OpenAI GPT Cyber models)

Reasoning about how the component could be abused, not whether it matches a known signature.

- [ ] The source has been assessed for how untrusted content could reach the model, what a hijacked agent could do with its tool permissions, and where a chain of individually harmless actions becomes a harmful one.
- [ ] Higher-risk and dual-use submissions were routed to more capable, purpose-trained models.
- [ ] Any model refusal is recorded as a review signal. A refusal is never treated as a clean pass.

### Stage 3 — Expert review and runtime verification (Tenable security researchers)

- [ ] Stage 1 and Stage 2 findings are validated rather than taken at face value.
- [ ] A threat model is written for the component.
- [ ] Every security-relevant surface in the source is reviewed.
- [ ] The dependency and build chain is assessed.
- [ ] The trustworthiness of the repository owner and maintainers is assessed.
- [ ] The component is installed and run in a clean, isolated environment, using only its documented setup steps.
- [ ] Observed behavior is compared against what the documentation claims. Any discrepancy is recorded as a finding.

### Coverage — the fifteen security issue classes

Every Tier 2 review tests all fifteen, across three layers. These are the floor, not the ceiling.

- [ ] All fifteen classes are tested and their results recorded:
  - **Model** — prompt injection; excessive agency; memory and context integrity; approval and intent failures
  - **Application** — tool and MCP server security; secrets handling; data exfiltration; output handling; conventional application flaws
  - **Infrastructure** — filesystem safety; code and command execution; network and web security; supply chain; denial of service

### Findings disposition

- [ ] Every **critical** and **high** severity finding is fixed and revalidated before promotion.
- [ ] Every **medium** and **low** severity finding is either fixed, or explicitly accepted with a named owner, a written rationale, and a follow-up date.
- [ ] No accepted residual risk overrides a "Rejected at Submission" criterion. Those are re-checked against the actual code at this tier and cannot be waived at any severity.
- [ ] Findings were worked through with the contributor directly. The goal is to promote strong listings, not to run an opaque rejection gate.

### The review record

Promotion requires a dated security review report. Reviewers confirm it records:

- [ ] The reviewed commit and artifact provenance.
- [ ] The threat model and data flows.
- [ ] The dependency and build assessment.
- [ ] The source review.
- [ ] The runtime verification steps and the behavior observed.
- [ ] Every finding, and how it was resolved.
- [ ] The promotion decision.
- [ ] The conditions that would trigger a re-review.

This record is what separates a vetted tag from a one-time automated pass.

### Decision

- [ ] The review ends in exactly one of: **approve**, **request changes**, or **decline promotion**.
- [ ] On approval, Tenable writes `tier: "vetted"`, `vetted_on` and `vetted_commit_sha` into the listing's frontmatter in a single change, using Tenable's push access rather than a change request to the contributor.
- [ ] The promotion is approved by someone independent of both the contribution and the review.

### Re-review on material change

A Tier 2 review covers one commit. Contributors keep their code and may change it at any time; when
a vetted listing changes materially from its reviewed commit, the new version may require another
review before the vetted tag continues to apply. Material changes include, but are not limited to:

- Authentication or authorization behavior, or required permissions and API scopes
- Network destinations, telemetry, or data handling
- Prompts, system instructions, tools, resources, or playbook steps
- Dependencies, lockfiles, build scripts, install scripts, or release artifacts
- Filesystem access, process execution, or export behavior
- Tenable product integration, or read versus write capability
- Any security finding that changes the previous risk decision

The public description of this process, written for people evaluating a listing rather than for
reviewers executing one, is on the Exchange at
<https://exchange.tenable.com/security-review-process>. The two must stay in step: that page is
where this tier is explained to the people who rely on it.
