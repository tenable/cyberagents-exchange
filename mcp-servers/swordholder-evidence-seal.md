---
last_reviewed: 2026-11-03
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
network calls at all. Key generation, sealing, verification and the SQLite index are local file
operations, and the MCP server never opens an outbound socket. The default CLI paths are equally offline:
`swordholder triage` runs `rules-v1` only, and `verify` / `query` / `trust` never talk to a network.

Two opt-in paths can reach a model endpoint. Both are off unless an operator selects them.

1. **Rule enrichment** — `swordholder triage --llm`, or `swordholder serve` started with LLM enabled.
   `rules-v1` still fixes verdict and severity; the model is only asked for a hypothesis and suggested
   actions. The request is `POST {SWORDHOLDER_OLLAMA}/api/generate` carrying the normalized alert JSON,
   where `SWORDHOLDER_OLLAMA` defaults to `http://127.0.0.1:11434` (a local Ollama server). Nothing leaves
   the host unless that variable is repointed at a non-loopback address. If the model server is
   unreachable the run degrades to `rules-v1 (llm-not-running)` and the seal is still produced.
2. **Autonomous agent loop** — `swordholder agent` (demonstrated by `scripts/demo_agent_loop.py`). This is
   a separate entry point, not the path the MCP server or the default triage command takes. The provider is
   selected by `SWORDHOLDER_LLM_PROVIDER`, which defaults to `ollama` → `http://127.0.0.1:11434` (local).
   A remote endpoint is contacted only when the operator sets the variable explicitly: `anthropic` →
   `https://api.anthropic.com` (requires `ANTHROPIC_API_KEY`), `openai` → `https://api.openai.com/v1`
   (requires `OPENAI_API_KEY`, overridable with `SWORDHOLDER_OPENAI_BASE`). With a remote provider, the
   full normalized alert JSON and the accumulated tool observations are sent as the model prompt at each
   reasoning step, so alert content leaves the host once per LLM call, and only to the endpoint the
   operator configured. With the default local provider, nothing leaves the host.

Outside those two opt-in paths, the only network traffic in the project's life cycle is `git clone` and
`pip install` of the two runtime dependencies (`cryptography`, `pyyaml`).

## What it deliberately does not do

- It does not score or second-guess the verdict. Bad judgement seals as happily as good judgement.
- It does not provide a PKI, a CA, or key distribution. The anchor registry is a local JSON file that an
  operator populates out of band.
- It does not sandbox or contain the agent that produces the verdict.
- It is not on PyPI; installation is from source (`pip install -e .`), Python 3.11+.

## Reproducing

```bash
git clone https://github.com/mzymazy/swordholder && cd swordholder
pip install -e .
swordholder demo
swordholder verify .demo_out/<seal>.json --keys trusted_keys.json
```

`pytest -q` reports 61 passing tests, and `python mcp_server/selftest.py` reports 10/10 for the MCP
transport and tool surface. To wire it into an MCP client, point the client at
`python mcp_server/server.py` with the repository root as the working directory.
