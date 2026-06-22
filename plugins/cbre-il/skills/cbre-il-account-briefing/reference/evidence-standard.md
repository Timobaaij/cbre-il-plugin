# The Evidence Standard

This is the governing rule of the entire deck. It overrides convenience, speed, and completeness. Read it before anything else.

**Nothing reaches a slide that has not been checked against a real, retrievable source.** Every material claim, every number, every name, every facility, every opportunity tag must carry a source record.

A **source record** is:
- the exact URL,
- the source tier (1 to 6, per `source-hierarchy.md`),
- the exact figure or quote as it appears at the source,
- the source's own publication or as-of date,
- the date the source was retrieved,
- and a confidence rating (High, Medium, Low) set per the confidence rubric below.

Keep the publication date distinct from the retrieved date, because the recency test measures age from when the source was published or last current, not from when you fetched it. Where a source carries no date at all, treat that as a recency penalty, not a free pass. These records are collected as the deck is built and delivered as the Source Ledger.

## "No inferring", defined precisely

This deck does analysis, including forecasting future facility needs that have not been announced. That is not banned. What is banned is **presenting an estimate as a fact, and making a factual claim with no source behind it.**

The rule is: every *input* to an analysis must be a verified source, and every *output* of an analysis must be labelled as a derived estimate, never stated as fact. A FORECAST opportunity is allowed only when every number feeding the growth math is sourced and the conclusion is shown as the result of a calculation the reader can see. If you cannot source the inputs, you cannot run the forecast; flag it as an intel gap instead.

## The verification gate

A claim is not "sourced" because it carries a citation. A citation is a pointer. **Verifying a claim means tracing it to the highest source tier on which it should exist, not merely re-fetching whatever was cited.** Confirming that a number appears on the page that was cited is not enough, because that page may have copied the number from somewhere else, which makes a wrong number look verified.

So for any claim where a tier 1 to 2 primary source should exist (financials, facility counts, lease disclosures, stakeholder roles, announced projects), the Source Verification agent must trace the claim to that primary source and confirm the figure or quote actually appears there. A claim that survives only at tier 5 to 6 is flagged as **thin** even when technically confirmed. A claim that cannot be confirmed at any tier is **struck** from the slide and moved to the Meeting Brief as an unverified item.

## The confidence rubric

High, Medium, and Low are not a feel. **A claim's confidence is the lowest band any of the following four tests produce.** Record the band and the test that set it in the Source Ledger. (`helpers/confidence.py` computes this.)

1. **Source tier.** Tier 1-2 supports High; tier 3-4 supports Medium; tier 5-6 caps at Low.
2. **Recency.** Confidence decays with age, measured from the source's publication or as-of date, not the retrieval date, and decays faster for things that change.
   - A prior-year revenue figure stays High for a year.
   - A "current Head of Supply Chain", a live lease expiry, or a facility count whose source is more than twelve months old drops a band.
   - Anything that may have changed and has not been reconfirmed within its useful window drops to Low.
3. **Corroboration.** A single source caps at Medium; two independent sources that agree support High.
4. **Plausibility (forecasts only).** A derived figure whose ratio sits inside the sector benchmark band can hold its band; one that sits outside the band drops to Low and carries a note, no matter how clean the arithmetic.

## No fabrication, ever

If a number is not publicly available after thorough search, do not invent it, do not estimate it silently, do not pattern-match it from a comparable company. Apply the Data Gap Protocol.

## Conflicting Sources Protocol

Supply chain news frequently contains contradictory data (one source says 500,000 sqft, another says 50,000 sqm; one says "new DC", another describes a warehouse extension). When sources conflict:

- Flag both figures and their sources on the slide rather than silently choosing one.
- Prefer the higher-ranked source per the Source Priority Hierarchy.
- If the company's own filings contradict a news report, **the company filing wins.**
- Note the discrepancy in the Meeting Brief as something to clarify in early engagement, and record the resolution in `fact_base.md`. Keep the discarded figure visible in the ledger so the resolution is auditable.

## Data Gap Protocol

If data is unavailable after thorough search, do not fabricate, estimate, or infer numbers that are not sourced. Instead:

- On the slide, include a note such as "Not publicly disclosed; priority intel gap for first meeting."
- In the Meeting Brief, add a Phase 1 action to gather this missing data through relationship engagement.
- Add the gap to the Meeting Brief.
- Never present an estimate as a fact. If you derive a range from partial data, label it explicitly (e.g. "Estimated at 15 to 20 DCs based on [source and reasoning]") and record the reasoning in the Source Ledger.

This applies especially to: owned vs leased split, internal decision-maker names, lease lengths, BREEAM requirements, and 3PL contract details, which are rarely fully public.
