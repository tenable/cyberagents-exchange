---
name: "Email-Analyst-in-a-box"
author: "austinsr1"
github_url: "https://github.com/austinsr1/assay"
description: "Eight-stage local triage chain for user-reported phishing, with a human checkpoint before every external mutation and an offline runner that enforces the contract."
license: "MIT"
tier: "contributed"
tags: ["phishing", "email-security", "triage", "local-inference", "playbook"]
domains: ["email-collaboration-security", "security-operations"]
integrations: ["GCP"]
date_added: 2026-11-04
contribution_agreement_date: 2026-11-04T16:56:57Z
works_with_tenable_hexa_mcp: false
playbook_type: "standard"
agents_used:
  - name: "Phish Triage Orchestrator"
    role: "Carries the eight-stage chain end to end and holds no external write tools."
    type: "github"
    ref: "https://github.com/austinsr1/assay"
  - name: "Phish Triage MCP Server"
    role: "Provides the typed tools the chain binds to: intake, parse, classify, adjudicate, verify."
    type: "github"
    ref: "https://github.com/austinsr1/assay"
---

# Email-Analyst-in-a-box

Built for Tenable SWARM Global 2026 by **Campus Autonomous Defenders (CAD)**.

## Scope: a triage layer, not primary detection

The name is a claim about **workload**, not about replacement. What goes in the box is the
part of an analyst's day spent proving that a reported message turned out to be nothing -
which is most of the day, and the part that does not need a person. What still needs a person
still gets a person, with the reasoning already assembled. Read everything below as that
division of labour rather than as a claim that the box is the analyst.

The input to this chain is a message **somebody already flagged** - a user who clicked
report phishing, or a secure email gateway that quarantined something and handed it on.
That flag is the detection decision, and it was made upstream by something else. This
playbook does not sit in the mail path, does not block delivery, and makes no claim about
interdicting a campaign that nobody reported.

What it does with a flagged message is the part that consumes an analyst's day: work out
whether it is nothing, whether it is something, or whether a person needs to look at it -
and in the third case hand that person the reasoning already assembled. So the figure that
matters is **how much of the queue gets settled automatically at a bounded error rate**,
not recall against novel attacks.

That boundary changes how to read the component numbers. A reviewer will find that the
phishing classifier caught **0 of 18** adversarial fixtures, and it is a fair thing to
find. It is not a claim about stopping new campaigns, because stopping them is the
gateway's job and by this point a human has already said the message looked wrong. It is a
measurement of one input to a triage decision, and this listing reports it rather than
burying it.

Two numbers carry the substance:

* **What it achieves** - across 203 real benign business emails, **84.2% were auto-cleared
  and none was falsely accused**, at roughly 90 ms per message for the whole local tier.
* **What it risks** - a **false clearance**: a reported threat waved through. That is the
  asymmetry the chain is built around, which is why clearance passes through a veto and
  every cleared case is written to an append-only ledger that a human can overturn, with
  the overturn recorded beside the original rather than replacing it.

### Why the cost unit is frontier calls, not accuracy

The published KnowBe4 PhishER playbook this chain is measured against does not have a cheap
rung. Its workflow polls every five minutes and sends each unresolved reported message to
Claude Sonnet 4 on Bedrock at `batchSize: 1`, which returns Clean, Spam or Threat and posts
the analysis to the ticket. Claude is the disposition, not a step before it. The consequence
is that the token spend does not depend on the outcome: **a reported message that turns out
to be a legitimate invoice costs the same call as one that turns out to be a credential
harvester.** That design bought real analyst time - about 930 hours a year on its own
published figures - and this does not argue with that. It removes the frontier spend
underneath it.

Which makes the useful unit **frontier cost per reported message**. Here, ~84% of reported
mail is settled by deterministic forensics and two small CPU models, and the ~16% residual
goes to a flash-class adjudicator **on the operator's own hardware**. Paid frontier API
calls are therefore zero rather than one per message. The reference published no clearance
or accuracy figure, and given its architecture there was none to publish; this one is
measured, and the corpora, licences and provenance behind it are in `docs/EVAL-SUITES.md`
and `eval/PROVENANCE.json`.

One limit stated up front rather than left to be found: neither adjudicator arm measured
here was Claude Sonnet 4. Both were flash-class, one local and one a third-party API used
purely as a comparison. So "no frontier call needed" rests on a local flash-class model
matching a remote flash-class one on this narrow task - an inference, not a head-to-head
against a frontier reasoning model.

## What it does

A user reports a suspicious email. This playbook reads it and produces one of four
dispositions - `threat`, `spam`, `clean`, or `manual_review` - together with the
evidence that produced it, a confidence band, an attack classification where one is
supported, and a list of proposed actions. Nothing is sent, labelled, commented on
or deleted without a human approving each action individually, and every approval
is bound to the specific verdict it was granted against.

It runs entirely on the operator's own infrastructure. There is no cloud inference
call, no vendor API, and no telemetry. Runtime dependencies are empty: the
package installs with nothing, and the deterministic stages are pure standard
library Python.

No part of it depends on a commercial platform, and that matters for a reason other
than licensing. User-reported phishing is the mail most likely to contain
credentials, HR complaints, executive correspondence and personal data - and in the
workflow this playbook is an alternative to, the full content of every reported
message, attachments base64-encoded, is sent to a public cloud inference endpoint in
a single AWS region. For a healthcare, finance, government or FERPA-covered
organization that is often a policy problem before it is a technical one. Here the
message never leaves the building, and the case record is a local SQLite file.

The honest counterweight: a commercial platform also brings accumulated
cross-customer link reputation and sits where the SOC already works. This playbook
has neither. It trades that for running anywhere, costing nothing per seat, and
keeping reported mail on-premises.

