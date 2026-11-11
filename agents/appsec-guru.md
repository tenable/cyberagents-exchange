---
name: "AppSec Guru"
author: "yukselao"
github_url: "https://github.com/yukselao/appsec-guru"
description: "A self-hosted application-security cockpit for Tenable Security Center and WAS, with an offensive AI agent that turns scan findings into attack paths and an agentic SAST reviewer."
license: "MIT"
tier: "contributed"
tags: ["web-application-scanning", "dast", "sast", "offensive-security", "recon", "ffuf", "rustscan", "subfinder", "ollama", "docker"]
domains: ["application-security", "vulnerability-management"]
integrations: ["Tenable"]
date_added: 2026-11-10
contribution_agreement_date: 2026-11-10T23:38:09Z
works_with_tenable_hexa_mcp: false
---

**AppSec Guru** is a Docker Compose cockpit built around **Tenable Security Center**
and its **Web Application Scanning (WAS)** sensors. It drives real WAS scans from a
guided wizard or saved, scheduled scan profiles, captures each scan's debug log live
over SSH, and adds an **offensive-security AI agent** that reads the findings — including
informational plugins used as reconnaissance — and produces ranked attack paths, a
category breakdown and a standalone HTML report.

## What it does

- **DAST (Tenable WAS):** derive a policy with chosen plugin families, launch on
  Security Center, stream the sensor's scanner log filtered to that scan, and store
  findings. One Security Center, many sensors.
- **Offensive AI analysis:** a local LLM (Ollama) turns a scan's findings into attack
  paths, quick wins and a reconnaissance table, rendered as an HTML report. An AI chat
  on every page can analyse pasted or attached logs.
- **SAST:** an agentic harness clones a Git repo, extracts functions and their sinks,
  and reviews each argument from source to sink with tools (get_function, read_file,
  search_code) and the same local LLM.
- **Open-source recon tools, each in its own container with a deterministic protocol:**
  Subdomain Discovery (subfinder → dnsx → httpx), Hidden Path Discovery (ffuf) and
  Port Scan (RustScan).

## How it works

nginx fronts a PHP/Twig UI and a FastAPI backend. The backend talks to the Security
Center REST API, SSHes to each WAS sensor for logs and debug control, orchestrates the
recon tool containers over a standard line protocol, and calls Ollama for analysis and
the SAST agent. Agents, skills and tools are defined as Markdown under `ai/` and read at
run time. Settings come from `.env` with UI overrides; secrets are encrypted at rest.

See the repository README for prerequisites, setup, outputs and known limitations.
