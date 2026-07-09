---
name: "TIE IoA Investigator"
author: "knethteo"
github_url: "https://github.com/knethteo/tie-ioa-investigator-ai-skill"
description: "Triages Tenable Identity Exposure IoA alerts as false positive, true positive, or false negative with a 1–10 confidence score."
license: "MIT"
tier: "unreviewed"
tags: ["identity-exposure", "ioa", "false-positive", "active-directory", "triage", "kerberos", "dcsync"]
integrations: ["Tenable"]
date_added: 2026-06-22
compatible_platforms: ["Claude Code"]
invocation: "/tie-ioa-investigation"
---

A Claude Code skill that triages Tenable Identity Exposure (TIE) Indicators of Attack (IoA) alerts, determining whether each is a false positive, true positive, or false negative with a 1–10 confidence score. Produces a structured Markdown investigation report with verdict, supporting signals, investigation steps, and whitelist recommendations.

## What it does

- Parses TIE IoA CSV exports (comma or semicolon delimited, UTF-8 BOM safe) or accepts pasted incident descriptions from the TIE console
- Limits analysis to the latest 20 alerts and groups duplicate attack patterns into distinct incidents
- Maps each incident to its IoA type across 16 supported attack categories (DCSync, Golden Ticket, NTDS Extraction, Kerberoasting, and more)
- Cross-references the Tenable Identity Exposure IoA Reference Guide (user-supplied MD or PDF) and live Tenable documentation
- Outputs a repeatable Markdown report per investigation with per-incident verdict, confidence score, numbered signals, investigation steps, and recommended whitelist actions

## How it works

On first use the skill prompts for the Tenable Identity Exposure — Indicators of Attack Reference Guide (available at https://www.tenable.com/downloads/identity-exposure#documentation). A bundled Python script (`build_ioa_index.py`) parses the guide — MD or PDF — and writes a section index mapping each IoA to its line number and common false-positive sources. For each alert, the skill reads the relevant Options table from the guide (whitelist controls, aggressive mode, defer time), weighs the observed source, account, and destination against known legitimate patterns, and assigns a verdict and confidence score using a defined rubric. A second script (`parse_ioa_csv.py`) handles CSV normalisation and deduplication before analysis begins.
