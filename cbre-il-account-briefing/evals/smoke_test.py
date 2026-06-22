"""Smoke test for the v8 scene skill: exercise the scene renderer (every cell
kind: prose, stat, list, table, panel, quote, heading, rule) and the gate
scripts with a tiny synthetic plan. Validates the skill code, not any company.
Builds with NO PowerPoint (resolve + label + bake off) so it runs anywhere.
Run: python evals/smoke_test.py
"""
import csv
import json
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SKILL / "helpers"))
import build_deck  # noqa: E402
import gate_runner  # noqa: E402

tmp = SKILL / "evals" / "_smoke_out"
tmp.mkdir(exist_ok=True)
ledger = tmp / "source_ledger.csv"
plan_p = tmp / "content_plan.json"
out = tmp / "Smoke_IL_Briefing.pptx"

COLS = ["claim_id", "slide", "claim", "source_url", "source_tier",
        "figure_or_quote_at_source", "source_pub_date", "retrieved_date",
        "confidence_band", "binding_test", "verified"]
rows = []
for i in range(1, 9):
    rows.append({"claim_id": f"C{i}", "slide": "2", "claim": f"claim {i}",
                 "source_url": f"https://example.com/{i}", "source_tier": "1",
                 "figure_or_quote_at_source": f"fig {i}", "source_pub_date": "2026-01-01",
                 "retrieved_date": "2026-06-06", "confidence_band": "High",
                 "binding_test": "tier", "verified": "yes"})
with open(ledger, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLS); w.writeheader(); w.writerows(rows)


def cell(kind, cids=None, **kw):
    c = {"kind": kind}; c.update(kw)
    if cids is not None:
        c["claim_ids"] = cids; c["confidence"] = "High"
    return c


def row(*cells, weight=1.0):
    return {"weight": weight, "cells": list(cells)}


def scene(no, tone, eyebrow, headline, hcids, body, lead=None, footer=None):
    s = {"slide_no": no, "kind": "scene", "tone": tone, "eyebrow": eyebrow,
         "headline": headline, "claim_ids": hcids, "confidence": "High", "scene": body}
    if lead:
        s["lead"] = lead
    if footer:
        s["footer"] = footer
    return s


plan = {
 "deck_meta": {"target": "Acme Corp", "date": "6 June 2026", "prepared_by": "CBRE I&L",
               "subtitle": "Industrial & Logistics Account Brief | as at 2026"},
 "slides": [
  {"slide_no": 1, "kind": "cover", "tone": "dark",
   "subtitle": "Industrial & Logistics Account Brief",
   "contents": ["Why now", "The company", "The network", "What it means"]},
  # prose + stat row
  scene(2, "dark", "01 | WHY NOW", "Acme is consolidating, not expanding", ["C1", "C2"],
    [row(cell("prose", cids=["C1", "C2"], label="THE SITUATION",
              text="Acme is mid-transformation: it is consolidating its European network into "
                   "fewer, larger nodes and releasing surplus industrial assets, so near-term "
                   "demand from Acme itself is shrinking rather than growing across the region."),
         weight=1.3),
     row(cell("stat", cids=["C1"], value="EUR 17.8bn", label="FY2025 sales"),
         cell("stat", cids=["C2"], value="23", label="sites in 11 countries"),
         cell("stat", cids=["C3"], value="3.8 yr", label="weighted lease term"),
         weight=0.8)]),
  # divider
  {"slide_no": "A", "kind": "divider", "tone": "dark", "number": 1,
   "title": "How the company works", "lead": "Regionalisation shapes the footprint.",
   "items": ["Strategy", "Supply chain", "Network"]},
  # table (last column is the analytical read)
  scene(3, "light", "02 | NETWORK", "A compact European network", ["C4"],
    [row(cell("table", cids=["C4", "C5"],
              headers=["Region", "Site", "What", "I&L read"],
              rows=[["NL", "Best", "Imaging", "Flagship, sticky"],
                    ["DE", "Hamburg", "Tubes", "Centre of excellence"],
                    ["US", "Reedsville", "Ultrasound", "Reshoring"]],
              aligns=["left", "left", "left", "left"]), weight=1.0)],
    lead="Two currents: reshoring and contraction."),
  # list + panel
  scene(4, "dark", "03 | OPERATING MODEL", "Make in-house, move via third parties", ["C6"],
    [row(cell("list", cids=["C6"], numbered=True,
              items=[{"title": "Make", "text": "Regulated in-house manufacturing across many sites."},
                     {"title": "Move", "text": "Distribution outsourced to 3PLs who hold the leases."},
                     {"title": "Rebalance", "text": "Rebalanced region by region as volumes shift."}]),
         cell("panel", cids=["C7", "C8"], title="THE I&L LENS",
              items=[{"label": "Tenure", "value": "Owned core; small lease book"},
                     {"label": "Governance", "value": "Reports to the CFO; EMEA team"}]),
         weight=1.0)]),
  # heading + rule + quote
  scene(5, "light", "04 | VOICE", "What leadership says", ["C1"],
    [row(cell("heading", text="ON THE RECORD"), weight=0.2),
     row(cell("rule"), weight=0.05),
     row(cell("quote", cids=["C2"], text="We are consolidating to fewer, larger nodes.",
              attrib="CFO, FY2025 call"), weight=1.0)]),
  {"slide_no": "ref", "kind": "references", "tone": "light"},
 ],
}
plan_p.write_text(json.dumps(plan, indent=2), encoding="utf-8")

