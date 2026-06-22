# OPTIONAL module: opportunity classification & forecast (OFF by default)

> This is the **optional forecast/opportunity module**. The default account brief does NOT use it: it carries no speculative forecast and no opportunity ladder, because a half-baked forecast is worse than an honest "we don't know, here is what to probe". Turn it on (`deck_meta.forecast_module: true`) only when a target genuinely supports a defensible, fully-sourced forecast and it passes the G3 gate. When off, opportunity elements carry no `classification`/`service_line`/`forecast_ref` and G2 flags any that do.

When the module is on, every opportunity element must be tagged exactly one of COMMITTED / PLANNED / FORECAST with a matching service line.

## The three classes
- **COMMITTED - site secured, publicly announced.** A named location/developer, planning submitted or construction started, a specific sqm and location both disclosed. The site has been found; the CBRE service is Project Management, Development Management, Facilities Management, sale-and-leaseback advisory (post-completion), BREEAM/sustainability advisory, or Valuation. **Never label an announced project as site sourcing or brokerage.**
- **PLANNED - announced intent, site possibly still in selection.** "We plan to open a DC in [region]" with no site named. Service: site sourcing, tenant representation, development advisory. Verify whether the site has since been secured (then it is COMMITTED).
- **FORECAST - not yet announced, derived from analysis.** No public announcement, but sourced growth math shows a future need. Service: proactive site sourcing, market intelligence, tenant representation.

## Service-line match table (G3 checks this)
| Stage | Valid | Invalid (auto-fail) |
|---|---|---|
| COMMITTED | Project Management, Development Management, Facilities Management, S&LB advisory (post-completion), BREEAM/sustainability advisory, Valuation | Site sourcing, Brokerage, Tenant representation (new site) |
| PLANNED | Site sourcing, Tenant representation, Development advisory | Project Management of the build, FM of a not-yet-built asset |
| FORECAST | Proactive site sourcing, Market intelligence, Tenant representation | Project Management, FM, any service implying a named site exists |

## Forecast decision tree (run via `helpers/forecasting.py`, write `forecasting_worklog.md`)
Save the sourced inputs you feed the helper to `intermediate/forecast_inputs.json` (the shape `forecasting.py` documents: one object or a list). The G3 Script half (`gate_runner.py qa3`) re-derives from that file and blocks on a missing file, an input with no `input_claim_ids`, any of the five anti-patterns, or an out-of-band ratio, so the worklog and the gate cannot disagree.
1. Identify company type. 2. Select the ratio (retail: stores per DC; manufacturer: capacity utilisation / capex / regional revenue; distributor: revenue per depot; e-commerce: online penetration). 3. Apply a region-specific growth rate, never a global average on a single market. 4. Compute when the threshold is breached and where. 5. Tag the CBRE opportunity. 6. Sanity-check against a sector benchmark band: a forecast that is internally consistent but outside the band is Low-confidence with the deviation noted, or sent back for an input error.

**Minimum bar:** every input sourced (a Claim ID each), visible math in the worklog, the sector band stated, and the output shown as a calculation, never stated as fact. If you cannot source the inputs, do not run it; flag the intel gap.

## The five forecasting anti-patterns (G3 checks each)
1. Do not apply a global growth rate to a single market. 2. Do not double-count a multi-function site. 3. Do not forecast a facility in a region the company is exiting. 4. Do not assume a 3PL-operated facility is a tenant-rep target (if the 3PL holds the lease, the company is not the target). 5. Do not project from revenue growth alone without checking whether the company is consolidating (fewer, larger) or densifying (more, smaller); the direction changes the forecast.
