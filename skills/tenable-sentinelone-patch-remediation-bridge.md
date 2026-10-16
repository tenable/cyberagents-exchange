---
name: "Tenable + SentinelOne Patch Remediation Bridge"
author: "jdelong-tenb"
github_url: "https://github.com/jdelong-tenb/tenable-sentinelone-patch-remediation-bridge"
description: "Bridges a Tenable-detected vulnerability to any third-party patch management tool's MCP server via a small, vendor-neutral contract, polls the resulting job to a pass/fail signal, and — only on an explicit pass, with confirmation — calls SentinelOne's REST API to release containment on the patched host."
license: "MIT"
tier: "contributed"
tags: ["patch-management", "remediation", "ctem", "vulnerability-management", "mcp-bridge", "sentinelone", "containment"]
integrations: ["Tenable", "SentinelOne"]
date_added: 2026-09-09
contribution_agreement_date: 2026-09-09T00:00:00Z
compatible_platforms: ["Claude Code"]
invocation: "Say things like \"trigger a patch job for this CVE,\" \"patch these hosts and tell me when it's done,\" \"did the patch job finish before we rescan,\" or \"release containment now that it's patched\" — the skill activates automatically."
last_reviewed: 2026-09-09
works_with_tenable_hexa_mcp: false
---

## What it does

A closed CTEM remediation loop — detect a vulnerability, contain the affected host, patch it, verify the fix, release containment — needs a "patch" step and a "release" step. There is no single standard patch-management API across vendors, so this skill defines a small, vendor-neutral MCP tool contract (`trigger_patch_job` / `get_patch_job_status`) for the patch step and orchestrates against whichever MCP server on the session actually implements it, rather than hardcoding to one patch-management vendor. On an explicit pass, and only with confirmation, it then calls SentinelOne's Management Console REST API directly to release containment on the patched host — completing the loop that the companion [`tenable-sentinelone-attack-path-interruption`](https://github.com/jdelong-tenb/tenable-sentinelone-attack-path-interruption) skill opened.

This is a community-built skill, not official guidance from Tenable or SentinelOne.

**Scope:** triggering and polling a patch job to a pass/fail signal, then releasing SentinelOne containment only on a confirmed pass. It does not detect vulnerabilities, does not itself contain hosts, and does not verify a patch actually applied beyond the TPM's own status reporting — those are the other legs of the loop it's designed to sit inside.

## How it works

Requires an MCP server, already connected to the session, that implements the skill's two-tool patch contract for your patch management tool (none is bundled), plus a SentinelOne Management Console API token/URL for the release step. When invoked, it:

1. Looks for `trigger_patch_job`/`get_patch_job_status` among the session's connected MCP tools, without assuming any specific TPM vendor.
2. Confirms the target assets and driving CVE/patch with the user before triggering anything.
3. Triggers the job, then polls it to a terminal status with exponential backoff and a timeout (`scripts/poll_patch_job.py`).
4. Reports a clean pass/fail signal — `complete` only counts as a pass; `failed`, timeout, or any status outside the known vocabulary all fail closed.
5. On a confirmed pass, and only with the user's confirmation, calls SentinelOne's `POST /web/api/v2.1/agents/actions/connect` directly (not through `purple-mcp`, which is read-only) to release containment (`scripts/reconnect_agent.py`, composed with the poll step in `scripts/patch_and_release.py`). A failed, timed-out, or unrecognized-status job never reaches this step.

Includes `scripts/poll_patch_job.py`/`scripts/reconnect_agent.py`/`scripts/patch_and_release.py` and matching test suites (`tests/test_*.py`), run against an in-memory fake TPM client and a mocked SentinelOne HTTP call respectively — no real TPM MCP server was available to test against while building this skill, and the SentinelOne reconnect endpoint has exactly one real-world verification (one tenant, one date); see the repository's Known Limitations for what that means in practice.
