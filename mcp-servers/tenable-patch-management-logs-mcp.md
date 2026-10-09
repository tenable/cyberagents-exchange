---
last_reviewed: 2026-10-05
name: "Tenable Patch Management Logs MCP"
author: "brendanong95"
github_url: "https://github.com/brendanong95/tenable-patch-management-logs-mcp"
description: "Answers 'why did patching fail?' from Tenable Patch Management SaaS logs — a server bundle and client logs become ranked issues, symptom verdicts and anomaly findings computed in Python, with no credentials and no network access."
license: "MIT"
tier: "contributed"
tags: ["patch-management", "log-analysis", "troubleshooting", "root-cause-analysis", "anomaly-detection", "offline"]
domains: ["platform-operations", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-10-02
contribution_agreement_date: 2026-10-02T03:56:13Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop"]
transport: "stdio"
runtime: "python"
auth_method: "none"
tools_exposed:
  - name: "check_log_sources"
    description: "First call: which logs are readable, the devices and roles inside them, the period each one covers, TPM versions with version advisories, files whose format was not recognised, and a flag on anything that does not look like a SaaS tenant's logs."
  - name: "summarize_errors"
    description: "Every warning and error in a window grouped into distinct issues and ranked: counts, first and last seen, affected devices, decoded error codes, root causes from stack traces, the latest example with file and line, and a fix where the signature is recognised."
  - name: "diagnose"
    description: "Runs one of ten symptom playbooks (patch install failures, content download, client connectivity, Tenable VM integration, feeds, content publication, service health, database, client upgrade, feature-update readiness) and returns a verdict with the evidence behind it."
  - name: "search_logs"
    description: "Literal or regex search across every log, matching whole entries including multi-line messages and stack traces, de-duplicated, with context lines and paging."
  - name: "build_timeline"
    description: "Merges server and client logs into one chronological sequence around a moment or across a window, with consecutive repeats collapsed and WARN-and-above always kept when rows are sampled."
  - name: "compare_devices"
    description: "What a failing device has in its logs that a healthy one does not, plus the signatures that are merely far more frequent on the failing one."
  - name: "detect_log_anomalies"
    description: "Compares a recent window with the days before it: error signatures that are new, error rates above the spike threshold, repeated service starts and logs that went quiet, each with evidence, the threshold crossed and a reasoning sentence."
  - name: "record_baseline_snapshot"
    description: "Writes the current per-day error counts to a local SQLite file so anomaly detection keeps a baseline after TPM rotates the logs away. The only tool that writes anything."
  - name: "list_log_files"
    description: "Every log file with its device, role, documented purpose, size and the period it covers, counted by device, role and log name."
  - name: "explain"
    description: "What a given log file records, what an error code means (Win32, MSI, HRESULT, Windows Update, CBS, HTTP), or what a symptom or known issue covers."
  - name: "add_log_source"
    description: "Registers a folder, UNC path, single log file or .zip/.tar.gz bundle to analyse, with an optional time zone for the machine that wrote it; remembered between sessions."
  - name: "remove_log_source"
    description: "Unregisters a source and deletes the server's extracted copy of a bundle, leaving the original untouched."
resources_exposed: []
prompts_exposed: []
---
last_reviewed: 2026-10-05

## What it does

> The reason the patch failed is in the logs. It is on line 48,112 of one of
> forty-two files, written at INFO, and the real cause is six lines further down
> in a Java stack trace.

Tenable Patch Management runs on the Adaptiva platform, and when a deployment goes
wrong the answer lives in its logs: a server bundle from the Admin Portal (forty-odd
files, including component and workflow logs) plus whatever the devices wrote. The
usual approach is to open `adaptiva.log`, search for "error", and scroll. The
failures that matter are rarely where you look — the documented Services-sensor bug
is written at **INFO** with an exception attached, and roughly two thirds of the
warnings in a real bundle are platform noise that recurs every few minutes.

This server does the reading. Tools return finished answers rather than excerpts for
the model to total up: `summarize_errors` returns ranked issues with counts, decoded
exit codes, root causes and the latest example quoted with its file and line;
`diagnose` runs a symptom playbook and returns a verdict. In the tenant it was built
against, one call surfaced that the Tenable VM integration had been failing for days
— API keys rejected as "not related to any active containers" — while the import
runs themselves were logging "completed successfully" and importing nothing.

It needs **no credentials and no network access**: TPM has no documented public API,
so everything comes from log files you already have. That also makes it safe to point
at a customer's bundle on a laptop.

## How it works

Parsing was derived from real 10.2.973.9 logs rather than documentation, which turned
out to matter: the documented rotation and workflow-log naming were wrong. Six layouts
are recognised — the Java service format used by every server and client log, workflow
logs, the `SQLUploader` block format, UTF-16 msiexec logs, generic timestamped lines,
and a plain fallback so an unrecognised file can never collapse into one entry. Rotated
and gzipped files read as one log, multi-line messages keep their stack traces attached,
and anything whose layout was not recognised is named in the result instead of being
quietly mis-parsed.

On top of that:

- **De-duplication.** TPM writes the same event to `adaptiva.log`, a component log and
  `adaptiva.err`. Events are matched across files and counted once, and the number of
  removed repeats is reported.
- **Severity correction.** Entries carrying a stack trace or a non-zero internal error
  code are raised to ERROR and flagged, because real failures are logged at INFO.
- **A knowledge base with honest confidence.** Each recognised signature is marked
  `documented` (described by Tenable or Adaptiva, with the link), `observed` (seen in
  real logs, explained from the surrounding lines) or `generic` (a standard Java,
  Windows, SQL or network error). Signatures whose impact is "none" are platform noise:
  counted and reported separately, never mixed into the issue list.
- **Error-code decoding** from context — MSI and Win32 exit codes, HRESULTs including
  `HRESULT_FROM_WIN32`, Windows Update and servicing codes, HTTP statuses — while the
  platform's own `Error Code = N` values are shown but never decoded as Windows errors.
- **Thresholds you can argue with.** Every anomaly threshold is a named constant and is
  echoed back in the result, and findings are marked low-confidence when the logs do not
  reach far enough back to support them.
- **Three things that make mixed evidence usable:** logs from machines in different
  zones are converted into one display zone once each is declared; relative windows say
  what they counted back from and name any device whose logs end well before that; and
  `record_baseline_snapshot` keeps daily counts in SQLite so a baseline survives log
  rotation.
- **A site knowledge file.** Your own recurring signatures, the noise you have already
  decided to ignore, and the undocumented `PatchDeploymentResult` values your console
  shows can be added as JSON or YAML — matched ahead of the built-in catalog, with
  rejected entries reported rather than dropped.

Nothing that looks like credential material leaves the server: TPM writes the Tenable VM
access key into its logs in plain text, so key-shaped values, labelled secrets, bearer
tokens and URL passwords are masked to their last four characters, and the offline test
suite plants fake secrets and asserts they never surface. Reads are capped at 1 GB and
5,000 files per call, newest first, and whatever was not read is listed with how to
narrow the call — a wide question degrades into a stated partial answer, not a silent one.

Python 3.11+ and [uv](https://docs.astral.sh/uv/); 234 tests and an offline end-to-end
run exercise every tool against synthetic logs in the real formats, so nothing in the
repository contains customer log content.

## Known limitations

- **Tenable Patch Management SaaS only.** Self-hosted Adaptiva OneSite servers are out
  of scope; a source whose logs name a SQL Server database is reported as unsupported
  rather than analysed as a tenant.
- Formats were validated against 10.2.973.9 server logs and a Windows client
  `adaptiva.log`. Linux and macOS clients use the same logging and are expected to
  match, but have not been checked against real samples.
- Client component logs were not in the samples, so the patch-failure playbook leans on
  exit codes, HRESULTs and exceptions rather than exact message wording. Site-specific
  wording belongs in the knowledge file.
- `PatchDeploymentResult` status and reason values are undocumented. They are shown as
  logged, with failure evidence taken from non-zero reason codes and exceptions, until
  you map the values your console shows.
- Time zones have to be declared: TPM writes local timestamps with no zone, so anything
  undeclared is shown as written and named in the results rather than guessed at.
- Recorded baselines start when you start recording, at day granularity, so a burst
  inside one day is judged against that whole day.
- Signatures marked `observed` come from one tenant's logs; confirm fixes against current
  Tenable documentation before acting on them.
