<h1 align="center">CyberAgents Exchange</h1>

<p align="center">
  <strong>The open exchange for cybersecurity AI agents.</strong><br>
  Open-source. Vendor-neutral. Built for security teams.
</p>

<p align="center">
  <a href="https://exchange.tenable.com/"><img src="https://img.shields.io/badge/exchange.tenable.com-E7FF00?style=flat-square&logo=googlechrome&logoColor=1E2426&label=website&labelColor=1E2426" alt="Website"></a>
  <a href="https://github.com/tenable/cyberagents-exchange/actions/workflows/validate.yml"><img src="https://github.com/tenable/cyberagents-exchange/actions/workflows/validate.yml/badge.svg" alt="Validate Content"></a>
  <a href="https://github.com/tenable/cyberagents-exchange/graphs/contributors"><img src="https://img.shields.io/github/contributors/tenable/cyberagents-exchange?style=flat-square&color=71FFC6" alt="Contributors"></a>
  <a href="https://github.com/tenable/cyberagents-exchange/stargazers"><img src="https://img.shields.io/github/stars/tenable/cyberagents-exchange?style=flat-square&color=FF8837" alt="Stars"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs welcome"></a>
</p>

<p align="center">
  <a href="https://exchange.tenable.com/discord"><img src="https://img.shields.io/badge/Discord-join%20us-5865F2?style=flat-square&logo=discord&logoColor=white" alt="Discord"></a>
  <a href="https://x.com/CyberAgentEx"><img src="https://img.shields.io/badge/follow-%40CyberAgentEx-000000?style=flat-square&logo=x&logoColor=white" alt="X"></a>
  <a href="https://www.youtube.com/@CyberAgentEx"><img src="https://img.shields.io/badge/YouTube-%40CyberAgentEx-FF0000?style=flat-square&logo=youtube&logoColor=white" alt="YouTube"></a>
</p>

---

This repository is the content source for the CyberAgents Exchange — a community directory of open-source AI agents, skills, MCP servers, and playbooks for cybersecurity.

## Mission

Security teams are experimenting with AI agents. These innovations are happening in silos. CyberAgents Exchange breaks those silos — a community-driven directory where security professionals discover, share, and chain open-source AI agents.

## What It Is

CyberAgents Exchange is a directory, not a code host. **Listing metadata lives here — the actual agent code lives in contributors' own GitHub repositories.** You always get code directly from the author.

The exchange indexes four types of content:

| Type | What it is | Directory |
|------|-----------|-----------|
| **Agents** | AI agents and tools that automate security tasks | [`agents/`](agents/) |
| **Skills** | Reusable agent skills that extend AI coding assistants with security capabilities | [`skills/`](skills/) |
| **MCP Servers** | Model Context Protocol servers for agent connectivity | [`mcp-servers/`](mcp-servers/) |
| **Playbooks** | Multi-agent workflows that chain agents together into end-to-end security processes | [`playbooks/`](playbooks/) |