It also runs with **no models at all**. Every model tier is optional and records
`UNAVAILABLE` rather than failing when unconfigured, and the repository commits
recordings of real model responses so the whole cascade can be replayed offline. A
reviewer with no inference host, no credentials and no network access gets the same
verdicts the operator gets:

```
pip install .
tenable-email demo
```

## How it works

The chain is eight stages declared in a machine-readable contract, and the order is
enforced at runtime rather than by convention.

The first three stages are deterministic and do most of the work. MIME and header
parsing yields SPF, DKIM, DMARC and ARC results, Reply-To and Return-Path
divergence, and the full attachment inventory. Signal extraction then produces
lookalike-domain detection by edit distance against the organization's own domains
and a vendor catalogue, anchor-text-versus-destination mismatch, display-name
spoofing, forwarded-message unwrapping, redirect-wrapper unwrapping, bulk-mail
headers, and prompt-injection surface detection. Link analysis enumerates every
attribute that can carry a destination - anchors, form actions, meta refresh,
iframes, scripts, objects, embeds, base elements, images, SVG references, CSS
`url()` and inline event handlers - because a link analysis that reads only
`<a href>` reports an empty list for a page whose entire payload is a credential
form.

Only what the deterministic layer cannot settle goes to models: a classifier
cascade, a vision tier for inline images, and an adjudication model shown the
verified facts alongside the fenced message content. Message content is fenced as
untrusted in every prompt, and an injection attempt found in a reported message is
itself reported as a threat class rather than only defended against.

Evidence carries provenance. A parsed fact, a model judgment, an unknown and an
unavailable tier are four different things, and a verdict may not cite a finding
whose provenance does not support it. Each message produces a receipt holding
digests rather than copies - no message body and no attachment byte is persisted -
and the receipt contract refuses to let a record claim completeness when the
reading was partial, when a finding it cites is unknown, or when the evidence was
simulated.

## The design decision worth arguing about

Authentication is treated as evidence of **domain control, not of benign intent**.
Passing SPF, DKIM and DMARC proves somebody controls the sending domain, which is
equally true of an attacker who registered it that morning. An automatic clearance
therefore requires positive evidence: the sender is the organization or is on the
deployer's trust list, and every destination in the message is accounted for by
that same relationship. Everything else stays unsettled, the models are asked, and
`manual_review` is the outcome only if nothing corroborates a clearance.

This was not the original design. An external red-team review found the earlier
policy clearing adversarial mail at high confidence, and the finding was correct: a
decisive `clean` could not be reopened by anything downstream, so the error was
silent and permanent. `docs/RED-TEAM-RESPONSE.md` in the repository tracks all
eleven findings, what was verified against each, and what remains open. The
repository also ships eighteen hostile messages in `fixtures/adversarial/`, each
sent from a subdomain of the protected domain with authentication that genuinely
passes; seventeen are asserted to escalate and the eighteenth is the one open
finding, under a strict expected-failure mark so that fixing it fails the build
until the status is consciously updated.

What this playbook deliberately does **not** do is treat a destination mismatch as
a verdict. Legitimate mail links to unrelated services constantly, and a
compromised account links to its own domain, so an unrelated destination is
recorded as a fact and routed to a person rather than becoming an accusation.

## What it does not do

Stated plainly, because a limitation nobody published is a defect rather than a
limitation.

- **No accuracy claim is made anywhere.** The committed corpora are small and
  synthetic. `eval/metrics.json` reports measured behaviour over them - zero false
  negatives and zero false accusations on fourteen labelled fixtures, with a
  pinned floor on how many benign messages must still clear, because a tool that
  escalates everything satisfies every safety assertion and is useless - and those
  numbers are properties of those fixtures, not estimates for real mail.
- **Attachment contents are not read.** Extensions, MIME types, sizes and a
  dangerous-type flag are recorded, and an unexamined high-risk attachment blocks
  an automatic clearance, but PDF and Word text extraction is declared in the
  contract as not implemented and skipped with an explicit reason.
- **One red-team finding remains open.** A single forged `Authentication-Results`
  header with nothing to contradict it cannot be distinguished from a
  receiver-added one inside a raw `.eml`. Closing it needs the receiving system's
  own metadata, which a deployed Gmail or Alert Center adapter supplies.
- **No mail-system writeback destination ships.** The approval gate, the proposed
  actions and the single-use tokens are implemented and tested, and two providers
  exist: a dry run that records intention and changes nothing, and a local case
  ledger. Neither touches a mail system. Google Alert Center has no comment API -
  its only writable annotation is a four-value enum about whether the *alert* was
  useful - so the reference pattern of posting a tag and a comment has no drop-in
  equivalent, and inventing a destination nobody chose would be a claim about an
  integration that does not exist.

## Components

The MCP server in `agents_used` exposes nine read-only tools over stdio, so an
orchestrating agent can drive the chain without holding any write capability:
`analyze_eml`, `analyze_eml_directory`, `explain_verdict`, `check_auth`,
`lookalike_domain`, `analyze_urls`, `classify_local`, `list_contracts` and
`get_case_record`. Replay is forced on and the store's write path is unreachable
from a tool, so no tool mutates disk or network, and no tool returns message bodies
or attachment bytes. Write-capable outcomes come back as proposed actions with
`executed: false` plus the CLI command that runs the approval gate.

`SKILL.md` carries the workflow judgment the tools cannot convey on their own: when
to escalate, how to read a disagreement between tiers, why provenance matters, why
authentication is not legitimacy, and why a VIP list must come from a directory the
organization already trusts rather than from scraping its own web pages.
