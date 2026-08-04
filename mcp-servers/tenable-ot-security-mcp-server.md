---
name: "Tenable OT Security MCP Server"
author: "aqamahn"
github_url: "https://github.com/aqamahn/MCP-server-Tenable-OT-V2"
description: "Tenable OT Security asset, vulnerability, event and policy tools, with an opt-in dry-run-by-default write layer."
license: "Apache-2.0"
tier: "contributed"
tags: ["mcp-server", "ot-security", "ics", "scada", "asset-inventory", "vulnerability-management", "audit-logging"]
integrations: ["Tenable"]
date_added: 2026-08-01
contribution_agreement_date: 2026-08-01T11:27:24Z
last_reviewed: 2026-08-04
transport: "both"
runtime: "python"
auth_method: "api-key"
compatible_clients: ["Claude Desktop", "Claude Code"]
tools_exposed:
  - name: "tenable_ot_status"
    description: "Check Tenable OT connectivity"
  - name: "query_assets"
    description: "Query OT assets"
  - name: "get_asset"
    description: "Get one OT asset"
  - name: "get_asset_vulnerabilities"
    description: "Get vulnerabilities for one asset"
  - name: "list_custom_fields"
    description: "List configured custom fields"
  - name: "get_manual_asset_upload_status"
    description: "Get manual asset-upload processing status"
  - name: "query_attack_pathways"
    description: "Query attack-pathway data (relational, not computed)"
  - name: "query_vulnerability_clusters"
    description: "Query vulnerability clusters (relational join, not computed)"
  - name: "query_temporal_patterns"
    description: "Query temporal patterns (event sequence, not motif analysis)"
  - name: "get_asset_intelligence"
    description: "Get asset intelligence bundle (joined data, not narrative)"
  - name: "query_events"
    description: "Query OT events"
  - name: "get_event"
    description: "Get one OT event"
  - name: "export_assets"
    description: "Bulk export assets"
  - name: "export_plugin_definitions"
    description: "Bulk export plugin definitions"
  - name: "export_findings"
    description: "Bulk export findings"
  - name: "query_plugin_definitions"
    description: "Query plugin (vulnerability) definitions"
  - name: "get_plugin_definition"
    description: "Get one plugin definition"
  - name: "list_detection_policies"
    description: "List detection policies"
  - name: "get_policy"
    description: "Get one policy's full configuration"
  - name: "query_policy_findings"
    description: "Query policy findings"
  - name: "get_schema_enums"
    description: "Introspect the Tenable OT GraphQL schema"
  - name: "list_sensors"
    description: "List sensors"
  - name: "summarize_environment"
    description: "Summarize the OT environment"
  - name: "list_segments_and_zones"
    description: "List network segments and zones"
  - name: "get_communication_paths"
    description: "Get communication paths for an asset"
  - name: "query_vulnerabilities"
    description: "Query OT vulnerabilities"
  - name: "get_vulnerability"
    description: "Get one vulnerability"
  - name: "list_asset_groups"
    description: "List asset groups (active)"
  - name: "list_archived_asset_groups"
    description: "List archived asset groups"
  - name: "get_asset_group"
    description: "Get an asset group by id"
  - name: "list_email_groups"
    description: "List email groups"
  - name: "get_email_group"
    description: "Get an email group by id"
  - name: "find_email_groups_using_smtp_server"
    description: "Find email groups that route through a given SMTP server"
  - name: "list_schedule_groups"
    description: "List schedule groups"
  - name: "list_archived_schedule_groups"
    description: "List archived schedule groups"
  - name: "get_schedule_group"
    description: "Get a schedule group by id"
  - name: "list_tag_groups"
    description: "List tag groups"
  - name: "get_tag_group"
    description: "Get a tag group by id"
  - name: "list_eligible_tags"
    description: "Discover tags eligible for a tag group"
  - name: "list_rule_groups"
    description: "List rule groups"
  - name: "list_archived_rule_groups"
    description: "List archived rule groups"
  - name: "get_rule_group"
    description: "Get a rule group by id"
  - name: "list_port_groups"
    description: "List port groups"
  - name: "list_archived_port_groups"
    description: "List archived port groups"
  - name: "get_port_group"
    description: "Get a port group by id"
  - name: "list_protocol_groups"
    description: "List protocol groups"
  - name: "list_archived_protocol_groups"
    description: "List archived protocol groups"
  - name: "get_protocol_group"
    description: "Get a protocol group by id"
  - name: "list_user_groups"
    description: "List user groups (ICP-level)"
  - name: "list_archived_user_groups"
    description: "List archived user groups (ICP-level)"
  - name: "get_user_group"
    description: "Get a user group by id (ICP-level)"
  - name: "list_em_user_groups"
    description: "List user groups (Enterprise Manager level)"
  - name: "list_em_archived_user_groups"
    description: "List archived user groups (Enterprise Manager level)"
  - name: "get_em_user_group"
    description: "Get a user group by id (Enterprise Manager level)"
  - name: "list_active_scans"
    description: "List active scans"
  - name: "get_active_scan"
    description: "Get one active scan"
  - name: "get_active_scan_executions"
    description: "Get past executions of an active scan"
  - name: "list_network_config"
    description: "Read what the appliance is configured to monitor"
  - name: "list_policy_relationships"
    description: "Check what references an object before changing it"