schema = str(SKILL / "templates" / "content_plan.schema.json")
bd = str(SKILL / "helpers" / "build_deck.py")


def show(name, defects):
    print(f"{name:14}:", "PASS" if not defects else f"FAIL {defects}")


print("building (no PowerPoint: resolve + label + bake off)...")
build_deck.build_deck(str(plan_p), str(out), str(ledger), resolve=False, label_and_bake=False)
from pptx import Presentation  # noqa: E402
print(f"OK: rendered {len(Presentation(str(out)).slides)} slides -> {out}")

# The build must emit deck_text.txt beside the pptx: the post-build text gates
# (reconcile / qa4 / G6b) and the Final Gate all consume it.
deck_text = tmp / "deck_text.txt"
assert deck_text.exists(), "build_deck must emit deck_text.txt next to the pptx"
print(f"OK: deck_text.txt emitted ({len(deck_text.read_text(encoding='utf-8').splitlines())} lines)")

print("\n-- happy path (all should PASS) --")
# The fixture is a small code-path test (a few slides, not a full deck), so filter
# the expected minItems complaint; everything else must be clean.
vp = [d for d in gate_runner.validate_plan(str(plan_p), schema)
      if "too short" not in d and "schema requires >=" not in d]
show("validate-plan", vp)
show("self-check", gate_runner.self_check(schema, bd))
show("qa1", gate_runner.qa1(str(plan_p), str(ledger)))
show("qa2", gate_runner.qa2(str(plan_p)))
show("density", gate_runner.density(str(plan_p)))
show("reconcile", gate_runner.reconcile(str(plan_p), str(deck_text), str(ledger)))
show("qa4", gate_runner.qa4(str(deck_text)))

print("\n-- negative fixtures (the gate must bite) --")
# (a) blank analytical-read last cell on a table row
bad = json.loads(plan_p.read_text(encoding="utf-8"))
for s in bad["slides"]:
    for r in s.get("scene", []) or []:
        for c in r["cells"]:
            if c.get("kind") == "table":
                c["rows"][0][-1] = ""  # empty the read cell
badp = tmp / "bad_density.json"; badp.write_text(json.dumps(bad), encoding="utf-8")
d = gate_runner.density(str(badp)); print("density catches empty read cell  :", "YES" if d else "NO (BUG)")
# (b) evaluative prose cell with no Claim ID
bad2 = json.loads(plan_p.read_text(encoding="utf-8"))
for s in bad2["slides"]:
    for r in s.get("scene", []) or []:
        for c in r["cells"]:
            if c.get("kind") == "prose":
                c.pop("claim_ids", None)
badp2 = tmp / "bad_qa2.json"; badp2.write_text(json.dumps(bad2), encoding="utf-8")
q = gate_runner.qa2(str(badp2)); print("qa2 catches unsourced prose      :", "YES" if q else "NO (BUG)")
# (c) reviewer verdict files missing
r = gate_runner.reviews(str(tmp.parent), "1"); print("reviews catches missing verdicts :", "YES" if r else "NO (BUG)")
# (d) a fabricated number on the deck that is not in the plan (single digit too)
badtext = deck_text.read_text(encoding="utf-8") + "\nA new unsourced line claiming 7 mega-sites opened.\n"
badtxt_p = tmp / "bad_deck_text.txt"; badtxt_p.write_text(badtext, encoding="utf-8")
rc = gate_runner.reconcile(str(plan_p), str(badtxt_p), str(ledger))
print("reconcile catches new number     :", "YES" if any("'7'" in x for x in rc) else "NO (BUG)")
