---
name: tenable-scan-calendar
description: Puts Tenable Vulnerability Management scans that are actively scheduled to run in the next 7 days onto the user's calendar, with each calendar event showing the severity breakdown (critical/high/medium/low/informational findings) from that scan's last completed run. Use this whenever the user asks what Tenable scans are coming up, asks to put scans on their calendar, asks about scan schedules combined with a calendar request, or wants a weekly heads-up on upcoming vulnerability scans and their recent results. Trigger even if the user just says something like "sync my scans to my calendar" or "what's scanning this week" without naming Tenable explicitly, as long as scan scheduling is clearly the topic.
---

# Tenable Scan → Calendar Sync

## What this skill does

Finds Tenable VM scans that have an active recurring schedule and are due to run in the next 7 days, then creates one calendar event per scan. Each event's description includes the finding counts (by severity) from that scan's most recent **completed** run, so the person can see at a glance both when the next scan fires and how bad things looked last time.

## Why the extra care around "is this scan actually scheduled"

`scan_list_scans` returns every scan definition, including ones that were run once by hand, are disabled, or reference a scanner that no longer exists. Don't treat "a scan exists" as "a scan is scheduled" — that produces a calendar full of noise. Confirm the schedule is actually enabled before creating an event.

## Step 1: Find candidates

1. Call `scan_list_scans` to get every scan.
2. For each scan, check whether its schedule is enabled by calling `scan_configure` with **only** `scan_id` (no other fields). This looks like an "update" tool, but calling it with no fields to change doesn't alter the scan — it's just the only available way to read back the current `Enabled` state (Tenable's MCP surface doesn't expose a pure read-only schedule-details call). The response includes an `Enabled` field:
   - `Enabled: True` → actively scheduled, keep it.
   - `Enabled: False` or `Enabled: None` → not scheduled to run on its own, skip it.
   - An error like "Scanner not found" or "Invalid uuid" → this scan definition is broken/orphaned. Skip it, but keep a short note of it so you can mention to the user that some scan entries couldn't be verified (don't silently drop this information).

## Step 2: Work out when each enabled scan will next run

Tenable's API surface here doesn't expose the schedule's rrule/start-time directly, so infer the cadence from history:

1. Call `scan_history` for the scan (default limit is fine — recent ~10-15 runs is plenty).
2. Look at the start times of the last several runs. Nearly all recurring scans in practice run weekly on a consistent day-of-week and time-of-day (occasionally daily or monthly) — read the pattern from the data rather than assuming weekly.
3. Project forward from the most recent run using that cadence to find the next occurrence that falls within the rolling 7-day window starting today (use the current date from context, not a hardcoded date).
4. If the history is too irregular to confidently infer a pattern (gaps vary a lot, or fewer than 3 runs exist), still surface the scan to the user but flag explicitly that the next-run time is uncertain rather than presenting a guess as fact.
5. If projecting forward lands outside the 7-day window, this scan doesn't get a calendar event this time around — skip it.

## Step 3: Pull severity counts from the last completed run

A zero-host result deserves the same skepticism as a wildly-different-from-normal result: a scan that finds 0 hosts every time is more likely scanning an unreachable or misconfigured target than a genuinely empty network. If `**Host Count:** 0` shows up, say so plainly in the event description rather than reporting "0 across the board" the same way you'd report a clean, fully-populated scan — those two situations look identical in the numbers but mean very different things to the person reading the calendar.

1. In the same `scan_history` results, find the most recent entry with `Status: completed` (skip `aborted`/`canceled`/`running` entries — their finding counts are unreliable or incomplete). If there is no completed run at all, note that in the event description instead of fabricating numbers.
2. Call `scan_results` with that scan's `scan_id` and the completed run's `history_id`.
3. This can come back two ways:
   - **Inline in the response** (small scans) — the markdown text is right there. Write it straight to a file under your working/outputs directory (the one your Bash tool can actually see — check your environment for the mapping between file-tool paths and shell paths, they often differ).
   - **Saved to a file** because it's too large for context — you'll get a file path instead. This file usually lives somewhere your Bash tool *cannot* reach (a different mount than your working directory), even though your Read/Grep tools can. Don't assume it's reachable from Bash — check first, and if it isn't, follow the extraction approach below rather than guessing.
