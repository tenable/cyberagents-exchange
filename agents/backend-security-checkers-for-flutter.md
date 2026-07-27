---
name: "Backend Security Checkers for Flutter"
author: "digitalonyx"
github_url: "https://github.com/digitalonyx/vibe-check"
description: "Externally verify Supabase RLS and Firebase Realtime Database security in Flutter apps."
license: "MIT"
tier: "contributed"
tags: ["supabase", "firebase", "flutter", "security", "row-level-security"]
integrations: ["Firebase", "Supabase"]
date_added: 2026-07-27
contribution_agreement_date: 2026-07-27T18:49:27Z
---

Backend Security Checkers for Flutter is a pair of dependency-light bash scripts that externally verify whether your Supabase and Firebase backends are properly secured — the same checks an outside attacker or security researcher would run using only your app's public keys.

## What it does

- `check_supabase_rls.sh` probes one or more Supabase tables using only the public anon key and reports whether Row Level Security is actually blocking unauthorized reads.
- `check_firebase_realtime_exposure.sh` checks whether a Firebase Realtime Database (or a specific path within it) is publicly readable due to permissive `.read`/`.write` rules.

Both scripts are designed to be run before shipping a Flutter release, or wired into CI, so misconfigurations are caught before they become an incident.

## How it works

Each script sends unauthenticated (or anon-key-only) HTTP requests to the target backend and inspects the response: an HTTP 401/403 or empty result indicates the resource is protected, while a 200 response with real data indicates the table or path is exposed. Output is color-coded (green = protected, red = exposed) and includes concrete remediation steps, such as the exact `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` statement to run.
