---
name: "Search the Exchange"
author: "securibee"
github_url: "https://github.com/securibee/search-the-exchange"
description: "Searches the CyberAgents Exchange catalog to answer whether a listing for your job-to-be-done already exists, returning a coverage verdict with linked matches."
license: "MIT"
tier: "contributed"
tags: ["cyberagents-exchange", "catalog-search", "coverage-verdict", "tool-discovery", "reuse-before-build"]
integrations: []
date_added: 2026-08-31
contribution_agreement_date: 2026-08-31T15:04:57Z
compatible_platforms: ["Claude Code", "Codex", "Cursor", "Cline", "Gemini CLI", "Windsurf"]
invocation: "/search-the-exchange"
---

Answers one question: does the CyberAgents Exchange already have something for this? So you can
use what's already been built instead of starting from scratch. Say what you want in whatever
words you have — it infers the job, searches the full catalog (~100 listings), and returns a
coverage verdict with the closest listings linked.

## What it does

- Reads your request as a job shape (input → procedure → output), inferred from plain speech
  rather than an interview. A bare noun is searched as a broad query, not bounced back.
- Strips identifiers from the query before anything leaves the machine.
- Assigns one verdict per matched listing — **covered**, **partial**, **adjacent**, or **none** —
  matching on the job rather than shared vocabulary.
- Reports a table of matches ordered covered → partial → adjacent, every listing linked to its
  page on exchange.tenable.com, plus a one-line next step. A **none** verdict still shows the
  nearest listings and why each fell short, and names the official submission path.

## How it works

Shallow-clones `tenable/cyberagents-exchange` and builds a local index with `tools/build-index.py`
in about a second, recording the catalog revision it read (the tarball works when `git` is
missing). It reads the index of all listings whole — the whole catalog is considered,
nothing is sampled — then reads the full body of only the shortlisted candidates. 
The index is built per run and never mirrored, so there is no stale copy to
serve. Requires a shell with `git` (or `curl`) and `python3`; no authentication.

Known limitations and the exact privacy boundary (one identifier-stripped description leaves the
machine, nothing else) are documented in the repository README.
