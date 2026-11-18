---
last_reviewed: 2026-11-18
name: "Java4Shell Tenable Skill"
author: "securibee"
github_url: "https://github.com/securibee/java4shell-tenable-skill"
description: "Reports Java4Shell (CVE-2026-114938) exposure per Java install from Tenable data via Hexa AI MCP as HTML, PDF and CSV."
license: "MIT"
tier: "contributed"
tags: ["java4shell", "java", "openjdk", "cve-2026-114938", "exposure-report", "runtime-inventory"]
domains: ["vulnerability-management"]
integrations: ["Tenable", "Tenable Hexa AI MCP"]
date_added: 2026-11-18
contribution_agreement_date: 2026-11-18T21:09:00Z
works_with_tenable_hexa_mcp: true
cta: "T1"
compatible_platforms: ["Claude Code"]
invocation: "/java4shell-tenable"
---

Builds a Java4Shell exposure report from your own Tenable data. Every asset, install and finding in it comes from a Tenable Hexa AI MCP call made during the run. The output is an HTML page, a PDF and a CSV.

## What it does

- Checks that the Hexa AI MCP tools are loaded, and prints the setup command if they aren't.
- Re-reads the Tenable Research Java4Shell FAQ for the current Oracle fixed builds and mitigations, and asks Tenable's plugin database for every plugin covering the CVE.
- Finds every asset with an open Java detection finding and reads each install's path, version and vendor from the plugin output. It adds CPU, architecture and virtualization context, plus CVE findings and Java package findings from container and cloud scans.
- Gives each Java install a verdict: Impacted, Affected build – CPU unconfirmed, Unknown – verify, Mitigated (temporary) or Not impacted. An asset takes the worst verdict of its installs.
- Summarizes counts by verdict, the ten worst assets, every asset that needs action, coverage per detection plugin and the mitigations in chat.

It only reads data. It never launches scans, creates tags or changes anything in Tenable, and it never connects to your hosts.

## How it works

Java4Shell needs four things at once: an affected runtime, an x86-64 host, a CPU with AVX-512 VBMI, and the JVM's Base64 intrinsic turned on. Tenable data usually settles the runtime and the architecture. No Tenable plugin reports CPU instruction-set flags or live JVM flags yet, so installs on affected builds show as Affected build – CPU unconfirmed until one does.

The skill pulls findings with `tenable_one_search_findings`, reads plugin outputs with `workbenches_get_vulnerability_outputs` and reads each asset's name, IP and OS with `workbenches_get_asset_info`. Hexa returns at most 10 outputs per call, so the skill repeats detection calls across age windows from 7 to 365 days and merges the results by asset. When an output wasn't retrieved or was cut short, the asset is marked Unknown – verify so it can't come out Not impacted.

`findings.py` writes one row per asset and install to `findings.json`. `render.py`, a standard-library Python script, compares each version to the vendor's fixed build and writes the report. The PDF comes from a local headless Chrome, and neither script makes network calls. CVE findings are supporting evidence only. A CVE plugin can stop an asset from being cleared, but it never marks an asset exposed on its own.