Browse everything at **[exchange.tenable.com/browse](https://exchange.tenable.com/browse/)**.

## How It Works

Each listing is a single markdown file: YAML frontmatter holding the metadata, and a markdown body describing the project. Contributors submit listings via pull request. Agents are vendor-neutral and run anywhere — not locked to a single platform or license.

When a PR opens, [`validator.py`](validator.py) runs automatically to check required fields, controlled vocabularies, and file placement. Two maintainers then review against the [contributing checklist](docs/contributing_checklist.md). Merged listings are published to the website on the next build.

## Contributing

**Read [CONTRIBUTING.md](CONTRIBUTING.md) before you submit.** It covers repository requirements, the Contribution Agreement, frontmatter reference for every listing type, and what reviewers check.

Anyone can contribute. The fastest path is the [CyberAgents Exchange Submission Builder](https://github.com/jtbuchanan-tenb/cyberagent-exchange-submission-builder) skill for Claude Code — install it, run `/cyberagents-exchange-submit` from your project directory, and it validates your repo, gathers metadata, generates the listing, and opens the PR. It takes about five minutes.

Prefer to do it by hand? Start from a template in [`templates/`](templates/) and follow the [manual submission steps](CONTRIBUTING.md#manual-submission).

Before you start, your project needs:

- A **public GitHub repository** owned by a personal account (not an EMU account)
- An **open-source license** — MIT recommended, Apache 2.0 also welcome
- **No secrets** anywhere in the git history
- A **README** covering purpose, prerequisites, how to run it, outputs, and known limitations

See the [Contribute page](https://exchange.tenable.com/contributing/) for a walkthrough.

## Show It Off

Once your listing goes live, add this badge to your README to showcase your contribution.

[![Listed on CyberAgents Exchange](https://img.shields.io/badge/CyberAgents%20Exchange-Listed-E7FF00?style=flat-square&labelColor=1E2426)](https://exchange.tenable.com/)

```markdown
[![Listed on CyberAgents Exchange](https://img.shields.io/badge/CyberAgents%20Exchange-Listed-E7FF00?style=flat-square&labelColor=1E2426)](https://exchange.tenable.com/)
```

Also, every contributor gets a profile page at `exchange.tenable.com/contributors/<your-github-handle>`!

<details>
<summary>HTML variant</summary>

```html
<a href="https://exchange.tenable.com/"><img src="https://img.shields.io/badge/CyberAgents%20Exchange-Listed-E7FF00?style=flat-square&labelColor=1E2426" alt="Listed on CyberAgents Exchange"></a>
```

</details>

## Repository Layout

```
agents/          One markdown file per agent listing
skills/          One markdown file per skill listing
mcp-servers/     One markdown file per MCP server listing
playbooks/       One markdown file per playbook listing
templates/       Starter templates for each listing type
docs/            Contribution Agreement, reviewer checklist
validator.py     Schema + controlled-vocabulary validation
```

`validator.py` is the source of truth for allowed field values. To propose a new integration, platform, or client, add it in alphabetical order to the relevant `Literal[...]` list and include the change in your listing PR — see [Adding to the Controlled Vocabulary](CONTRIBUTING.md#adding-to-the-controlled-vocabulary).

### Running the validator locally

```bash
uv sync
uv run ./validator.py
```

Optionally install the pre-commit hooks so validation runs on every commit:

```bash
uv run pre-commit install
```

## FAQ

**Is this a marketplace? Do agents cost money?**
No. The exchange is free and open-source. There are no fees to list or use agents. All code is hosted on contributors' public GitHub repositories.

**Is this only for Tenable products?**
No. The exchange is vendor-neutral. Agents can integrate with any security product — Tenable, CrowdStrike, SentinelOne, or anything else. Best on Tenable One, but built for all.

**What's the difference between an agent, a skill, an MCP server, and a playbook?**
In short: agents run tasks, skills extend coding assistants, MCP servers expose data to agents, and playbooks chain agents into multi-step workflows. Full definitions are in [CONTRIBUTING.md](CONTRIBUTING.md).

**Who's behind this?**
CyberAgents Exchange is built and maintained by Tenable's Agentic AI Accelerator practice. Tenable provides the platform, review infrastructure, and flagship agents — the community provides the ecosystem.

More at [exchange.tenable.com/about](https://exchange.tenable.com/about/).

## Questions & Support

- **Community chat** — [join us on Discord](https://exchange.tenable.com/discord) for questions, help, and what's landing next
- **General questions** — visit [exchange.tenable.com](https://exchange.tenable.com/)
- **Issues & feature requests** — [open a GitHub issue](https://github.com/tenable/cyberagents-exchange/issues)
- **Security concerns with a listed contribution** — reach out to the repository owner; if needed, use [GitHub Security Advisories](https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories)

Come hang out on [Discord](https://exchange.tenable.com/discord), and follow along on [X](https://x.com/CyberAgentEx) and [YouTube](https://www.youtube.com/@CyberAgentEx).

Listings are licensed by their respective authors — check each linked repository for its license. See [SECURITY.md](SECURITY.md) and the [CyberAgents Contribution Agreement](docs/CyberAgents_Contribution_Agreement).