resources_exposed: []
prompts_exposed: []
---

An MCP server that connects any MCP client — Claude Desktop, Claude Code, or
another — to a Tenable OT Security deployment, exposing OT/ICS asset inventory,
vulnerabilities, events, detection policies and policy findings as read tools,
plus an opt-in write layer for asset edits, group and policy management, scan
definitions and finding resolution.

Because this server talks to industrial control systems, its safety model is
structural rather than advisory: writes are invisible until explicitly enabled,
every write previews before it acts, destructive operations need a second
confirm flag, and every write attempt is recorded to an append-only audit log.

> Not an official Tenable product. Copyright (c) 2026 Tenable, Inc., released
> under Apache 2.0, but shipped with no SLA, no warranty and no support
> commitment, and not covered by Tenable's product security or
> vulnerability-disclosure processes.

## What it does

**59 read tools, always available.** Asset inventory with identity, IPs/MACs,
Purdue level, segment and backplane membership and aggregate risk; fleet-wide
and per-asset vulnerability search with CVE, CVSS and exploit/KEV flags; OT
events; detection policies and their per-asset findings; the plugin
(vulnerability) definition catalog; and bulk exports of assets, findings and
plugin definitions via pyTenable.

Beyond raw inventory it covers the environment's shape and its dependencies:
network segments and zones as observed, per-asset communication paths, sensor
inventory, and `list_network_config` — what the appliance is *configured* to
watch, which flags disabled subnets as monitoring blind spots and is the usual
answer to "why is this asset missing". `list_policy_relationships` answers
"what breaks if I change this?" before a write lands, which matters because
Tenable OT's policy mutations are full replaces, not patches.
`summarize_environment` gives a one-call orientation on an unfamiliar
deployment, and `get_schema_enums` introspects the appliance's own GraphQL
schema.

**71 write tools, only when `TENABLE_OT_WRITE_TOOLS_ENABLED=1`.** Asset
lifecycle (hide/restore, bulk variants, removal by address, merge, risk
recalculation, manual file upload), asset properties and custom-field schema,
detection policy enable/disable/archive and full policy editing, finding
resolution, group management across asset / email / schedule / tag / rule /
port / protocol / user groups, sensor management, and scan *definition*
create/edit.

Nothing in the codebase runs a scan. There is no run, start, or execute
mutation anywhere in it — definitions can be written, and `enable_active_scan`
sets whether a definition participates in runs, but only a human starting a
scan from the Tenable OT UI ever launches one against live equipment.

## How it works

A Python 3.12+ server on the MCP SDK, wrapping Tenable OT's GraphQL API
directly with `httpx` for everything Tenable doesn't officially cover, and
bridging to pyTenable for the bulk-export surface. Most paginated read tools
are declared as data — a `ConnectionSpec` record naming a query and a field
projection — and one registrar turns specs into tools, so the pagination and
projection plumbing exists and is tested once rather than being re-implemented
per tool. Composite tools that fan out or join across queries stay
hand-written. Queries whose availability varies by appliance are marked
unconfirmed and return an actionable `error` envelope naming what to
introspect, instead of raising.

The four safety properties are enforced in the architecture, not by
convention:

1. **Write tools are absent, not merely refused.** Without the opt-in
   environment variable the write modules are never imported, so no write tool
   name appears in the MCP `tools/list` response. A client cannot call — or
   discover — an operation that wasn't enabled.
2. **Every write defaults to `dry_run=True`,** returning the exact payload that
   *would* be sent without sending it, so the operator approves a concrete
   preview before anything changes.
3. **Destructive operations require a second explicit flag.** `dry_run=false`
   alone is insufficient; `delete_custom_field`, for instance, is rejected
   without `confirm_wipes_values=True`.
4. **Every write call is audited** — dry-run, live, or failed — as one JSON
   line recording timestamp, tool, parameters, dry-run flag, outcome and error.
   The audit writer fails closed: if it cannot record, the call raises rather
   than proceeding silently.

Credentials come from the environment only. The API key is read from
`TOT_API_KEY`, held privately by the client, and is never logged, never written
to disk by the server, and never included in an audit entry; uploaded file
contents are never audited either, only filename and byte size.

Ships with a Dockerfile and compose file. The container entrypoint fixes
bind-mount ownership for the audit directory and proves the target uid can
actually write there before permanently dropping from root via `setpriv` — a
failure mode that otherwise surfaces late, only on the first write. The test
suite runs entirely against a mocked client with no network, appliance or
credentials, covering dry-run paths, live paths, audit-entry assertions and
confirm-flag rejection paths.
