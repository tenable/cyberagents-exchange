---
last_reviewed: 2026-11-13
name: "Tenable Docs MCP"
author: "Lance Duvall"
github_url: "https://github.com/lanz/tenable-docs-mcp"
description: "Cited answers from Tenable's product documentation: searches an index of docs.tenable.com and its translated sites, kept up to date automatically, and links each answer to the exact section."
license: "GPL-3.0-or-later"
tier: "contributed"
tags: ["documentation", "docs", "citations", "search", "how-to", "release-notes", "tenable", "nessus", "security-center", "exposure-management"]
domains: ["platform-operations"]
integrations: ["Tenable"]
date_added: 2026-11-13
contribution_agreement_date: 2026-11-13T18:47:11Z
works_with_tenable_hexa_mcp: false
transport: "both"
runtime: "go"
auth_method: "none"
compatible_clients: ["Claude Desktop", "Claude Code", "VS Code Copilot", "Cursor", "Windsurf", "Gemini CLI", "Codex"]
tools_exposed:
  - name: "search_docs"
    description: "Rank the doc sections that answer a question, each with its link, product, version, language, and location in its guide"
  - name: "read_doc"
    description: "Read a section or a whole page as Markdown, with its product, version, required roles, and source link"
  - name: "outline"
    description: "List a page's headings, or a guide's pages from its table of contents"
  - name: "browse_guide"
    description: "Show a guide's name and table of contents in reading order"
  - name: "related_pages"
    description: "Find the pages around a page: its neighbors in the guide, the pages it links to and from, and the same page in other languages"
  - name: "list_products"
    description: "List the products, guides, older versions, and languages the index covers"
  - name: "find_setting"
    description: "Explain a setting: its description, default, valid values, and whether it's required, from the docs' settings tables"
  - name: "required_role"
    description: "Find the roles and permissions the docs say a task needs"
  - name: "requirements"
    description: "Look up system requirements: ports, hardware, operating systems, browsers, and dependencies"
  - name: "release_notes"
    description: "List release-note entries, newest first, by product, date range, version, and words"
  - name: "compare_versions"
    description: "Show how a page or a setting differs between two versions of an on-premises product"
  - name: "whats_changed"
    description: "List the pages added, updated, or removed since a date, with the sections each update changed"
  - name: "define_term"
    description: "Define a term, abbreviation, or product name, including retired product names"
  - name: "verify_citations"
    description: "Check every docs link in an answer or draft: that the page and anchor exist, and whether it points to an older version or a translation"
  - name: "report_gap"
    description: "Record a question the docs didn't answer, locally, and offer the user a form to send it to Tenable's documentation team"
  - name: "open_feedback_form"
    description: "Show the user the docs feedback form for a page, which they fill in themselves"
  - name: "index_status"
    description: "Show the server's version, what the index holds, and the state of its automatic updates"
  - name: "refresh_index"
    description: "Update given pages, or a whole guide, from the live docs sites"
resources_exposed:
  - name: "tenable-docs://status"
    description: "The server's version and what its documentation index holds"
  - name: "tenable-docs://page/{+doc_id}"
    description: "A docs page as Markdown"
  - name: "tenable-docs://guide/{+guide}/toc{?language}"
    description: "A guide's table of contents"
prompts_exposed:
  - name: "how-to"
    description: "Get the documented steps for a task"
  - name: "explain-setting"
    description: "Explain a setting: what it does, its options and default, and where to find it"
  - name: "troubleshoot"
    description: "Find the docs' guidance for a problem or error message"
  - name: "whats-new"
    description: "Summarize a release from the release notes"
  - name: "who-can"
    description: "Find the role or permission an action needs"
  - name: "upgrade-check"
    description: "Check what changes between two versions before upgrading"
  - name: "fact-check"
    description: "Check a reply, draft, or answer against the docs: which claims are right, wrong, or unsupported, with links and corrections"
---

Tenable Docs MCP grounds answers about Tenable products in the published documentation rather than in a model's training data. It covers every product, version, and language on docs.tenable.com, and each answer cites the exact section it draws on.

## What it does

A question such as how to install Nessus on Linux, which ports Security Center requires, or what a scan setting controls is answered from the relevant documentation, with the documented steps and a link to the section that contains them. Beyond full-text search, the server provides:

- **Structured lookups.** Settings, required roles, and system requirements are read from the documentation's own tables, so a response can state a setting's default and valid values, the role a task requires, or the ports a product uses, with the source cited.
- **Answers match your version.** Answers say which product version they're for, `compare_versions` shows how a page or setting changed between two releases of an on-premises product, and `whats_changed` lists what the docs changed since a date.
- **Multilingual coverage.** Questions in Japanese, French, German, Spanish, Korean, or Chinese are answered from that language's documentation, with the current English page alongside when a translation lags behind.
- **Citation verification.** `verify_citations` confirms that every documentation link in a response or draft resolves and that its anchor exists, flags links to older versions and translations, and proposes corrections for broken ones.
- **User-controlled feedback.** When the documentation doesn't cover a question, the server says so and can record the gap locally. Gap reports and page feedback reach Tenable's documentation team only through a form the user completes and approves; the model can't write them on the user's behalf.

API questions are better served by the Tenable Developer Portal MCP. The repository includes a companion skill that routes each question to the right server.

## How it works

The server is a single, self-contained Go binary that requires no credentials. It answers from a local SQLite index with full-text search, downloaded on first start from an index published at docs.tenable.com. It checks for updates daily, downloads only the parts that changed, and verifies each file's checksum. If the published index is unavailable, it can build the index from the live documentation sites, observing their robots.txt.

Network access is limited to Tenable's own sites: docs.tenable.com and its translated sites for the index, update checks, and live pages, and www.tenable.com only when the user submits feedback or a gap report through an approved form. The README documents each connection.

It runs over stdio for desktop and IDE clients, or over Streamable HTTP. A hosted mode runs it as stateless, read-only containers behind a load balancer.

It installs as a Claude Desktop extension (`.mcpb`), as a binary for macOS, Windows, and Linux, with `go install`, or as a container image. For Claude Code and the other supported clients, `tenable-docs-mcp config` prints ready-to-paste settings, including the `claude mcp add` command.
