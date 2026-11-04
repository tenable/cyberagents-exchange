---
last_reviewed: 2026-11-04
name: "ScreenWarden"
author: "the-cyberlayer"
github_url: "https://github.com/the-cyberlayer/screenwarden"
description: "Guarded Android phone control for AI agents: cleans what the agent sees and blocks hijacked actions such as OTP forwarding."
license: "MIT"
tier: "contributed"
tags: ["android", "mobile-agents", "prompt-injection", "guardrail", "owasp-agentic", "adb", "otp", "phishing"]
domains: ["ai-security", "data-security"]
integrations: ["Anthropic"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-03T17:12:44Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor"]
tools_exposed:
  - name: "start_task"
    description: "Sets the user's goal; locked once the first screen is read, so on-screen text cannot change it"
  - name: "read_screen"
    description: "Returns the current screen with hidden and instruction-like text removed and outside text marked as data"
  - name: "tap"
    description: "Taps an element after checking the action against the goal"
  - name: "type_text"
    description: "Types into a field; refuses credential entry on spoofed pages and codes leaving the device"
  - name: "send_sms"
    description: "Sends an SMS only to recipients named by the user or known contacts, never with a captured OTP"
  - name: "open_url"
    description: "Opens a URL unless its host was taken from untrusted screen content"
  - name: "open_app"
    description: "Opens an app by package name"
  - name: "scroll"
    description: "Scrolls the screen"
  - name: "back"
    description: "Presses Back"
  - name: "home"
    description: "Presses Home"
resources_exposed: []
prompts_exposed: []
---

AI agents that drive a phone can be steered by anything on its screen. A fake bank SMS can ask the
agent to forward a login code. White-on-white text on a web page can tell it to message a premium
number. A cloned login page can collect a password. ScreenWarden is an MCP server that gives any
MCP client phone tools with a security layer built in, so an operator does not have to watch every
tap.

## What it does

- Every screen is cleaned before the client's model reads it. Text a person cannot see is dropped:
  transparent, zero-size, off-screen, or present in the UI tree but missing from the screenshot.
  Instruction-like text from messages and web pages is dropped too, and the rest is labelled as
  untrusted data.
- Every action is checked before adb runs it. A recipient, URL or message body that came from the
  screen rather than from the user's goal is refused. OTP forwarding, credential entry on spoofed
  pages, payments, installs and settings changes are refused or need the user.
- Refusals come back as tool errors with the rule and an OWASP Agentic tag (ASI01 Agent Goal Hijack,
  ASI02 Tool Misuse). Every decision is written to a JSON-lines audit log.

## How it works

The server wraps adb over stdio JSON-RPC and needs only Python and PyYAML. One policy file covers
all apps. For apps the policy does not know, the optional `--learn` flag asks Claude to label each
new screen layout once. For example: this control sends, this field takes a password. Only the
structure is sent, with short button labels and field captions. Messages, page text, codes and
numbers are never sent. Labels are cached and can only make decisions stricter.
Without `--learn` the server makes no network calls.

On an Android 15 emulator, scripted attack plans succeed with the guard off and are stopped with it
on, in three attack types and in a messaging app the policy does not know. A real local model
(`llama3.2:3b`) followed a hidden web instruction with the guard off. With the guard on, the
instruction never reached it. In a matrix of 52 pages opened in real Chrome, covering 16 ways of
hiding an instruction and 7 attacker goals mapped to the OWASP Agentic Top 10, all 41 hijacked
actions were stopped and no text was removed from the 6 normal pages. The repository also ships a Python SDK, an adb proxy and an
Ollama-compatible gateway for agents that cannot use MCP.
