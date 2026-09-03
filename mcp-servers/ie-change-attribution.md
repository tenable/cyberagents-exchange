---
last_reviewed: 2026-09-03
name: "Tenable IE Change Attribution"
author: "hatumus"
github_url: "https://github.com/hatumus/tenable-ie-change-attribution"
description: "Names the actor behind Tenable IE's Active Directory findings by correlating them with DC Security logs, via MCP."
license: "MIT"
tier: "contributed"
tags: ["active-directory", "identity-exposure", "incident-response", "threat-hunting", "attribution", "windows-event-log", "mcp"]
integrations: ["Tenable"]
date_added: 2026-09-02
contribution_agreement_date: 2026-09-02T09:32:40Z
transport: "stdio"
runtime: "python"
auth_method: "api-key"
compatible_clients: ["Claude Code", "Claude Desktop"]
tools_exposed:
  - name: "who_caused_deviances"
    description: "Pull Tenable IE deviances (IoE security findings) and attribute each to the actor in the DC Security log."
  - name: "attribute_ie_window"
    description: "Pull IE Trail Flow changes in a time range and attribute each to the DC actor who made them, paginating past the API's 500-event page cap."
  - name: "attribute_change"
    description: "Attribute a single AD change (by DN / objectSid / objectGUID / sAMAccountName + timestamp) to its actor."
  - name: "attribute_trailflow_event"
    description: "Attribute a single Trail Flow event by its numeric event id to the DC-log actor who made it."
  - name: "query_dc_log"
    description: "Query the DC Security event log directly over WinRM, bypassing Tenable IE, for ad-hoc investigation."
resources_exposed: []
prompts_exposed: []
---

Tenable Identity Exposure detects Active Directory changes but doesn't know who made them — deviances derive from AD replication metadata, which carries no actor identity. This MCP server closes that gap by correlating IE deviances and Trail Flow events with the Domain Controller's Security event log, matching on object identity (objectSid/objectGUID > DN > sAMAccountName) within a time window, and returning the actor with a confidence score.

## What it does

- Attributes IE deviances (IoE findings) and Trail Flow events to the DC-log actor who caused them
- Scores confidence as high / medium / low / ambiguous / none — a `none` rate surfaces DC audit-coverage gaps rather than claiming "no actor"
- Queries the DC Security log directly, bypassing IE, for ad-hoc investigation
- Runs agentless: reads the DC remotely over WinRM or SSH, nothing installed on the DC
- Ships as a dependency-free MCP server that implements the JSON-RPC handshake directly, with no FastMCP or pydantic dependency required

## How it works

It pulls changes from Tenable IE's REST v3 API (deviances endpoint and `/api/events/search` for Trail Flow), then joins each one against the Windows Security event log entries that carry `SubjectUserName`/`SubjectUserSid` (event IDs such as 4720/4728/4732/5136), reporting the best-matching actor and supporting evidence. A CLI mode also supports offline verification against exported IE data, with no live DC or IE connection required.
