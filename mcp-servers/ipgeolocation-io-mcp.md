---
last_reviewed: 2026-10-21
name: "IPGeolocation.io MCP Server"
author: "IPGeolocation"
github_url: "https://github.com/IPGeolocation/ipgeolocation-io-mcp"
description: "17 tools for accurate IP geolocation, company information, ASN and network data, IP security, abuse contacts, time zones, astronomy, currency data and user-agent parsing."
license: "MIT"
tier: "contributed"
tags: ["geolocation", "osint", "ip-address", "asn", "security"]
domains: ["threat-intelligence", "security-operations"]
integrations: ["IPGeolocation.io"]
date_added: 2026-10-21
contribution_agreement_date: 2026-10-21T09:31:21Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop", "Cline", "Codex", "Cursor", "Gemini CLI", "VS Code Copilot", "Windsurf"]
transport: "stdio"
runtime: "node"
auth_method: "api-key"
tools_exposed:
  - name: "lookup_ip"
    description: "IP geolocation with optional company, ASN, network, security, abuse, time zone and currency fields."
  - name: "bulk_lookup_ip"
    description: "IP geolocation for batches of IP addresses."
  - name: "get_my_ip"
    description: "Public egress IP of the server host, without an API key."
  - name: "lookup_company"
    description: "Company name, domain and type, alongside ASN ownership fields."
  - name: "lookup_currency"
    description: "Currency code, name and symbol with country metadata."
  - name: "lookup_network"
    description: "Route prefix, connection type and anycast status."
  - name: "check_security"
    description: "VPN, proxy, Tor, bot, hosting and spam indicators for an IP."
  - name: "bulk_security_check"
    description: "IP security indicators for batches of IP addresses."
  - name: "get_timezone"
    description: "Time zone details for an IP, location, airport or IANA time zone."
  - name: "convert_timezone"
    description: "Time conversion between source and destination time zones or locations."
  - name: "get_astronomy"
    description: "Sun, moon and twilight data for one date or the current time."
  - name: "get_astronomy_time_series"
    description: "Daily astronomy data across a date range."
  - name: "lookup_asn"
    description: "ASN registration and organization details, plus route and relationship datasets with WHOIS records."
  - name: "get_abuse_contact"
    description: "Abuse reporting contacts for an IP address."
  - name: "parse_user_agent"
    description: "Browser, device and operating system data from a user-agent string."
  - name: "bulk_parse_user_agent"
    description: "Parsed browser, device and operating system data for multiple user agents."
  - name: "get_cached_result"
    description: "Complete cached result pages without another API request or additional credits."
resources_exposed: []
prompts_exposed: []
---

## What it does

IPGeolocation.io's official MCP server provides 17 tools for accurate IP geolocation, company information, ASN and network data, IP security (VPN, proxy, Tor, bot, hosting and spam detection), abuse contacts, time zones, astronomy, currency data and user-agent parsing.

Investigators can enrich IP indicators with location and company information. They can inspect routing and security signals and identify abuse reporting contacts. Company fields describe the company name, domain and type. ASN fields describe the autonomous system and its organization, registration, routes and relationships. IP geolocation describes network location; it does not establish a person's identity or exact address.

## How it works

The server runs as a local Node.js process over stdio. It sends lookup inputs to `https://api.ipgeolocation.io` over HTTPS and returns text and structured results to the MCP client. Authenticated requests use the `x-ipgeolocation-api-key` header. The provider receives the requested lookup data and the server's public egress IP; see the [security and privacy documentation](https://github.com/IPGeolocation/ipgeolocation-io-mcp/blob/main/SECURITY.md).

Bulk tools accept up to 250 inputs by default. Large responses use cached pagination: `get_cached_result` reads the remaining pages without another API request or additional credits. Results stay in process memory, with five-minute expiry by default; successful page reads renew a snapshot's idle expiry. Eviction or a process restart can remove cached results.

## Installation and access

Requires Node.js 22 or later. Add this entry to your client's MCP server configuration and replace the placeholder with your API key in private client settings:

```json
{
  "mcpServers": {
    "ipgeolocation": {
      "command": "npx",
      "args": ["-y", "ipgeolocation-io-mcp@latest"],
      "env": {
        "IPGEOLOCATION_API_KEY": "<YOUR_API_KEY>"
      }
    }
  }
}
```

The server starts without a key, and `get_my_ip` works without one. The other 15 API tools require a key. Cached page retrieval uses the same key and running process as the original lookup. Client-specific configuration formats and setup steps appear in the [installation guide](https://github.com/IPGeolocation/ipgeolocation-io-mcp#install-by-client).

The free plan provides 1,000 API credits per day, including accurate IP geolocation, basic ASN data, time zone details, and user-agent parsing. Company information, detailed ASN and network data, IP security, and abuse contact information require a paid plan.

The server code uses the MIT license. API access follows the account's plan and credit limits. See the [API documentation](https://ipgeolocation.io/documentation.html) for endpoint fields and billing rules.
