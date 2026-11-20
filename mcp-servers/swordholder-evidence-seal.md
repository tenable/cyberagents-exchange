---
name: "Swordholder Evidence Seal"
author: "mzymazy"
github_url: "https://github.com/mzymazy/swordholder"
description: "Seals an AI agent's alert-triage verdict into an offline-verifiable ed25519 evidence record, so downstream SOC tooling can prove who concluded what, from which payload, unaltered."
license: "Apache-2.0"
tier: "contributed"
tags: ["alert-triage", "evidence-integrity", "ed25519", "audit-trail", "incident-response", "agent-output-verification"]
domains: ["security-operations", "ai-security"]
integrations: ["Splunk", "Microsoft Sentinel"]
date_added: 2026-10-31
contribution_agreement_date: 2026-10-31T03:46:46Z
works_with_tenable_hexa_mcp: false
compatible_clients: ["Claude Code", "Claude Desktop"]
transport: "stdio"
runtime: "python"
auth_method: "none"
tools_exposed:
  - name: "seal_record"
    description: "Sign a triage verdict or response record (JSON) into a .seal.json envelope: payload digest binding plus ed25519 signature, written to disk."
  - name: "verify_seal"
    description: "Re-verify a .seal.json from raw bytes: recompute the payload digest, check the ed25519 signature and compare the signing key against the trust-anchor list. Returns VALID, VALID_UNTRUSTED_KEY or INVALID with an error code."
  - name: "verify_proof"
    description: "Verify a Swordholder deterrence proof end to end: integrity, signature, trust anchor and freshness window, returning VALID or INVALID with a reason code."
  - name: "list_trusted_keys"
    description: "List the locally registered trust anchors with key ids and public-key fingerprints, for manual issuer identification."
  - name: "keygen"
    description: "Generate an ed25519 key pair on the local machine; refuses to overwrite an existing private key and returns the public key hex for anchor registration."
resources_exposed: []
prompts_exposed: []
---

Swordholder is a small, dependency-light Python project that solves one narrow problem: when an AI agent
(or a rules engine) decides that an alert is a true positive, that decision currently lives only in a chat
transcript or a log line. Nobody downstream can show, later, which verdict was produced, over which byte
exact payload, at what time, and that it was not edited afterwards.

Swordholder does not try to judge whether the verdict is correct. It makes the verdict's provenance
independently checkable by a third party who has neither the source code nor any reason to trust the issuer.

## What it does

The MCP server exposes five tools over stdio:

- `keygen` — creates an ed25519 key pair on the local host. The private key is written with restrictive
  permissions and an existing key file is never overwritten; the public key hex is returned so it can be
  registered as a trust anchor elsewhere.
- `seal_record` — takes a JSON record (a normalized alert plus its triage verdict, or a response action
  record) and produces `<name>.seal.json` containing a `seal_header`, the untouched `payload`, and a
  detached `signature`.
- `verify_seal` — reads the seal file from disk and verifies it from raw bytes, not from re-serialized
  Python objects. It returns one of three verdicts: `VALID`, `VALID_UNTRUSTED_KEY` (cryptographically
  sound but the signing key is not a registered anchor, always accompanied by `E_NO_TRUST_ANCHOR`), or
  `INVALID` with a specific error code such as `E_PAYLOAD_TAMPERED` or `E_BAD_SIGNATURE`.
- `verify_proof` — checks a deterrence proof file: signature, anchor, and validity window, reported per
  file rather than as one aggregate pass/fail score.
- `list_trusted_keys` — dumps the local anchor registry (`key_id`, `public_key_hex`,
  `fingerprint_sha256`) so an operator can compare a fingerprint through an out-of-band channel.

The same core is also reachable without MCP, as a CLI (`swordholder triage`, `swordholder verify`,
`swordholder query`, `swordholder trust add|retire|revoke|check`) and as a local HTTP service
(`swordholder serve`, exposing `/healthz` and `/v1/schema`). All three entry points share one
implementation, so a seal produced through MCP verifies identically through the CLI.

## How it works

The signing input is a domain separator, the SHA-256 of the canonicalized payload, a newline, then the
canonicalized header:

```
signing_input = "swordholder-seal-v1\n" || sha256(c14n(payload)) || b"\n" || c14n(header)
```

`c14n` is a documented canonicalization (`json-c14n-v1`: sorted keys, no extra whitespace, UTF-8,
non-ASCII not escaped) that both signer and verifier use, so re-implementation in another language is
unambiguous. Because the header is inside the signing input, changing the issuer, subject or timestamp
invalidates the signature exactly like changing the payload does — those fields are not "metadata floating
outside the signature".

Trust is fail-closed. A signature that verifies against a key which is absent from `trusted_keys.json` is
never reported as a bare `VALID`; it degrades to `VALID_UNTRUSTED_KEY`. Anchors can be added, retired, or
revoked with overlapping windows, and existing seals are re-evaluated against revocation state instead of
silently becoming unverifiable.

Alert ingestion normalizes generic JSON as well as Splunk, Microsoft Sentinel and Wazuh shaped alerts; an
unrecognized shape is rejected explicitly rather than guessed.

The listing's `integrations` field is about **alert-format interop, not API integration**: Swordholder
parses Splunk and Microsoft Sentinel shaped alert JSON into its normalized record so that a verdict can be
sealed over it. It does not call either product's API, holds no credentials for them, sends them nothing, and
requires no agent or app installed on those platforms.