4. **If the file isn't reachable from Bash (common case for large scans):** don't try to `Read` the whole thing — these files can be huge (100k+ tokens) and `Read` will refuse. Instead use Grep with `-o: true` on that file to pull out just the two patterns you need, and copy the matches into a new file in your Bash-reachable outputs directory using the Write tool:
   - Pattern A (per-host severity): `Vulns: \[Crit: \d+ \| High: \d+ \| Med: \d+ \| Low: \d+\]`
   - Pattern B (informational plugin counts): `\(Sev: 0\).{0,80}?Count: \d+` with `multiline: true`
   - **Set `head_limit` generously (500-1000, or higher for very large scans) — never rely on the default.** A truncated extraction silently under-counts and hands you a wrong severity total with no error message. Wrong numbers presented confidently are worse than no numbers with an honest caveat, so if you're at all unsure whether you captured every match (e.g. the match count looks suspiciously close to your head_limit), raise the limit and re-run rather than proceeding.
   - Write both sets of matches (Pattern A results, then Pattern B results) into one file, one match per line, then point the script at that file.
5. Either way, once you have a Bash-reachable file with the relevant text, run:
   ```
   python3 scripts/parse_severity.py <path-to-file>
   ```
   This prints JSON like `{"totals": {"critical": N, "high": N, "medium": N, "low": N, "info": N}, "host_count": N, "declared_host_count": N}`. Always use the script rather than eyeballing or hand-summing the raw text — these scans can have hundreds of hosts and manual summation (by you or a subagent) is exactly the kind of arithmetic that quietly goes wrong. If two runs of this skill on the same underlying scan data ever produce different severity totals, that's a sign an extraction step silently truncated — go back and check the match counts against `head_limit`.
   - `declared_host_count` comes from the scan's own `**Host Count:**` header. If it's wildly different from `host_count` (the number of per-host entries the script actually found and summed), say so — it usually means the results format shifted or an extraction step above missed entries, and the totals shouldn't be presented as authoritative without a caveat.

## Step 4: Create the calendar events

For each scan that survived steps 1-2 (enabled AND projected to run in the next 7 days), call the calendar tool's create-event function with:

- **summary**: `Tenable Scan: <scan name>`
- **startTime / endTime**: the projected next-run window, in UTC (`...Z` suffix) — pass ISO 8601 timestamps directly rather than guessing the user's timezone; the calendar tool converts to their local zone automatically. If the run's typical duration is unclear from history, default to a 2-hour block.
- **availability**: `AVAILABILITY_FREE` (a scan running in the background shouldn't block the person's calendar)
- **description**: include the scan ID/UUID, owner, the inferred cadence (e.g. "weekly, Fridays ~06:00 UTC"), and the severity breakdown from Step 3 formatted plainly, e.g.:
  ```
  Last completed run (2026-07-24): Critical: 1, High: 12, Medium: 45, Low: 8, Informational: 210
  Hosts scanned: 3
  ```
  If severity data was uncertain or unavailable, say so plainly instead of omitting it silently — the person is relying on this to know whether the next scan matters.

## Step 5: Summarize for the user

After creating the events, tell the user concisely: how many events were created, which scans they're for, and call out anything they should know about — scans that couldn't be verified as scheduled, scans whose next-run time is a best guess, or scans with no completed history yet. Don't bury this in a wall of text; a short list is fine.

## Notes

- This skill only touches the calendar (create events) and reads from Tenable — it does not modify any scan configuration, even though Step 1 technically calls a "configure" endpoint. Don't pass any fields to `scan_configure` beyond `scan_id`.
- If the user asks to also cover scans that are enabled but disabled/broken, or wants a different lookahead window than 7 days, adjust the window/filtering logic accordingly rather than treating 7 days as hardcoded gospel.
