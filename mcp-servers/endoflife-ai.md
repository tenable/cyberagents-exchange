---
name: "endoflife.ai - Software Lifecycle Intelligence"
author: "endoflife-ai"
github_url: "https://github.com/endoflife-ai/endoflife-mcp"
description: "End-of-life dates, EOL Risk Scores, CISA KEV exposure, SBOM audits and edge-device end-of-support status for 500+ products, read-only, no key required."
license: "MIT"
tier: "contributed"
tags: ["end-of-life", "eol", "end-of-support", "software-lifecycle", "cisa-kev", "risk-score", "sbom", "edge-devices", "bod-26-02", "exposure-management", "node"]
domains: ["governance-risk-compliance", "vulnerability-management"]
integrations: []
date_added: 2026-09-14
contribution_agreement_date: 2026-09-14T14:05:00Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop", "Cursor", "VS Code Copilot", "Windsurf", "Cline", "Gemini CLI", "Codex"]
transport: "both"
runtime: "node"
auth_method: "none"
tools_exposed:
  - name: "check_eol"
    description: "Is product X version Y past end of life? Status, dates and the source the date was read from."
  - name: "get_risk_score"
    description: "EOL Risk Score (0-100) with the factor breakdown: recency, attack surface, CISA KEV exposure, extended support."
  - name: "scan_stack"
    description: "Score a whole stack of product/version pairs in one call."
  - name: "list_products"
    description: "Search the 500+ tracked products and resolve names to slugs."
  - name: "get_product_lifecycle"
    description: "Full version history and lifecycle dates for one product."
  - name: "get_kev_exposure"
    description: "Every CISA Known Exploited Vulnerabilities entry attributed to a product, with due dates and required action, plus the exploited-and-unpatchable entries."
  - name: "get_upcoming_eol"
    description: "Everything reaching end of life in the next N days, catalog-wide or for a product list."
  - name: "get_edge_device_status"
    description: "End-of-support status for network edge platforms (firewalls, VPN gateways, routers, load balancers) against CISA BOD 26-02."
  - name: "get_upgrade_path"
    description: "Supported upgrade targets and the vendor-stated successor for a version."
  - name: "check_sbom"
    description: "CycloneDX or SPDX in; every component resolved by package URL and scored; unmatched components listed with a reason, never guessed."
resources_exposed:
  - name: "https://endoflife.ai/llms.txt"
    description: "endoflife.ai guide for assistants: what the site publishes, how to cite it, and the article index."
  - name: "https://endoflife.ai/eos-edge-devices.json"
    description: "EOS Edge Device Intelligence feed: edge platforms with BOD 26-02 end-of-support statuses, KEV records, CPEs and provenance."
  - name: "https://endoflife.ai/exploited-and-unpatchable.json"
    description: "Exploited & Unpatchable feed: exploited CVEs whose affected versions will never receive a fix."
  - name: "https://endoflife.ai/verification.json"
    description: "Accuracy and provenance report: where every served date comes from, live vendor feeds, open disagreements and published corrections."
  - name: "https://endoflife.ai/purl-map.json"
    description: "Package URL map: the purl-to-product join key that check_sbom uses."
  - name: "https://endoflife.ai/kev-products.json"
    description: "CISA KEV by product: every tracked product with its attributed KEV entries, dates, due dates and required actions."
  - name: "https://endoflife.ai/eos-edge-changelog.json"
    description: "EOS Edge feed change log: every edge line added, removed, re-dated or status-changed, by build date."
prompts_exposed:
  - name: "audit_stack"
    description: "Score every component of a stack, then explain what is end-of-life, what is actively exploited, and where to move."
  - name: "eol_calendar"
    description: "List what reaches end-of-life in a window, grouped by month, with the action each one needs."
  - name: "edge_device_review"
    description: "Review edge devices against CISA BOD 26-02: past end of support, within 12 months, and the KEV exposure of each."
---

Vulnerability scanners find the CVEs you have. This server answers the question underneath: is the software still receiving fixes at all, and if not, how urgent is that?

## What it does

endoflife.ai keeps lifecycle dates for 500+ products (operating systems, runtimes, databases, frameworks, network appliances and AI models), reconciled against the vendors' own lifecycle pages and the endoflife.date community dataset, with the source returned on every answer. The MCP server exposes that data read-only, with no key required:

- **Status and dates** for a product version, and the full lifecycle of a product.
- **EOL Risk Score**, 0 to 100, from how long a version has been unpatched, its attack surface, whether CISA lists it as actively exploited, and whether extended support can still be bought. The methodology is public at endoflife.ai/risk-score.
- **CISA KEV join**: which exploited vulnerabilities attach to a product, and the exploited-and-unpatchable set, meaning past end of life and on the KEV list, where no fix is coming.
- **Forward calendar**: what crosses end of life in the next 30, 90 or 365 days, so a team plans instead of reacts.
- **SBOM audit**: CycloneDX or SPDX in, components resolved by package URL, scored, and unmatched components named rather than guessed.
- **Edge devices**: 54 network appliance platforms (1,600+ release lines) against the BOD 26-02 deadline.

## How it works

The server is a thin, stateless layer over the public endoflife.ai API and its published JSON feeds. It runs hosted at mcp.endoflife.ai (streamable HTTP) or locally with `npx endoflife-mcp` (stdio); a Red Hat UBI container image is included for cluster deploys. Every tool is read-only and every answer carries `eol_date_source`, the vendor page or upstream record the date was read from. Lookup misses return "did you mean" suggestions instead of a guess.

## Where it fits with Tenable

Tenable's Security End of Life plugins tell you which scanned assets already run software past its security EOL. This server adds what a plugin cannot: the dates ahead (what goes out of support next quarter), the source behind each date, a severity that ranks EOL findings against each other, the CISA KEV cross-reference, whether paid extended support exists, and edge-device lines that a network scan sees only as a firmware string. Two listings already on this exchange (Tenable Asset EOL Tracker and security-intel-brief) pull lifecycle data from endoflife.date; this server is the same idea as a callable MCP layer, with vendor-verified corrections applied and the Risk Score and KEV join on top.

Typical agent use: pull an asset or package inventory from Tenable VM or a CMDB, call `scan_stack` or `check_sbom`, then `get_kev_exposure` for anything past end of life, and rank by EOL Risk Score. `get_upcoming_eol` turns the same inventory into a 90-day plan.

## Prerequisites and limits

- Hosted endpoint needs only outbound HTTPS; the stdio server runs on a current Node.js (the container image ships Node 22).
- No authentication and no write operations; nothing is stored between calls.
- Coverage is 500+ products; a product not in the catalog returns "not tracked" with suggestions, never a guessed date.
- Not yet tested against Tenable Hexa AI's MCP support, so `works_with_tenable_hexa_mcp` is false until it is.
