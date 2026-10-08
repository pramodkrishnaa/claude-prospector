---
name: lead-scout
description: >
  Scours the free public web for B2B companies that fit your ICP and produces
  a ranked, sourced prospect brief — company, a real dated trigger, the
  closest matching case study, a genuinely public contact, and 2-3 talking
  points. Never drafts or sends outreach; the human writes every message.
  Use this whenever the user asks to find leads, find prospects, build an
  outbound list, find B2B clients, scout startups to pitch, or asks "who
  should I reach out to" / "who should I pitch" / "find me some leads" —
  even if they don't say "lead-scout" explicitly.
license: MIT
---

# Lead Scout

Find real B2B companies worth reaching out to and hand the user a ranked
brief they can act on in minutes. **This skill researches — it does not
write or send email.**

## Before you start

Resolve the context file, in this order:
1. `./prospector.context.md` in the current directory (per-project override).
2. `~/.claude/prospector/context.md` (your default).
3. If neither exists: read `${CLAUDE_PLUGIN_ROOT}/templates/context.template.md`,
   copy it to `~/.claude/prospector/context.md`, tell the user to open and
   fill it in (company, ICP, proof, voice), and stop. Never guess someone's
   ICP, proof points, or case studies.

Then get the niche from the user, or default to a broad sweep. Examples:
"recently funded B2B infra", "devtools launching this month", "Series A SaaS
hiring for GTM".

## Pipeline

### 1. Source (free only — no paid APIs, no scraping behind logins)
Use `WebSearch` and `WebFetch` over public pages:

| Source | How |
|--------|-----|
| Y Combinator directory | `WebFetch` on `https://www.ycombinator.com/companies?industry=B2B` (add `&batch=<batch>` if given one) |
| Product Hunt (recent launches) | `WebFetch` the front page, then follow product pages that look B2B |
| Funding news | `WebSearch` "seed round B2B <sector> <month> <year> announced" → `WebFetch` the article |
| Accelerator cohorts | `WebSearch` for the batch/demo-day page, then `WebFetch` it |
| Founder posts | `WebSearch` public posts: "launching", "just raised", "hiring head of marketing" |

A few good sources beat a broad flaky crawl. Don't build a scraper for a page
`WebFetch` can't read — skip it and note the gap.

### 2. Qualify
For each candidate, score fit **0..1** against the context file's ICP. Drop
anything that's pure-consumer, has no visible founder, or has neither a
trigger nor a contact. Find the concrete **trigger** and its date (raise /
launch / batch / GTM hire / big release). Match the **closest case study**
from the context file as proof.

### 3. Build the lead objects
Emit a JSON array, one object per surviving lead, exactly these fields:

```json
[{
  "company": "Acme", "domain": "acme.com",
  "what": "one line on what they sell and to whom",
  "person": "Founder name", "contact": "public email or @handle or '' if none public",
  "trigger": "raised $2M seed", "trigger_date": "2026-09-20",
  "fit": 0.85, "case_study": "the matching case study name from your context file",
  "angle": ["observation about their current story/site", "why now (the trigger)", "proof point that matches"],
  "source_url": "https://..."
}]
```
Rules: `contact` is **only** a genuinely public address/handle — never a
guessed pattern. `angle` = 2-3 talking points the user turns into their own
email, NOT a written email.

### 4. Rank + output
For a handful of leads, rank them yourself (fit × how fresh the trigger is)
and output the Markdown brief directly — no script needed.

For a larger batch, or when the user wants a CSV, write the JSON array to
`leads.json` with the `Write` tool, then run:

```
Bash: python "${CLAUDE_PLUGIN_ROOT}/skills/lead-scout/scripts/rank.py" leads.json --csv prospects.csv
```

It dedups by domain, ranks by `fit × trigger-recency`, prints the Markdown
brief, and writes the CSV. Give the user the Markdown brief either way.

### 5. Track (optional)
If the user wants to track prospects, that's on their own tool (Linear,
Notion, a kanban board, a plain TODO) — not automated here.

## Guardrails
- Never fabricate a trigger, a contact, or a metric. If unknown, say so or
  leave it blank.
- Every lead cites a `source_url` the user can verify in one click.
- Quality over volume: 5 sharp, real, well-triggered leads beat 50 guesses.

## Self-check
`python scripts/rank.py --selftest` (verifies dedup + ranking, offline, no
network).
