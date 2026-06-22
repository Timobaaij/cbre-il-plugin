"""Forecasting Decision Tree numerics for the CBRE I&L account briefing.

Runs the growth math on SOURCED inputs, shows its working, holds the result
against a sector benchmark band, and flags the five forecasting anti-patterns.
The point is compute-then-narrate: this writes the working to a worklog so the
deck shows the calculation, not just the conclusion, and QA3 can re-run it.

A forecast that is internally consistent can still be absurd. The sector band is
the sanity gate: 71 stores per DC when the norm is 25-40 is wrong even if the
arithmetic checks.

CLI:
  python forecasting.py --json path/to/forecast_inputs.json
  python forecasting.py --demo   # prints a worked example

Input JSON shape (one forecast):
  {
    "key": "uk_dc_2027",
    "company_type": "retailer",
    "ratio_name": "stores per DC",
    "current_units": 1180,        # e.g. stores
    "current_facilities": 14,     # e.g. DCs
    "growth_rate_pct": 6.0,       # region-specific, sourced
    "horizon_years": 3,
    "region": "UK",
    "sector_band": [25, 40],      # the norm for ratio_name
    "input_claim_ids": ["R2-014", "R2-021", "R3-009"],
    "growth_rate_basis": "region",  # 'region' (required) or 'global' (anti-pattern 1)
    "exiting_regions": [],        # for anti-pattern 3
    "operator": "owned",          # 'owned' or '3pl' (anti-pattern 4)
    "revenue_driven": false,      # is the ratio driven by revenue growth? (anti-pattern 5)
    "direction": "densifying",    # 'consolidating' | 'densifying' (anti-pattern 5)
    "double_counted": false       # is a multi-function site counted twice? (anti-pattern 2)
  }

Anti-patterns 1, 2, and 5 depend on the analyst declaring the relevant input
field (growth_rate_basis, double_counted, revenue_driven). QA3 must set these
when re-running the forecast; the worklog records each one so "the check was
skipped" is visible. The five anti-patterns themselves are defined verbatim in
reference/opportunity-classification.md (the optional forecast module; this
helper runs only when that module is turned on).
"""
from __future__ import annotations

import argparse
import json
from typing import List, Optional


def compute_ratio(units: float, facilities: float) -> Optional[float]:
    if not facilities:
        return None
    return units / facilities


def project_units(current_units: float, growth_rate_pct: float, years: int) -> float:
    return current_units * ((1 + growth_rate_pct / 100.0) ** years)


def facilities_needed(projected_units: float, target_ratio: float) -> float:
    if not target_ratio:
        return float("nan")
    return projected_units / target_ratio


def check_anti_patterns(fc: dict) -> List[str]:
    """Return a list of anti-pattern violations (empty = clean)."""
    flags: List[str] = []
    # 1. Global rate on a single market.
    if fc.get("growth_rate_basis") == "global" and fc.get("region", "").lower() not in ("global", ""):
        flags.append("anti-pattern 1: a global growth rate is applied to a single market "
                     f"({fc.get('region')}); use region-specific data")
    # 3. New facility in an exiting region.
    if fc.get("region") in (fc.get("exiting_regions") or []):
        flags.append(f"anti-pattern 3: forecasts a facility in {fc.get('region')}, "
                     "a region the company is exiting")
    # 4. 3PL-held lease is not a tenant-rep target.
    if str(fc.get("operator", "")).lower() == "3pl":
        flags.append("anti-pattern 4: facility is 3PL-operated; if the 3PL holds the lease the "
                     "company is not the tenant-rep target, so the opportunity differs")
    # 5. Revenue growth alone without consolidate/densify direction.
    name = fc.get("ratio_name", "").lower()
    revenue_driven = bool(fc.get("revenue_driven")) or name.startswith("revenue") or "revenue" in name
    if revenue_driven and not fc.get("direction"):
        flags.append("anti-pattern 5: projecting from revenue growth without stating whether the "
                     "company is consolidating or densifying; the direction changes the forecast")
    # 2. Double-count (declared by the caller when a site is multi-function).
    if fc.get("double_counted"):
        flags.append("anti-pattern 2: a multi-function site is being counted as more than one "
                     "opportunity")
    return flags


