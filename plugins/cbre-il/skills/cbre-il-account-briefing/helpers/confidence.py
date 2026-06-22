"""Confidence rubric calculator for the CBRE I&L account briefing.

A claim's confidence is the LOWEST band any of four tests produce. This module
computes that floor and, crucially, names the test that set it, so the Source
Ledger can record both. Getting this wrong by hand is easy (models tend to
average or pick the modal band); the floor-not-average rule is the whole point.

Bands, ordered weakest to strongest: Low < Medium < High.

The four tests (see reference/evidence-standard.md):
  1. source tier      tier 1-2 -> High, 3-4 -> Medium, 5-6 -> Low
  2. recency          decays from the source's publication/as-of date, faster
                      for volatile facts; undated is penalised
  3. corroboration    1 source -> Medium cap, 2+ independent agreeing -> High
  4. plausibility     forecasts only: inside sector band holds, outside -> Low

CLI:
  python confidence.py --tier 2 --pub-date 2024-09-30 --today 2026-05-29 \
      --volatile false --sources 2 --kind fact
  python confidence.py --tier 2 --pub-date 2023-01-01 --today 2026-05-29 \
      --volatile true --sources 1 --kind forecast --in-band false
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from typing import Optional

_ORDER = {"Low": 0, "Medium": 1, "High": 2}
_REV = {v: k for k, v in _ORDER.items()}


def _floor(*bands: str) -> str:
    return _REV[min(_ORDER[b] for b in bands)]


def tier_band(tier: int) -> str:
    if tier in (1, 2):
        return "High"
    if tier in (3, 4):
        return "Medium"
    return "Low"


def _months_between(pub: Optional[_dt.date], today: _dt.date) -> Optional[float]:
    if pub is None:
        return None
    return (today - pub).days / 30.44


def recency_band(pub_date: Optional[str], today: str, volatile: bool) -> str:
    """Recency test, returned as an independent band (the rubric then takes the
    floor across all four tests).

    This is the agreed concrete operationalisation of the spec's "confidence
    decays with age ... drops a band ... drops to Low" rule. Volatile facts
    (current role, live lease expiry, facility count) sit at High while fresh,
    drop one band once the source is older than 12 months, and fall to Low once
    well past their useful window. Stable facts (a prior-year revenue figure)
    hold High for a year, then decay more slowly. Undated sources are penalised,
    never given a free pass. Because confidence is the floor of the four tests,
    this band only ever lowers the result, matching "drops a band".
    """
    today_d = _dt.date.fromisoformat(today)
    pub_d = _dt.date.fromisoformat(pub_date) if pub_date and pub_date != "undated" else None
    age = _months_between(pub_d, today_d)
    if age is None:
        # Undated: penalise. Volatile undated is unusable as High/Medium.
        return "Low" if volatile else "Medium"
    if volatile:
        if age <= 12:
            return "High"
        if age <= 24:
            return "Medium"
        return "Low"
    # Stable facts
    if age <= 12:
        return "High"
    if age <= 36:
        return "Medium"
    return "Low"


def corroboration_band(n_independent_sources: int) -> str:
    return "High" if n_independent_sources >= 2 else "Medium"


def plausibility_band(in_band: Optional[bool]) -> str:
    """Forecasts only. None for non-forecast claims (test does not apply)."""
    if in_band is None:
        return "High"  # not applicable -> does not lower the floor
    return "High" if in_band else "Low"


def assess(tier: int, pub_date: Optional[str], today: str, volatile: bool,
           n_sources: int, kind: str = "fact",
           in_band: Optional[bool] = None) -> dict:
    """Return {'band', 'binding_test', 'tests': {...}}.

    kind: 'fact' or 'forecast'. For 'fact', the plausibility test does not apply.
    """
    tests = {
        "tier": tier_band(tier),
        "recency": recency_band(pub_date, today, volatile),
        "corroboration": corroboration_band(n_sources),
    }
    if kind == "forecast":
        tests["plausibility"] = plausibility_band(in_band)
    band = _floor(*tests.values())
    # The binding test is the weakest one, i.e. the test that actually SET the
    # band. On a TIE at the minimum band, name the most actionable cause first
    # (recency, corroboration, plausibility) ahead of the structural 'tier', so a
    # stale current-fact reports binding_test=recency rather than tier even when
    # both land at the same band. BUT when the band is High nothing lowered it,
    # so naming recency would falsely imply recency is the limiting factor; report
    # 'tier' (the source ceiling), which is what holds a clean claim at High.
    if band == "High":
        tie = {"tier": 0, "recency": 1, "corroboration": 2, "plausibility": 3}
    else:
        tie = {"recency": 0, "corroboration": 1, "plausibility": 2, "tier": 3}
    binding = min((t for t in tests),
                  key=lambda t: (_ORDER[tests[t]], tie[t]))
    return {"band": band, "binding_test": binding, "tests": tests}


def _parse_bool(s: str) -> Optional[bool]:
    if s is None:
        return None
    s = s.strip().lower()
    if s in ("true", "yes", "y", "1"):
        return True
    if s in ("false", "no", "n", "0"):
        return False
    if s in ("none", "na", "n/a", ""):
        return None
    raise ValueError(f"not a bool: {s}")


def main() -> None:
    p = argparse.ArgumentParser(description="Confidence rubric calculator (floor of four tests).")
    p.add_argument("--tier", type=int, required=True)
    p.add_argument("--pub-date", default=None, help="ISO date or 'undated'")
    p.add_argument("--today", required=True, help="ISO date")
    p.add_argument("--volatile", default="false", help="does this fact change quickly?")
    p.add_argument("--sources", type=int, default=1, help="independent agreeing sources")
    p.add_argument("--kind", default="fact", choices=["fact", "forecast"])
    p.add_argument("--in-band", default="none", help="forecasts: result inside sector band?")
    a = p.parse_args()
    vol = _parse_bool(a.volatile)
    if vol is None:
        sys.stderr.write("WARNING: --volatile unset; defaulting to false (stable). "
                         "Pass true for facts that change quickly.\n")
        vol = False
    res = assess(a.tier, a.pub_date, a.today, vol, a.sources, a.kind, _parse_bool(a.in_band))
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
