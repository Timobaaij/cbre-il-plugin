"""The Final Gate for the CBRE I&L account-brief pipeline (v6).

Binary shippability checklist. Prints a green/red line per check. Any red line
means: surface it in writing and DO NOT declare done. Mechanical checks live
here; the judgement confirmations are recorded on the scorecards, and the
reviewer-verdict files (intermediate/reviews/*.md) prove the independent
reviewers actually ran.

Usage:
  python final_gate.py <Company>_briefing/ --deck-text path/to/deck_text.txt
                       [--ledger path/to/source_ledger.csv]

The ledger is resolved as: explicit --ledger, else intermediate/source_ledger.csv
(the canonical location written by ledger.py merge and read by every gate), else a
briefing-root source_ledger.csv (back-compat for older runs). No manual copy needed.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

import gate_runner

SKILL = Path(__file__).resolve().parent.parent
SCHEMA = SKILL / "templates" / "content_plan.schema.json"
BUILD_DECK = SKILL / "helpers" / "build_deck.py"

GREEN = "[PASS]"
RED = "[FAIL]"


def _scorecard_all_pass(path: Path) -> bool:
    if not path.exists():
        return False
    return re.search(r"(?im)^\s*STATUS:\s*ALL-?PASS\s*$", path.read_text(encoding="utf-8")) is not None


def _read_ledger(path: Path):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def run(dirpath: str, deck_text: str | None, ledger_arg: str | None = None) -> int:
    d = Path(dirpath)
    inter = d / "intermediate"
    plan = inter / "content_plan.json"
    worklog = inter / "forecasting_worklog.md"
    g1 = inter / "gate1_scorecard.md"
    g2 = inter / "gate2_scorecard.md"
    # Canonical ledger location is intermediate/source_ledger.csv (where merge writes
    # and every gate reads). Resolve: explicit --ledger > intermediate/ > briefing root
    # (the last is a back-compat fallback for older runs that copied it to the root).
    if ledger_arg:
        ledger = Path(ledger_arg)
    else:
        cand = inter / "source_ledger.csv"
        ledger = cand if cand.exists() else d / "source_ledger.csv"
    deliv = d / "deliverables"

    results: list[tuple[str, bool, str]] = []

    def add(q, ok, note=""):
        results.append((q, ok, note))

    # 1. Both scorecards ALL-PASS AND the independent reviewers produced verdict files.
    g1_ok, g2_ok = _scorecard_all_pass(g1), _scorecard_all_pass(g2)
    rev1 = gate_runner.reviews(str(d), "1") if plan.exists() else ["plan missing"]
    rev2 = gate_runner.reviews(str(d), "2")
    add("1. Both gate scorecards ALL-PASS and every independent reviewer left a verdict file",
        g1_ok and g2_ok and not rev1 and not rev2,
        "" if (g1_ok and g2_ok and not rev1 and not rev2)
        else f"scorecards {'ok' if g1_ok and g2_ok else 'incomplete'}; "
             f"{len(rev1)+len(rev2)} reviewer verdict files missing/empty")

    # 2. Plan is schema-valid and the docs/code have not drifted.
    if plan.exists() and SCHEMA.exists():
        vp = gate_runner.validate_plan(str(plan), str(SCHEMA))
    else:
        vp = ["content_plan.json or schema missing"]
    sc = gate_runner.self_check(str(SCHEMA), str(BUILD_DECK)) if SCHEMA.exists() and BUILD_DECK.exists() else ["schema/build_deck missing"]
    add("2. Content plan is schema-valid and slide/cell kinds match the renderer",
        not vp and not sc, f"{len(vp)} schema + {len(sc)} drift defects" if (vp or sc) else "")

    qa1_def = gate_runner.qa1(str(plan), str(ledger)) if (plan.exists() and ledger.exists()) else ["plan/ledger missing"]
    add("3. Every plan claim has a complete, verified ledger row (G1a)",
        not qa1_def, f"{len(qa1_def)} defects" if qa1_def else "")

    qa2_def = gate_runner.qa2(str(plan)) if plan.exists() else ["plan missing"]
    add("4. Evidence and honesty: no evaluative claim unsourced (G2 mechanical)",
        not qa2_def, f"{len(qa2_def)} defects" if qa2_def else "")

    dens_def = gate_runner.density(str(plan)) if plan.exists() else ["plan missing"]
    add("5. Density: I&L-read columns populated, takeaways present, no sparse slide",
        not dens_def, f"{len(dens_def)} defects" if dens_def else "")

    env_def = gate_runner.envelope(str(plan)) if plan.exists() else ["plan missing"]
    add("5d. Envelope: no scene overflows its body region (plan-time fit backstop)",
        not env_def, f"{len(env_def)} slides overflow" if env_def else "")

    pers_def = gate_runner.personas(str(plan)) if plan.exists() else ["plan missing"]
    add("5b. Mandatory persona slides present (CEO / CSCO / Head of Real Estate)",
        not pers_def, f"{len(pers_def)} defects" if pers_def else "")

    spine_def = gate_runner.spine(str(plan)) if plan.exists() else ["plan missing"]
    add("5c. Answer contract present (BLUF, big movers, supply-chain signature, opportunity, etc.)",
        not spine_def, f"{len(spine_def)} defects" if spine_def else "")

    qa3_def = gate_runner.qa3(str(plan), str(worklog)) if plan.exists() else []
    add("6. Forecast module (if on) shows sourced math, in-band, not fact (G3)",
        not qa3_def, f"{len(qa3_def)} defects" if qa3_def else "(module off)")

    if deck_text and Path(deck_text).exists():
        qa4_def = gate_runner.qa4(deck_text)
        add("7. No em/en dashes in the deck (G6a)", not qa4_def, f"{len(qa4_def)} hits" if qa4_def else "")
    else:
        add("7. No em/en dashes in the deck (G6a)", False, "deck text not provided (--deck-text)")

    rows = _read_ledger(ledger)
    band_missing = [r.get("claim_id") for r in rows
                    if (r.get("verified") or "").lower() != "no"
                    and (not r.get("confidence_band") or not r.get("binding_test"))]
    add("8. Every claim carries a confidence band and binding test",
        not band_missing, f"{len(band_missing)} rows missing band/test" if band_missing else "")

    brief = next(iter(deliv.glob("*Meeting_Brief*.md")), None) if deliv.exists() else None
    struck = [(r.get("claim_id") or "").strip() for r in rows if (r.get("verified") or "").lower() == "no"]
    if brief and brief.exists():
        btext = brief.read_text(encoding="utf-8")
        missing = [c for c in struck if c and c not in btext]
        add("9. Every struck/unverified item appears on the Meeting Brief",
            not missing, f"{len(missing)} struck claims not on the sheet" if missing else "")
    else:
        add("9. Every struck/unverified item appears on the Meeting Brief", False, "Meeting Brief not found")

    pptx = next(iter(deliv.glob("*.pptx")), None) if deliv.exists() else None
    xlsx = next(iter(deliv.glob("*Source_Ledger.*")), None) if deliv.exists() else None
    deliverables_ok = bool(pptx and xlsx and brief)

    print("=" * 72)
    print("FINAL GATE")
    print("=" * 72)
    all_ok = True
    for q, ok, note in results:
        line = f"{GREEN if ok else RED}  {q}"
        if note:
            line += f"   ({note})"
        print(line)
        all_ok = all_ok and ok
    print("-" * 72)
    print(f"{GREEN if deliverables_ok else RED}  Three deliverables present (deck / ledger.xlsx / Meeting Brief)")
    all_ok = all_ok and deliverables_ok
    print("=" * 72)
    if all_ok:
        print("ALL GREEN - clear to deliver.")
        return 0
    print("RED LINES PRESENT - do not declare done. Surface these in writing.")
    return 1


def main() -> None:
    p = argparse.ArgumentParser(description="Run the Final Gate (v6).")
    p.add_argument("dir")
    p.add_argument("--deck-text", default=None)
    p.add_argument("--ledger", default=None,
                   help="path to source_ledger.csv (default: intermediate/, then briefing root)")
    a = p.parse_args()
    sys.exit(run(a.dir, a.deck_text, a.ledger))


if __name__ == "__main__":
    main()
