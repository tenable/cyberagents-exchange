---
name: "NASL Writer"
author: "quanxk"
github_url: "https://github.com/quanxk/skill-nasl-writer"
description: "NASL/Nessus plugin writing skill. 25+ patterns, .inc library guide, vendor templates, VCF framework."
license: "MIT"
tier: "unreviewed"
tags: ["nessus", "nasl", "tenable", "plugin-development", "vulnerability-management", "security-scanning"]
integrations: ["Tenable"]
date_added: 2026-06-30
compatible_platforms: ["Claude Code"]
invocation: "/nasl-writer"
---

A structured knowledge pack that makes AI coding assistants an expert in writing custom Nessus/NASL plugins for Tenable Security Center and Nessus. Distills real plugin patterns from the Tenable plugin family so the AI writes correct, maintainable, production-ready NASL on the first try.

## What it does

- Covers the complete NASL plugin structure: `script_id`, `script_set_attribute`, `script_category`, family, copyright, and dependencies - with the exact ordering rules that new plugin authors get wrong.
- 25 ready-to-adapt detection patterns: banner grabbing, CVE signature checks, default credential testing (Telnet/HTTP/SNMP), buffer overflow probes, UDP protocol detection, Windows registry reads, backdoor/backdoor-shell signatures, backported-patch detection, and more.
- Walks through every important `.inc` library: `http.inc`, `ftp_func.inc`, `smb_func.inc`, `ssl_funcs.inc`, `vcf.inc`, `install_func.inc`, `webapp_func.inc`, `telnet_func.inc`, `byte_func.inc`, with realistic function-by-function examples.
- Producer-template specialist recipes for the VCF (Version Check Framework), the modern Tenable way to express vulnerability constraints (`less`, `equal`, `greater`, `range`) instead of hand-rolled `ver_compare` chains.
- Vendor-specific detection patterns for Cisco ASA SSL VPN, Cisco Small Business Routers (SNMP), Cisco TelePresence MCU (FTP+SNMP), Citrix NetScaler, VMware ESXi / vCenter, SAP NetWeaver, F5 BIG-IP, and KVM Over IP appliances.

## How it works

The skill is a pure-text knowledge pack (no scripts to run). Place the `skill-nasl-writer` directory in your AI coding assistant's skills directory (`~/.claude/skills/nasl-writer/` for Claude Code). The skill activates whenever you ask about NASL plugin structure, Nessus plugin writing, a CVE detection, or a plugin compilation error. It guides the model through the correct plugin skeleton, dependency declarations, includes, report functions (`security_note` / `security_warning` / `security_hole`), and exit conventions so the generated plugin compiles cleanly and runs without surprises.

Three reference templates are included in the skill: a generic custom plugin template (using the `900000-999999` ID range with `script_family(english:"Custom Plugins")`), a web-app detection template, and a custom-binary protocol template - all written so you can fork them and rename the placeholders.
