---
name: "Webapp Testing Checklist"
author: "AccessITGroup"
github_url: "https://github.com/AccessITGroup/webapp-testing-checklist"
description: "Structures an authorized web app pentest around the OWASP Web Security Testing Guide (WSTG) methodology as a checklist, and turns tester-supplied evidence into a WSTG-numbered findings report — backseat mode only, it never sends payloads or runs scanners."
license: "MIT"
tier: "contributed"
tags: ["pentest", "owasp", "wstg", "web-security", "security-testing", "checklist", "findings-report"]
integrations: ["Anthropic"]
date_added: 2026-09-03
contribution_agreement_date: 2026-09-03T18:16:27Z
works_with_tenable_hexa_mcp: false
compatible_platforms: ["Claude Code"]
invocation: "No fixed slash command — triggered by natural-language requests like \"run this through WSTG\" or \"OWASP testing guide checklist for this app\", or invoked directly by skill name (webapp-testing-checklist)"
---

For a human-led, already-authorized web application penetration test, this skill is the checklist
and report-writing layer, not the testing tool. It never touches Burp, ZAP, nmap, or any other
offensive tooling itself — the tester runs the actual security testing with their own tools, and
hands results back to the skill to track and write up.

## What it does

Walks all 12 OWASP WSTG categories (Information Gathering, Configuration & Deployment, Identity
Management, Authentication, Authorization, Session Management, Input Validation, Error Handling,
Weak Cryptography, Business Logic, Client-side, API Testing) as a structured checklist, one test
at a time, and produces a findings report with WSTG-numbered IDs (WSTG-AUTHZ-04, WSTG-INPV-02,
etc.) in Markdown, Word, and/or PDF.

It opens with a hard authorization gate — it won't walk a single test until the tester confirms
written authorization, the specific target/scope, the testing window, and how test credentials
will be supplied (via a local file, never pasted into the chat). Account creation in the target
app is a separate, stricter gate requiring explicit SOW confirmation plus real-time go-ahead at
the moment it's needed.

For each test, the tester either hands over a raw request/response capture (from Burp, ZAP, or
curl) plus any screenshot, or just states the verdict directly — either is fine, and the report
is explicit about which was used. The skill assesses evidence against that test's criteria; it
never crafts or sends an injection string, exploit attempt, or fuzzing input, and never runs an
automated scanner itself. If asked to "just try" something that requires attack traffic, it
redirects to the tester's own tooling instead of complying.

## How it works

`SKILL.md` encodes the workflow (authorization gate → scope intake → per-category checklist walk
→ report generation) and the guardrails; `references/` holds one file per WSTG category with the
test IDs, titles, and what each one verifies, cross-checked against the live WSTG source (not a
frozen PDF snapshot). Evidence handed off during a session is written to a local, git-ignored
`~/wstg-evidence/` directory — split into `pass-evidence/` and `fail-evidence/` subtrees, one
folder per WSTG ID, each holding the raw request/response transcript and any screenshots — so the
final report can cite exactly where its evidence lives instead of just asserting a verdict.

The generated report includes a coverage table (Pass/Fail/N/A/Not Tested counts per category) so
gaps are visible rather than buried, and an appendix with every test's result and evidence
pointer for audit purposes. An included eval suite (`evals/`) regression-tests the safety-critical
boundaries — the authorization gate, credential non-disclosure, refusal to send payloads or run
scanners, refusal to fabricate findings, and resistance to prompt injection via content fetched
from the target itself.
