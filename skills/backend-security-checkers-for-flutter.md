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
compatible_platforms: ["Claude Code", "Gemini CLI", "Codex"]
invocation: "/vibe-check"
---

Backend Security Checkers for Flutter is a skill for Claude Code, Gemini CLI, and Codex, backed by two dependency-light bash scripts, that externally verifies whether your Supabase and Firebase backends are properly secured — the same checks an outside attacker or security researcher would run using only your app's public keys.

## What it does

- Discovers your Supabase URL/anon key and Firebase project ID directly from your Flutter project (`.env`, `firebase_options.dart`, `google-services.json`) instead of making you paste them in — and is explicitly instructed never to read a `.env` file wholesale, since it may hold unrelated secrets.
- Infers which Supabase tables and Firebase Realtime Database paths are worth probing from your app's own code, rather than making you enumerate them.
- Runs `check_supabase_rls.sh` and `check_firebase_realtime_exposure.sh` — the two scripts that do the actual probing with only the public anon key / project ID — and reports whether Row Level Security or Firebase rules are actually blocking unauthorized reads.
- Interprets the raw results in context: explains what a given exposed table or path means for your specific app, prioritizes what to fix first, and generates remediation (RLS policies, Firebase rules) fitted to your real schema instead of generic examples.
- The two scripts also run standalone from the command line or in CI, independent of any assistant — the skill is an additional interactive layer on top, not a replacement.

## How it works

Invoke the skill with `/vibe-check` in a Claude Code, Gemini CLI, or Codex session inside your Flutter project, or just ask naturally (e.g. "check my backend for exposed tables"). The assistant discovers credentials and infers probe targets from your project's own code, then shells out to the two bash scripts exactly as documented: each sends unauthenticated (or anon-key-only) HTTP requests to the target and inspects the response — a 401/403 or empty result means the resource is protected, a 200 with real data means it's exposed. The assistant turns that raw pass/fail output into a prioritized, schema-aware report and can write the fix (an RLS migration, updated Firebase rules) directly.
