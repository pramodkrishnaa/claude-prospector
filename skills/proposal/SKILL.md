---
name: proposal
description: >
  Turns a scope conversation or raw notes into a short, proof-led proposal /
  SOW that drives to your booking link, using your own services, proof, and
  voice. Use whenever the user asks to draft a proposal, write an SOW, scope
  a deal, or turn notes/a call into something a prospect can say yes to.
license: MIT
---

# Proposal

Turn messy scope notes into a tight proposal a prospect can say yes to.

## Before you start

Resolve the context file, in this order:
1. `./prospector.context.md` in the current directory.
2. `~/.claude/prospector/context.md`.
3. Neither exists → read `${CLAUDE_PLUGIN_ROOT}/templates/context.template.md`,
   copy it to `~/.claude/prospector/context.md`, tell the user to fill it in,
   and stop.

## Input
Ask for (or infer from notes): the prospect, their goal, what they need (map
to the services in the context file), timeline, and any budget signal.

## Output structure (keep it one page)
1. **What you're launching** — restate their goal in their words, one line.
2. **What we'll build** — the specific pieces, from the context file's
   services list.
3. **Proof** — the single closest case study from the context file + one
   hard number.
4. **How it works** — your process, briefly, in phases with a rough timeline.
5. **Investment** — follow the context file's pricing stance; don't put a
   hard number in writing unless that file says to.
6. **Next step** — the booking link from the context file.

## Rules
- Voice: follow the context file's voice section exactly.
- Never invent proof, a client, or a number not in the context file.
- The CTA is always the call/booking link, never a price over cold text/email.
