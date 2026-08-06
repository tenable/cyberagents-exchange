---
name: "ThreatCorraling"
author: "giraldomauricio"
github_url: "https://github.com/giraldomauricio/threatcorraling"
description: "Correlates results from Checkmarx with Tenable WAS via a JSON glue file."
license: "MIT"
tier: "contributed"
tags: ["Checkmarx", "SAST", "WAS", "Tenable","CxOne"]
integrations: ["Tenable"]
date_added: 2026-08-05
contribution_agreement_date: 2026-08-05T00:00:00Z
works_with_tenable_hexa_mcp: false
transport: "stdio"
runtime: "python"
auth_method: "none"
compatible_clients: ["Claude Desktop", "Claude Code"]
tools_exposed:
  - name: "get_checkmarx_sast_for_scoped_projects"
    description: "Get Checkmarx Projects selected from the JSON."
  - name: "get_tenable_was_for_scoped_domains"
    description: "Get Tenable WAS results selected from the JSON."
resources_exposed: []
prompts_exposed: []
---

Optional longer description of your MCP server.

## What it does

ThreatCorralling is an intelligent, extensible Vulnerability Correlation Agent and Model Context Protocol (MCP) server. It bridges the gap between disparate security tools by analyzing scoped assets across platforms like Checkmarx SAST and Tenable WAS.

## How it works

Using FastMCP wrapper, the file sits in the background and waits for an external AI to ask for a correlation between CxOne Projets and Tenable WAS targets. It then executes the tools locally and passes the data back to the AI. For performance, the server caches the results for further use. This feature can be replaced by a database or any other better persistence method.
