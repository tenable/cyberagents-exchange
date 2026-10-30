---
name: "AuthRecon Suite"
author: "AuthRecon"
github_url: "https://github.com/AuthRecon/AuthRecon"
description: "Works out how a web app's login works and hands back a verified Selenium .side login script for Tenable WAS scans."
license: "Apache-2.0"
tier: "contributed"
tags: ["tenable-was", "authenticated-scanning", "dast", "selenium", "login-automation", "self-hosted", "mcp"]
domains: ["application-security"]
integrations: ["Tenable"]
date_added: 2026-10-26
contribution_agreement_date: 2026-10-26T14:14:37Z
---

AuthRecon is a self-hosted Docker stack for the hardest part of authenticated web app scanning: getting the scanner logged in. Give it a login URL and a test account. It works out what kind of login the app uses, logs in the way a scanner would, and hands back a verified Selenium `.side` script plus the exact values to paste into a Tenable Web App Scanning (WAS) scan's Selenium authentication settings. Everything runs locally with no cloud services.

## What it does

- **Detects the login type and automates it:** form logins (including JavaScript-rendered pages), two-step username-then-password, HTTP Basic, and dedicated handlers for Azure AD, Okta, SAML/ADFS, LDAP-style forms and OAuth/OIDC redirects. Kerberos/NTLM and Digest are detected and explained rather than scripted.
- **Tenable WAS setup card:** after a successful run you get the login page, page to verify, regex pattern to verify and a downloadable `.side` file.
- **One-click Verify:** replays the `.side` script in a clean browser the same way WAS does, so you know it works before the scan starts.
- **Scan readiness:** grades how well the login will hold up in a scan (cookie-only session survival, session lifetime, WAF and rate limits) and suggests starting settings such as URLs to exclude and the session cookie.
- **Scan Analyzer (preview):** upload a WAS scan's debug zip or JSON export after a failed or thin scan to see what went wrong (logged out, timeouts, WAF, skipped URLs) and which settings to change. Rule-based, no AI required.
- **Troubleshooting artifacts:** a timeline, step-by-step screenshots, HAR capture, and cookie and security-header findings for logins that won't automate. There's also multi-role runs and manual recording through a live noVNC browser for flows you have to drive by hand.
- **Exports:** HAR, curl, Postman, Burp and ZAP from the captured session.
- **Optional AI via MCP:** connect your own MCP client (for example Claude Code or Claude Desktop) with a per-user API key to launch runs from stored credentials, read timelines, fetch WAS settings, trigger Verify and suggest selectors for stuck form logins. The client never receives passwords or `.side` contents, and an admin has to turn MCP on.
- **LoginLab:** optional built-in practice targets covering each supported login style. Off by default and bound to loopback.

## How it works

A React UI talks to a FastAPI portal that handles sign-in (with optional TOTP MFA and HttpOnly session cookies) and per-user checks. The AuthRecon API queues each run on Redis, and a worker drives a real Chromium with Playwright or Selenium against the target. It records the timeline, screenshots, HAR and `.side` script, encrypted at rest in PostgreSQL and an artifacts volume. Stored credentials are bound to the domains they may be used on, so the worker never types a password on an unexpected site. Targets are checked so a run can't reach cloud metadata or AuthRecon's own services. With browser isolation turned on, the browsers run in a separate container with no secrets and no database access.

Install with `git clone` and `./install.sh`, which generates unique secrets, builds the stack and checks its health. It runs on Linux and on macOS with Docker Desktop, and supports corporate TLS inspection and private package mirrors. Intended for authorized testing only.