def run_forecast(fc: dict) -> dict:
    cur_ratio = compute_ratio(fc["current_units"], fc["current_facilities"])
    band = fc.get("sector_band")
    in_band = None
    if band and cur_ratio is not None:
        in_band = band[0] <= cur_ratio <= band[1]
    # If current ratio is outside the band, the gap to the band edge drives need.
    target_ratio = None
    if band:
        # Pull toward the nearer band edge if currently outside; else hold current.
        if cur_ratio is None:
            target_ratio = sum(band) / 2
        elif cur_ratio > band[1]:
            target_ratio = band[1]
        elif cur_ratio < band[0]:
            target_ratio = band[0]
        else:
            target_ratio = cur_ratio
    else:
        target_ratio = cur_ratio

    projected = project_units(fc["current_units"], fc["growth_rate_pct"], fc["horizon_years"])
    needed = facilities_needed(projected, target_ratio) if target_ratio else float("nan")
    additional = needed - fc["current_facilities"] if needed == needed else float("nan")
    anti = check_anti_patterns(fc)

    return {
        "key": fc.get("key"),
        "region": fc.get("region"),
        "ratio_name": fc.get("ratio_name"),
        "current_ratio": round(cur_ratio, 1) if cur_ratio is not None else None,
        "sector_band": band,
        "current_ratio_in_band": in_band,
        "target_ratio": round(target_ratio, 1) if target_ratio else None,
        "projected_units": round(projected, 0),
        "facilities_needed": round(needed, 1) if needed == needed else None,
        "additional_facilities": round(additional, 1) if additional == additional else None,
        "input_claim_ids": fc.get("input_claim_ids", []),
        "anti_pattern_flags": anti,
        # The forecast is publishable as-is only if the current ratio sits inside
        # the band; otherwise it carries Low confidence with the deviation noted.
        "plausibility_in_band": in_band,
    }


def worklog_text(res: dict, fc: dict) -> str:
    lines = []
    lines.append(f"### Forecast: {res['key']}  ({res['region']})")
    lines.append("")
    lines.append(f"- Ratio used: {res['ratio_name']}")
    lines.append(f"- Inputs (sourced): {', '.join(res['input_claim_ids']) or 'NONE — cannot run, flag as intel gap'}")
    lines.append(f"- Current ratio: {fc['current_units']} / {fc['current_facilities']} = {res['current_ratio']}")
    lines.append(f"- Sector benchmark band: {res['sector_band']}  -> current ratio in band? {res['current_ratio_in_band']}")
    lines.append(f"- Growth rate applied: {fc['growth_rate_pct']}% per year over {fc['horizon_years']} years (region-specific)")
    lines.append(f"- Projected units in {fc['horizon_years']}y: {res['projected_units']}")
    lines.append(f"- Target ratio: {res['target_ratio']}")
    lines.append(f"- Facilities needed: {res['facilities_needed']}  ->  additional vs today: {res['additional_facilities']}")
    lines.append(f"- Anti-pattern inputs declared: growth_rate_basis={fc.get('growth_rate_basis','UNSET')}, "
                 f"operator={fc.get('operator','UNSET')}, revenue_driven={fc.get('revenue_driven', False)}, "
                 f"direction={fc.get('direction','UNSET')}, exiting_regions={fc.get('exiting_regions', [])}, "
                 f"double_counted={fc.get('double_counted', False)}")
    if res["anti_pattern_flags"]:
        lines.append("- ANTI-PATTERN FLAGS:")
        for f in res["anti_pattern_flags"]:
            lines.append(f"    * {f}")
    else:
        lines.append("- Anti-pattern check: clean (none of the five present, with the inputs above declared)")
    if res["plausibility_in_band"] is False:
        lines.append("- PLAUSIBILITY: current ratio is OUTSIDE the sector band. Either fix an input "
                     "error or publish at Low confidence with the deviation noted.")
    lines.append("")
    return "\n".join(lines)


_DEMO = {
    "key": "uk_dc_2027", "company_type": "retailer", "ratio_name": "stores per DC",
    "current_units": 1180, "current_facilities": 14, "growth_rate_pct": 6.0,
    "horizon_years": 3, "region": "UK", "sector_band": [25, 40],
    "input_claim_ids": ["R2-014", "R2-021", "R3-009"], "growth_rate_basis": "region",
    "exiting_regions": [], "operator": "owned", "revenue_driven": False,
    "direction": "densifying", "double_counted": False,
}


def main() -> None:
    p = argparse.ArgumentParser(description="Forecasting decision tree + sector-band + anti-patterns.")
    p.add_argument("--json", help="path to a forecast inputs json (single object or list)")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo or not a.json:
        forecasts = [_DEMO]
    else:
        data = json.loads(open(a.json, encoding="utf-8").read())
        forecasts = data if isinstance(data, list) else [data]
    for fc in forecasts:
        res = run_forecast(fc)
        print(worklog_text(res, fc))
        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