The **default** triage engine is `rules-v1`, a small deterministic rules engine behind a stable interface.
It needs no model and no network, and it is what the default triage entry points use: `swordholder triage`
and `POST /v1/triage`. The MCP tools do not triage at all: `seal_record` signs whatever record the caller
hands it, so it stays neutral about which engine produced that verdict. Two optional paths layer an LLM on top and both are
off unless an operator selects them: (`swordholder triage --llm`, or `swordholder serve` with LLM enabled)
uses a model only to add a hypothesis and suggested actions while `rules-v1` keeps verdict and severity;
and the separate `swordholder agent` loop hands verdict selection to the model, with `rules-v1` as its
fallback when the guardrail rejects an answer or the steps are exhausted. Neither is required for
seal/verify. Records and verdicts are indexed in a local SQLite file for `query` lookups; nothing is
uploaded.

## Data flows

The five MCP tools (`keygen`, `seal_record`, `verify_seal`, `verify_proof`, `list_trusted_keys`) make no
network calls: key generation, sealing, verification and the local index are file operations, and the MCP
server opens no outbound socket. The default CLI paths are offline as well — `swordholder triage` runs
`rules-v1` only, and `verify`, `query` and `trust` never reach a network.

Four paths can leave the host. All four are opt-in, and each is off unless an operator switches it on.

1. **Rule enrichment — LLM.** `swordholder triage --llm`, or `swordholder serve` with the LLM switch
   enabled. `requests` POSTs the normalized alert JSON to `{SWORDHOLDER_OLLAMA}/api/generate`;
   `SWORDHOLDER_OLLAMA` defaults to `http://127.0.0.1:11434`, i.e. loopback. If the endpoint is
   unreachable the run degrades to `rules-v1` and records `llm-not-running`.
2. **Autonomous agent loop — LLM.** `swordholder agent` (`scripts/demo_agent_loop.py`). The provider comes
   from `SWORDHOLDER_LLM_PROVIDER`, defaulting to `ollama` → `http://127.0.0.1:11434`. A remote endpoint
   is contacted only if the operator names one: `anthropic` → `https://api.anthropic.com` (needs
   `ANTHROPIC_API_KEY`), `openai` → `https://api.openai.com/v1` (needs `OPENAI_API_KEY`, base
   overridable with `SWORDHOLDER_OPENAI_BASE`). The full normalized alert JSON and the tool observations
   form the model prompt at each reasoning step, so alert content leaves the host once per LLM call, and
   only to the endpoint that was configured.
3. **External timestamping — RFC 3161.** `swordholder/timestamp.py` obtains an RFC 3161 `TimeStampResp`
   for a detached seal. In the package itself there is no default TSA and no automatic stamping:
   `stamp_digest` and `stamp_bytes` take a `timestamp_url` argument, and nothing in the MCP tool surface,
   `swordholder seal` or `swordholder triage` supplies one. The package carries `KNOWN_TSAS` as examples —
   `https://freetsa.org/tsr`, `http://timestamp.digicert.com`, `http://timestamp.sectigo.com` — each with a
   15 s timeout. What crosses the wire is a DER-encoded `TimeStampReq` (message imprint over a SHA-256
   digest of the seal payload, plus a nonce); the alert record itself is never sent. The helper
   `probe_authorities(urls=None, timeout=6.0)` walks `KNOWN_TSAS` when called without arguments and is not
   called anywhere in the repository. One carve-out worth naming: `scripts/stage11/compliance_probe.py` —
   a research/CI probe rather than a shipped path — does stamp for real. It carries its own candidate list
   (`https://freetsa.org/tsr`, `http://timestamp.digicert.com`, `https://rfc3161.ai.moda`), tries each
   twice at 20 s per attempt, stops at the first success, and takes `SWORDHOLDER_TSA_URL` as an override;
   if every candidate fails it records the failures and reports an unanchored stub instead of claiming an
   anchor it did not obtain.
4. **Transparency-log anchoring — Sigstore Rekor.** `swordholder/transparency.py` can anchor a seal in a
   public transparency log. `make_backend()` defaults to `none` — anchoring is disabled unless chosen
   explicitly, and an explicit `rekor` request that cannot be met fails loudly instead of silently
   downgrading. When enabled, the default base is `https://rekor.sigstore.dev` (25 s timeout) and the
   submission is a signed anchor statement carrying `trace_id`, `seal_sha256` and `tsa_token_sha256`:
   digests and identifiers only, not the alert payload. Anything submitted to a public log is publicly
   readable by design. The same `scripts/stage11/compliance_probe.py` probe is what selects this backend,
   and it does so by default: its log spec falls back to `rekor` and is overridable with
   `SWORDHOLDER_TLOG` (including `none`). The MCP tools and the default CLI never construct a Rekor
   backend.

Outside those four opt-in paths, the only network traffic in the project's life cycle is `git clone` and
`pip install` of the runtime dependencies (`cryptography`, `pyyaml`).

What it does not do: does not score or second-guess the verdict; does not provide PKI/CA/key distribution;
does not sandbox the agent; not on PyPI; installation from source (`pip install -e .`), Python 3.11+.

## Reproducing

```bash
git clone https://github.com/mzymazy/swordholder && cd swordholder
pip install -e .
swordholder demo
swordholder verify .demo_out/<seal>.json --keys trusted_keys.json
```

`pytest -q` covers the seal/verify/trust, timestamp and transparency paths; the count grows with each
release, so take the current figure from the repository's CI status rather than a number frozen here.
`python mcp_server/selftest.py` prints a per-check summary for MCP transport and tool surface. To wire it into an MCP client, point the client at
`python mcp_server/server.py` with the repository root as the working directory.
