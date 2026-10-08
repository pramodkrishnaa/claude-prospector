#!/usr/bin/env python3
"""Dedup + rank Prospector leads and emit a Markdown brief + CSV.

The LLM does the web sourcing/qualification and hands this script validated JSON
(one object per lead). This script owns the deterministic part — dedup, ranking,
formatting — so it doesn't depend on the model sorting things correctly.

Lead JSON fields: company, domain, what, person, contact, trigger,
trigger_date (ISO "YYYY-MM-DD" or ""), fit (0..1), case_study, angle (list[str]),
source_url.

Usage:
    python rank.py leads.json                 # -> prints Markdown, writes prospects.csv
    python rank.py leads.json --csv out.csv
    cat leads.json | python rank.py -
    python rank.py --selftest
"""
import csv, json, math, sys
from datetime import date, datetime

# ponytail: recency = exp(-days/30) — a naive 30-day half-life-ish decay. Fine for
# ranking. Swap for a real decay/weighting only if the ordering proves wrong.
def recency_weight(trigger_date: str, today: date) -> float:
    if not trigger_date:
        return 0.5  # unknown trigger age: neutral
    try:
        d = datetime.strptime(trigger_date, "%Y-%m-%d").date()
    except ValueError:
        return 0.5
    days = max((today - d).days, 0)
    return math.exp(-days / 30.0)

def score(lead: dict, today: date) -> float:
    return float(lead.get("fit", 0)) * recency_weight(lead.get("trigger_date", ""), today)

def dedup(leads):
    seen, out = set(), []
    for l in leads:
        key = (l.get("domain") or l.get("company", "")).strip().lower()
        if key and key in seen:
            continue
        seen.add(key)
        out.append(l)
    return out

def rank(leads, today=None):
    today = today or date.today()
    ranked = dedup(leads)
    for l in ranked:
        l["_score"] = round(score(l, today), 4)
    ranked.sort(key=lambda l: l["_score"], reverse=True)
    return ranked

CSV_COLS = ["company", "domain", "person", "contact", "trigger", "trigger_date",
            "fit", "_score", "case_study", "what", "source_url"]

def to_markdown(ranked):
    lines = ["# Prospects\n", f"_{len(ranked)} qualified, ranked by fit x trigger recency._\n"]
    for i, l in enumerate(ranked, 1):
        lines.append(f"## {i}. {l.get('company','?')}  |  score {l.get('_score')}")
        lines.append(f"- **What:** {l.get('what','')}")
        lines.append(f"- **Who:** {l.get('person','?')}  |  **Contact:** {l.get('contact') or '(find manually)'}")
        lines.append(f"- **Trigger:** {l.get('trigger','')}  ({l.get('trigger_date') or 'date?'})")
        lines.append(f"- **Fit:** closest proof = {l.get('case_study','?')}")
        angle = l.get("angle") or []
        lines.append("- **Angle (your talking points - you write the mail):**")
        lines += [f"    - {a}" for a in angle] or ["    - (none)"]
        lines.append(f"- source: {l.get('source_url','')}\n")
    return "\n".join(lines)

def write_csv(ranked, path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(ranked)

def selftest():
    ref = date(2026, 9, 30)
    leads = [
        {"company": "A", "domain": "a.com", "fit": 0.9, "trigger_date": "2026-09-29"},  # fresh, high fit
        {"company": "B", "domain": "b.com", "fit": 0.9, "trigger_date": "2026-06-01"},  # high fit, stale
        {"company": "A dup", "domain": "a.com", "fit": 0.5, "trigger_date": ""},          # dup of A
        {"company": "C", "domain": "c.com", "fit": 0.4, "trigger_date": "2026-09-29"},  # fresh, low fit
    ]
    r = rank(leads, today=ref)
    assert len(r) == 3, f"dedup failed: {len(r)}"                 # A dup dropped
    assert r[0]["company"] == "A", f"A should rank first: {r[0]}"  # fresh + high
    assert r[-1]["company"] == "B", f"B (stale) should rank last: {r[-1]}"
    assert recency_weight("", ref) == 0.5
    print("selftest OK")

def main(argv):
    if "--selftest" in argv:
        return selftest()
    args = [a for a in argv[1:] if not a.startswith("--")]
    csv_path = "prospects.csv"
    if "--csv" in argv:
        csv_path = argv[argv.index("--csv") + 1]
    src = args[0] if args else "-"
    raw = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    ranked = rank(json.loads(raw))
    write_csv(ranked, csv_path)
    sys.stdout.write(to_markdown(ranked))
    sys.stderr.write(f"\n[wrote {len(ranked)} prospects to {csv_path}]\n")

if __name__ == "__main__":
    main(sys.argv)
