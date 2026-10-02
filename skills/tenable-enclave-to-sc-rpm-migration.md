---
name: "Tenable.sc RHEL Migration and Recovery Skill"
author: "conard0-git"
github_url: "https://github.com/conard0-git/tenable-enclave-to-sc-rpm-migration"
description: "Migrate Tenable Enclave Security / Tenable.sc to standalone RHEL 8 with external PostgreSQL, preserving data and runtime."
license: "MIT"
tier: "contributed"
tags: [tenable, tenable-sc, security-center, migration, rhel, postgresql, aws-rds]
domains: [platform-operations, vulnerability-management]
integrations: [Tenable, AWS]
date_added: 2026-10-02
contribution_agreement_date: 2026-10-02T20:00:00Z
compatible_platforms: [Claude Code]
invocation: "/tenable-enclave-to-sc-rpm-migration"
---

A guided runbook for migrating or recovering Tenable Enclave Security / Tenable Security Center data onto a standalone RHEL 8 Tenable.sc host backed by external PostgreSQL (for example AWS RDS). Distilled from a real recovery after a container-to-RPM migration broke the fresh runtime.

## What it does

Walks an operator through, in order: establishing rollback points (RDS snapshot, preserved failed `/opt/sc`, stopped-service tar backup); building a clean RPM runtime and proving it starts against the external database before touching data; selectively `rsync`-ing persistent data from the old tree while preserving the fresh host's `.pgvars` and `data/enc.key`; and troubleshooting the usual follow-on failures — `fapolicyd` blocking PHP, PHP `memory_limit` exhaustion during feed updates, and `/opt/sc` growing from leftover feed directories. Includes an upgrade preparation checklist and a diagnostic decision tree.

## How it works

The skill treats the external PostgreSQL database as authoritative application state and the RPM `/opt/sc` tree as replaceable runtime. Instead of overwriting the fresh RHEL runtime with a container `/opt/sc` tree (which carries different PHP/library binaries and causes silent startup failures), it rebuilds a clean RPM install against the preserved database, then overlays only persistent data directories (`orgs`, `repositories`, parts of `data`) with an explicit `rsync` exclude list. Each phase is gated by validation — connectivity, service start, feed/job processing — before the next destructive step runs.
