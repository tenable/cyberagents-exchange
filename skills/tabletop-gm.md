---
name: "Tabletop GM"
author: "eshin087"
github_url: "https://github.com/eshin087/tabletop-gm"
description: "AI facilitator that runs a tailored incident response tabletop from your exposure data and scores it the same day"
license: "MIT"
tier: "contributed"
tags: ["tabletop", "incident-response", "exercise", "after-action-report", "industry-packs", "policy-testing", "claude-code"]
domains: ["security-operations", "governance-risk-compliance"]
integrations: ["Tenable", "Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T17:27:11Z
compatible_platforms: ["Claude Code"]
invocation: "/tabletop"
---

Tabletop GM runs an incident response exercise for a leadership team the way a good facilitator would. The host puts the Claude Code chat on the projector, Claude presents each inject, reacts to what the room decides, plays the CEO, the regulator, and the press when the room stalls, and logs every decision as it happens. When the host types END, the room gets a scored after-action report and an executive summary in minutes. The scenario is not a template: it is built from the organization's exposure data (Tenable Vulnerability Management or Tenable One exports, a scan export, or a synthetic sample estate), its industry's notification deadlines, and its own written incident response plan.

## What it does

- **Builds a tailored exercise.** A short clickable intake picks the industry pack, length (30, 60, or 90 minutes), severity, data held, and regulated status. The engine selects the entry point (CISA KEV first, then highest Tenable VPR), the pivot, and the crown jewel from the exposure data and records the rule that fired for each. Every inject cites a finding ID or a labeled assumption.
- **Tests the organization's own plan.** Uploaded IR plans and playbooks are extracted with section anchors. Each inject names the procedure it tests and quotes it verbatim; a validator rejects any quote that does not exist in the source.
- **Applies real notification deadlines.** Ten industry packs (healthcare, banking, insurance, public sector, higher education, SaaS, retail, manufacturing and OT, energy and utilities, federal contractors) plus common clocks such as GDPR, SEC 8-K, CIRCIA, and state breach laws. Every clock carries a source URL, a checked date, and a verification tier, and researched-tier clocks are flagged on every output.
- **Facilitates live in chat.** Claude presents injects in pack order through the question UI, with Pause, Skip, and End as one-click options, asks at most two follow-ups per inject from the pack's probing questions, speaks short labeled stakeholder lines when the room stalls, and never reveals what is coming. Each decision becomes one append-only, engine-timestamped log entry.
- **Or builds the room documents.** A projector deck, a facilitator guide, a participant handout, a dropdown-only decision tracker, and attendance and sign-off sheets, all generated from the approved exercise pack.
- **Scores and reports.** One command scores the live log or the filled tracker on five dimensions against the plan's own commitments, then writes a two-page after-action report with lessons learned, a plan coverage map, every gap with its citation and an evidence page, and a seven-slide executive summary with a one-page memo.

## How it works

Deterministic engine first, agent on top. A pure-Python command-line engine (`ttx`) computes every fact that has to be right: the attack path, the deadlines, the citations, the validation, the documents, the timestamps, and the scores. Claude, running the `/tabletop` skill in Claude Code, does only the judgment and the conversation: the intake interview, mapping the plan to procedures, writing and adversarially reviewing the narrative, facilitating the room, and explaining the result. Validators check that the model stayed inside those bounds, and a named human must approve the outline before anything runs or builds; the approval hash is recorded on every output.

The engine is read-only against Tenable (export endpoints only, read-only API keys are enough) and makes one optional unauthenticated request to the CISA KEV feed. Every outbound call is documented in the repository's SECURITY.md. No secrets, uploaded policies, or real company data enter the repository; the committed sample run is synthetic and can be rebuilt with no API key and no model call. Dependencies are pure Python (python-pptx, python-docx, openpyxl, pyyaml, pypdf, jinja2); there is no Docker, database, or cloud service. 132 automated tests cover the engine, validators, document builders, scoring, launcher, and live decision log.
