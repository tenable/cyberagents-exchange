# Contributing to the CyberAgents Exchange Powered by Tenable

Thanks for your interest in contributing! The CyberAgents Exchange powered by Tenable is a community directory of cybersecurity AI agents, skills, MCP servers, and playbooks. Your code stays in your own GitHub repository — you submit a listing file that points to it.

This guide walks you through everything you need to know to get your submission accepted.

## Before You Start

Make sure your project meets these requirements:

### Repository Requirements

- **Public GitHub repository** — your repo must be public and accessible (not archived or disabled).
- **Personal GitHub account** — your repo must be owned by a personal GitHub account, not an Enterprise Managed User (EMU) account. EMU accounts typically follow the `orgname_username` pattern (with an underscore). Accounts with hyphens (like `name-tenb`) are fine.
- **Open-source license** — your repo must include a `LICENSE` file with a permissive open-source license. We recommend **MIT**. Apache 2.0 is also welcome. GPL v3 and other restrictive licenses may be considered in exceptional cases — [open a GitHub issue](https://github.com/tenable/cyberagents-exchange/issues) to start that conversation.
- **No secrets in git history** — your repository (including its full git history) must be free of credentials, API keys, and secrets. This is scanned automatically.
- **README** — your README should describe what the project does, prerequisites, how to run it, what it outputs, and known limitations.

### Contribution Agreement

By submitting a listing, you agree to the [CyberAgents Contribution Agreement](https://github.com/tenable/cyberagents-exchange/blob/main/docs/CyberAgents_Contribution_Agreement). If you submit manually (not via the submission builder skill), you must:

1. Include the following statement in your pull request description:

   > I have reviewed and accept the [CyberAgents Contribution Agreement](https://github.com/tenable/cyberagents-exchange/blob/main/docs/CyberAgents_Contribution_Agreement).

2. Set the `contribution_agreement_date` field in your listing frontmatter to the ISO 8601 date and time when you accepted the agreement (e.g., `2026-07-09T14:30:00Z`).

## The Recommended Way: Submission Builder Skill

We strongly recommend using the **[CyberAgents Exchange Submission Builder](https://github.com/jtbuchanan-tenb/cyberagent-exchange-submission-builder)** skill for Claude Code. It handles the entire process for you:

- Validates your repository meets all requirements
- Captures your confirmation of the Contribution Agreement and includes the required acceptance statement in your PR
- Interviews you to gather the right metadata
- Generates a correctly-formatted listing file
- Forks the exchange repo, creates a branch, and opens the PR

Install it and run `/cyberagents-exchange-submit` from your project directory. It takes about five minutes.

## Manual Submission

If you prefer to submit by hand, here's the process:

### 1. Fork and Branch

1. Fork [tenable/cyberagents-exchange](https://github.com/tenable/cyberagents-exchange).
2. Create a branch named `add-<your-slug>` (e.g., `add-my-cool-agent`).

### 2. Create Your Listing File

Copy the appropriate template from the [`templates/`](https://github.com/tenable/cyberagents-exchange/tree/main/templates) directory to get started:

| Type | Template | Target Directory |
|------|----------|------------------|
| Agent | `templates/agent-template.md` | `agents/` |
| Skill | `templates/skill-template.md` | `skills/` |
| MCP Server | `templates/mcp-server-template.md` | `mcp-servers/` |
| Playbook | `templates/playbook-template.md` | `playbooks/` |
| n8n Playbook | `templates/n8n-playbook-template.md` | `playbooks/` |

Copy your template into the correct target directory and rename it to a valid slug: lowercase letters, numbers, and hyphens only (e.g., `my-cool-agent.md`).

Your listing file has two parts: YAML frontmatter (the metadata) and a markdown body (the description).

### 3. Write the Frontmatter

Every field in the frontmatter must pass validation. The sections below show what's required for each type.

Several fields use a **controlled vocabulary** — a fixed set of allowed values defined in [`validator.py`](https://github.com/tenable/cyberagents-exchange/blob/main/validator.py). That file is always the most up-to-date source of truth for allowed values. Some common values are shown in the examples below, but always check `validator.py` for the complete lists.

If you need a value that isn't in the vocabulary yet (a new integration, platform, or client), see [Adding to the Controlled Vocabulary](#adding-to-the-controlled-vocabulary) below.

#### Agent

```yaml
---
name: "Your Agent Name"
author: "your-github-username"
github_url: "https://github.com/your-username/your-repo"
description: "A one-line description of what it does."
license: "MIT"
tier: "contributed"
tags: ["tag1", "tag2"]
domains: ["vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-07-09
contribution_agreement_date: 2026-07-09T14:30:00Z
works_with_tenable_hexa_mcp: false
---
```

- `tier` is always `contributed` for new submissions
- `integrations` uses a controlled vocabulary — see `validator.py` for the full list
- `domains` — one or two values from a controlled vocabulary; the first is the primary domain. See [Domains](#domains)
- `contribution_agreement_date` — the ISO 8601 date and time when you accepted the Contribution Agreement (e.g., `2026-07-09T14:30:00Z`)
- `works_with_tenable_hexa_mcp` — optional boolean; set to `true` if your submission integrates with Tenable products via the [Tenable Hexa AI MCP Server](https://docs.tenable.com/vulnerability-management/Content/getting-started/hexa-AI-MCP.htm). Omit or set to `false` if it uses other Tenable APIs (VM, Security Center, etc.) or does not integrate with Tenable at all

#### Skill

```yaml
---
name: "Your Skill Name"
author: "your-github-username"
github_url: "https://github.com/your-username/your-repo"
description: "A one-line description of what it does."
license: "MIT"
tier: "contributed"
tags: ["tag1", "tag2"]
domains: ["vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-07-09
contribution_agreement_date: 2026-07-09T14:30:00Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "your-skill-name"
---
```

- `compatible_platforms` uses a controlled vocabulary (e.g., `Claude Code`, `Cursor`, `Windsurf`) — see `validator.py` for the full list
- `invocation` is the slash command or trigger name
- `domains` — one or two values from a controlled vocabulary; the first is the primary domain. See [Domains](#domains)

#### MCP Server

```yaml
---
name: "Your MCP Server Name"
author: "your-github-username"
github_url: "https://github.com/your-username/your-repo"
description: "A one-line description of what it does."
license: "MIT"
tier: "contributed"
tags: ["tag1", "tag2"]
domains: ["vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-07-09
contribution_agreement_date: 2026-07-09T14:30:00Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop"]
transport: "stdio"
runtime: "python"
auth_method: "api-key"
tools_exposed:
  - name: "tool_name"
    description: "What this tool does"
resources_exposed: []
prompts_exposed: []
---
```

- `transport` must be `stdio`, `http`, or `both`
- `runtime` must be `binary`, `bun`, `go`, `node`, `python`, or `rust`
- `auth_method` must be `api-key`, `none`, `oauth2`, or `token`
- `compatible_clients` uses a controlled vocabulary — see `validator.py` for the full list
- `domains` — one or two values from a controlled vocabulary; the first is the primary domain. See [Domains](#domains)

#### Playbook

```yaml
---
name: "Your Playbook Name"
author: "your-github-username"
github_url: "https://github.com/your-username/your-repo"
description: "A one-line description of what it does."
license: "MIT"
tier: "contributed"
tags: ["tag1", "tag2"]
domains: ["vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-07-09
contribution_agreement_date: 2026-07-09T14:30:00Z
works_with_tenable_hexa_mcp: false
playbook_type: "standard"
agents_used:
  - name: "Agent Name"
    role: "What this agent does in the playbook"
    type: "exchange"
    ref: "slug-of-exchange-listing"
---
```

- `playbook_type` must be `standard`, `sponsored`, or `n8n`
- `agents_used[].type` must be `exchange`, `github`, `info`, or `vendor` (only `sponsored` playbooks may include `vendor`-type agents)
- `ref` links to an existing exchange listing or GitHub URL depending on the agent type
- `domains` — one or two values from a controlled vocabulary; the first is the primary domain. See [Domains](#domains)

#### Domains

`domains` places your listing in the Exchange's security domain taxonomy. It powers the domain filters on the browse page, so a listing without it won't show up when someone filters by domain.

The rules:

- One or two values, no duplicates.
- **The first value is the primary domain.** Pick the domain your listing's main job belongs to — not every domain it touches.
- Add a second value only when the listing genuinely straddles two domains.

| Value | Label | What belongs here |
|-------|-------|-------------------|
| `ai-security` | AI Security | Security *of* AI systems: agent and MCP security, AI-SPM, prompt-injection testing. Not "this is an AI agent" — nearly everything here is. |
| `application-security` | Application Security | SAST/DAST, dependency and supply-chain risk, secrets in code, secure SDLC, API security. |
| `cloud-security` | Cloud Security | CSPM/CNAPP, cloud misconfiguration, container and Kubernetes posture, cloud attack paths. |
| `cryptography-pki` | Cryptography & PKI | TLS and certificate posture, post-quantum readiness, key management. |
| `data-security` | Data Security | Data discovery and classification, DLP, database security, sensitive-data exposure. |
| `email-collaboration-security` | Email & Collaboration Security | Phishing analysis, email gateway and header forensics, Slack/Teams/SaaS collaboration risk. |
| `governance-risk-compliance` | Governance, Risk & Compliance | Framework and benchmark mapping, audit evidence, policy, risk quantification, reporting to leadership. |
| `identity-access` | Identity & Access | IAM and entitlement review, privilege escalation paths, MFA and SSO posture, Active Directory and Entra ID. |
| `network-security` | Network Security | Firewall and segmentation review, network device configuration, traffic and perimeter analysis. |
| `ot-iot-security` | OT/IoT Security | ICS/SCADA, medical and embedded devices, industrial protocols. |
| `platform-operations` | Platform Operations | **Not a security domain.** Platform health checks, licensing, scan operations, exports and reporting, API connectors, onboarding and setup helpers. Use it when the main job is operating or administering a security platform rather than performing a security function. |
| `security-awareness` | Security Awareness | Training content, phishing simulation, secure-behavior coaching. |
| `security-operations` | Security Operations | SIEM/EDR/NDR work, threat hunting, detection engineering, incident response, malware analysis, insider threat. |
| `threat-intelligence` | Threat Intelligence | IOC and actor research, CVE and exploit intelligence enrichment, threat feeds, attribution. |
| `vulnerability-management` | Vulnerability Management | Core VM workflows only: scanning, prioritization, remediation tracking, exposure and risk scoring for known vulnerabilities. |

Two of these get over-claimed. Don't reach for `vulnerability-management` unless VM is genuinely your listing's primary function, and use `platform-operations` when your listing runs a platform rather than secures something.

If you leave `domains` out, a reviewer will propose values during review — but you know your project better than we do, so pick them yourself.

### 4. Write the Body

Below the frontmatter, write a markdown description that covers:

- **What it does** — a clear explanation of the project's purpose and capabilities
- **How it works** — a brief overview of the approach

This should be substantive, original content — not a copy of the README. Make sure to replace all template placeholder text with your own content.

### 5. Open a Pull Request

1. Commit your listing file (and any `validator.py` updates if needed — see [below](#adding-to-the-controlled-vocabulary)).
2. Push to your fork.
3. Open a PR against `tenable/cyberagents-exchange` with the title: **`Add listing: Your Agent Name`**
4. Include the Contribution Agreement acceptance statement in your PR description (see [above](#contribution-agreement)).

## What Happens After You Submit

Your submission is validated automatically and then reviewed by two maintainers who work through the [contributing checklist](https://github.com/tenable/cyberagents-exchange/blob/main/docs/contributing_checklist.md) item by item. Every item on that checklist is verified before your listing is accepted.

Here's what will be checked:

### Automated Validation

The [`validator.py`](https://github.com/tenable/cyberagents-exchange/blob/main/validator.py) script runs automatically when you open your PR. It checks that:

- Your frontmatter has all required fields for your submission type
- All controlled-vocabulary fields use valid values
- Your file is in the correct directory
- Schema validation passes

If validation fails, you'll see the errors in the PR checks. Fix them and push again.

### Review Checks

Reviewers will also verify:

- Your linked repository is public, accessible, and not owned by an EMU account
- A valid open-source license is present and matches what you declared
- No secrets exist anywhere in the git history
- Your README covers the required topics (purpose, prerequisites, how to run, outputs, limitations)
- Installation instructions are accurate — referenced files, packages, and commands actually exist
- The metadata in your listing (name, description, integrations) accurately reflects what's actually in the repository
- Claims in your listing body are supported by the README or repository content
- The project follows reasonable coding standards and doesn't contain malicious, deceptive, or unauthorized behavior

If anything needs attention, you'll receive specific feedback as a review comment on your PR.

### How PRs Are Merged

All pull requests are merged using **squash and merge** — the entire PR is combined into a single commit on `main`. Merge commits and rebase merges are disabled, so squash is the only option. The squash commit uses your PR title and description, so please keep them clear and descriptive. The source branch is deleted automatically after the merge.

### Add the Badge

Once your listing is merged, add the "Listed on CyberAgents Exchange" badge to your own README — see [Show It Off](README.md#show-it-off) for the pitch and the profile page link.

```markdown
[![Listed on CyberAgents Exchange](https://img.shields.io/badge/CyberAgents%20Exchange-Listed-E7FF00?style=flat-square&labelColor=1E2426)](https://exchange.tenable.com/)
```

## Things That Will Get Your Submission Rejected

Regardless of how well-formatted your listing is, submissions are rejected outright if they involve:

- **Offensive or weaponized agents** — anything designed to exploit, move laterally, or exfiltrate data
- **Hardcoded secrets** — credentials or API keys anywhere in the repository's git history
- **Undisclosed outbound calls** — all outbound data flows must be documented
- **Competitor targeting** — anything designed to disrupt or surveil a third party
- **Weakening security controls** — disabling logging, EDR, or firewalls without justification

## Adding to the Controlled Vocabulary

Several frontmatter fields only accept values from a controlled vocabulary defined in [`validator.py`](https://github.com/tenable/cyberagents-exchange/blob/main/validator.py). The controlled fields are:

- `integrations` — vendor and platform names (e.g., `Tenable`, `AWS`, `Splunk`)
- `domains` — security domain taxonomy (e.g., `cloud-security`, `identity-access`) — see [Domains](#domains)
- `compatible_platforms` (skills) — AI coding platforms (e.g., `Claude Code`, `Cursor`)
- `compatible_clients` (MCP servers) — MCP client applications (e.g., `Claude Desktop`, `VS Code Copilot`)
- `transport` (MCP servers) — `stdio`, `http`, or `both`
- `auth_method` (MCP servers) — `api-key`, `none`, `oauth2`, or `token`
- `runtime` (MCP servers) — `binary`, `bun`, `go`, `node`, `python`, or `rust`
- `playbook_type` (playbooks) — `standard`, `sponsored`, or `n8n`
- `agents_used[].type` (playbooks) — `exchange`, `github`, `info`, or `vendor`

If your submission needs a value that doesn't exist yet (for example, a new integration vendor or a platform we haven't listed), you're welcome to propose it. Here's how:

1. Open `validator.py` and find the relevant `Literal[...]` list for the field you need to update.
2. Add your new value in **alphabetical order** within that list.
3. Include the `validator.py` change in the same pull request as your listing submission.

Your proposed addition will be reviewed alongside your listing. We welcome genuine additions — if a vendor, platform, or client exists and is relevant, we'll accept it.

**`domains` is the exception.** The domain taxonomy is closed: the Exchange website mirrors it to build its browse filters and display labels, so adding a domain takes a coordinated change across two repositories. Don't add a `domains` value in your submission PR — [open an issue](https://github.com/tenable/cyberagents-exchange/issues) to propose one, and pick the closest existing domain in the meantime.

## Updating an Existing Listing

To update a listing you previously submitted, open a PR that modifies your existing file. The same review process applies.

## Questions & Support

- General questions: visit the CyberAgents Exchange website
- Issues & feature requests: [github.com/tenable/cyberagents-exchange/issues](https://github.com/tenable/cyberagents-exchange/issues)
- Security concerns with a listed contribution: reach out to the repository owner; if needed, use [GitHub Security Advisories](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories)
