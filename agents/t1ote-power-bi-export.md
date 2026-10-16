---
name: "Tenable OT to Power BI Export (reference application)"
author: "dpstorey"
github_url: "https://github.com/dpstorey/T1OTE_POWER_BI"
description: "Reference app: exports Tenable One OT Exposure assets from Enterprise Manager into a Power BI push dataset."
license: "Apache-2.0"
tier: "contributed"
tags: ["tenable", "ot-security", "power-bi", "asset-inventory", "reporting", "reference-implementation"]
domains: ["ot-iot-security", "platform-operations"]
integrations: ["Tenable"]
date_added: 2026-10-16
contribution_agreement_date: 2026-10-16T16:09:19Z
---

A small, readable Python command-line program that pulls OT assets from **Tenable One OT Exposure / Enterprise Manager** and loads them into a **Microsoft Power BI** dataset, so they can be charted and filtered alongside other reporting. It is a *reference implementation*: run it as-is to evaluate, or read and adapt it for your own pipeline. It is a single, fully commented file with a Doxygen documentation layer and an offline test suite.

## What it does

Each run takes a point-in-time snapshot. It reads assets from Enterprise Manager's GraphQL API (resolving the site, paging through results, and optionally filtering by site, criticality, subnet or IP range), shapes them into flat rows, then clears and refills a Power BI push dataset table so the report always shows the latest export. A `--dry-run` mode fetches and summarises without touching Power BI.

Commands: `sites` (list paired sites), `login` (one-time Microsoft device-code sign-in), `create-dataset` (create the push dataset), `export` (run the export).

Exported columns: `asset_id`, `name`, `site`, `vendor`, `model`, `criticality`, `ips`, `last_seen`, `total_risk`, `exported_at`.

## How it works

Power BI push datasets accept rows only from a signed-in user (service principals are not supported), so the program signs in once with the OAuth device-code flow, keeps the refresh token in an owner-only file, and saves each rotated token as it is issued. Rows are sent in batches of at most 10,000. All HTTP goes through one function (`make_client`), which is the seam the tests replace with a fake transport, so the 30 tests need no network or credentials. Tenable access is read-only; in Power BI the program only creates its own dataset and replaces the rows of its own table.

## Prerequisites

- Python 3.9 or newer; `pip install -r requirements.txt` (httpx, python-dotenv).
- A Tenable OT Exposure / Enterprise Manager API key (`accessKey=...;secretKey=...`) whose user can read assets, and network access to the EM.
- A Power BI Pro (or better) user with Contributor or Member on the target workspace, and an Entra ID app registration (public client flows enabled, delegated `Dataset.ReadWrite.All`), as described in the README.

## Running it

```bash
cp .env.example .env            # fill in the Tenable and Azure settings
python t1ote_export.py sites
python t1ote_export.py login
python t1ote_export.py create-dataset     # paste the printed POWERBI_DATASET_ID into .env
python t1ote_export.py export --criticality-at-least high --dry-run
python t1ote_export.py export
```

## Known limitations

- Push datasets do not auto-refresh an open report page; a dashboard tile pinned from the report does refresh after each export.
- Power BI limits: 10,000 rows per request, 200,000 rows per table (FIFO retention), plus per-minute and per-hour request caps (not handled; ordinary OT-site exports sit far below them).
- The dataset schema is fixed at creation; changing columns means creating a new dataset.
- At most 50,000 assets are fetched per run (a safety limit).
- Delegated sign-in only; there is no unattended service-principal mode, because Power BI does not allow one for push datasets.
- Validated by the author against a live Enterprise Manager and Power BI workspace; not load-tested at very large scale.
- Community reference implementation, provided as-is and not an officially supported Tenable product; not affiliated with or endorsed by Microsoft. Portions of the Tenable client logic are adapted from the Tenable OT MCP Server by John Walley / OneClearPath (Apache-2.0); see NOTICE.
