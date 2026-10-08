---
name: copy
description: >
  Writes landing-page, case-study, and founder-content copy in your brand
  voice, proof-led and buzzword-free, using the services/proof/voice defined
  in your context file. Use whenever the user asks to write landing page
  copy, a case study writeup, founder content, or marketing copy for their
  own company.
license: MIT
---

# Copy

Marketing/product copy in your voice.

## Before you start

Resolve the context file, in this order:
1. `./prospector.context.md` in the current directory.
2. `~/.claude/prospector/context.md`.
3. Neither exists → read `${CLAUDE_PLUGIN_ROOT}/templates/context.template.md`,
   copy it to `~/.claude/prospector/context.md`, tell the user to fill it in,
   and stop.

## Voice
Follow the context file's voice section exactly — tone, verbatim lines, and
what to avoid. When in doubt: short sentences, lead with the useful thing,
show proof instead of adjectives.

## Common jobs
| Job | Notes |
|-----|-------|
| Landing / product page | hero = one clear promise + a proof number; every section tells the same story; CTA = the context file's booking link |
| Case-study writeup | problem → what you built together → the number/outcome |
| Founder content | hooks, cuts, captions for whatever channel the user names |

## Rules
- Never invent a metric, client, or outcome not in the context file.
- Every claim earns its place with proof or gets cut.
