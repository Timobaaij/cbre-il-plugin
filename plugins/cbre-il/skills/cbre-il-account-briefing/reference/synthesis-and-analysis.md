# Synthesis & Analysis (Stage 2)

Synthesis turns five agents' findings into one fact base and the **analytical reads** the brief is built on. It is the reasoning hinge: the brief's quality is decided here, not in the renderer. Do not build slides from this output; hand it to the narrative outline (Stage 2.5) and the content plan (Stage 3).

**Output language.** Write the analytical reads (and from here on, the narrative outline and every authored slide) in `deck_meta.language` (default English; see `content-and-tone.md`). The `fact_base.md` may stay in English as internal scaffolding, but keep each sourced figure/quote verbatim in its source language (it flows to the ledger `figure_or_quote_at_source` untranslated).

## Step 1 - Deduplicate and resolve conflicts
- Read all five `*.findings.md` and `*.sources.csv`.
- Deduplicate claims; keep the highest-tier source for each.
- Resolve conflicts (Conflicting Sources Protocol in `evidence-standard.md`): flag both figures, prefer the higher-ranked source, **company filing beats news report**. Record every resolution in `fact_base.md`; keep the discarded figure visible in the ledger.
- Run `helpers/ledger.py merge` to build the canonical `source_ledger.csv` with stable Claim IDs.

## Step 2 - Build the single fact base
Write `fact_base.md`: the deduped, conflict-resolved facts, each tied to its Claim ID, grouped so the brief can draw from it (company shape; financials and leases; manufacturing and network; supply-chain operating model; strategy and corporate actions; challenges; stakeholders; recent movements; competitive). Flag every gap explicitly.

## Step 3 - Write the analytical reads (the core of the brief)
This is what makes the brief tell the reader something. For each, write a short, sourced interpretation into `fact_base.md` (these become the narrative prose, the slide takeaways and the analytical-read columns). The brief LEADS WITH THE COMPANY and explains it in prose, so write the company reads FIRST, then the supply-chain and real-estate reads. Each read maps to an answer-contract id (in brackets) that the deck must then carry (`reference/deck-structure.md`).

A. **Company and strategic profile.** In a few sentences, who this business is: what it sells and to whom, the growth model, the stated strategy and the 3 to 5 priorities, the competitive position (where it leads vs is a challenger), and the major pivots of the last 2 to 3 years. This anchors the company chapters and the brief's "what's true" up front. (`company-profile`, `strategy-priorities`)
B. **Financial trajectory.** Read the multi-year table, not single figures: the direction of revenue (growing/flat/contracting), the margin path, the capital intensity (capex trend), and the leverage trend. State what the trajectory implies (turnaround in progress, disciplined cash generator, over-levered and rationalising, etc.). This drives the financial story and KPI strip. (`financial-story`)
C. **The big movers (what is really going on).** Stand back from the individual events and name the two or three vectors actually reshaping the company over the planning horizon: M&A, divestiture or carve-out, reshoring / nearshoring / regionalisation, channel shift, a large committed capex or automation programme, cost-driven rationalisation, an ESG / net-zero commitment. For EACH, state the direction it pushes logistics and industrial demand: created, destroyed, or transferred (and from where to where, or from owner to 3PL). This is the synthesis the executive read (`bluf`) leads on and the dedicated event scenes then expand. (`big-movers`, feeds `bluf`)

1. **Strategy to space.** Take each strategic pillar and the company's targets and state the physical-footprint consequence (expansion, consolidation, regionalisation, reuse, retrofit). Lead with where logistics/industrial demand is being created or destroyed. (feeds `strategy-priorities`, `challenge-to-real-estate`)
2. **Supply-chain signature.** What is structurally distinctive about THIS company's supply chain: the two to four product and demand characteristics that dominate (seasonality, SKU count and range churn, value density and cube, temperature / shelf-life, service proposition, channel mix, returns intensity, import profile), the archetype they add up to, the consequence for the network and the building spec, and how CBRE should therefore approach the conversation. Read it against the archetype, because a highly seasonal, high-SKU business needs a different set-up than a fast-fashion player or an omnichannel grocer. Use `reference/supply-chain-signatures.md`. This is the baseline physics, distinct from the big movers (the deltas) and the operating model (how they run it). (`supply-chain-signature`)
3. **How the supply chain works (operating model).** Make / move / rebalance: what is manufactured in-house and where, what is outsourced, who holds which lease (company vs 3PL), and how the network is being rebalanced. This is the slide a naive brief omits. (`operating-model`)
4. **Challenge to real estate.** For each material challenge or pressure, state the real-estate consequence honestly (surplus, rationalisation, frozen capacity, retrofit, capital release). (`challenge-to-real-estate`)
5. **Competitive read.** Triangulate at least two independent peer views and state the company's distinctive position; do not let the core thesis rest on a single source. (`competitive-position`)
6. **Opportunity intersection.** Pull the demand signals together: across the strategy, the big movers, the signature and the challenges, where is logistics or industrial demand being created, destroyed or transferred, and what specific, sourced fact evidences each. Name the incumbent advisor where there is one and CBRE's actual standing. This is an evidence-bound synthesis of facts already in the brief, NOT the speculative forecast module (off by default) and NOT a generic pitch: every angle ties to a Claim ID, and an honest "not yet known, here is what to probe" is preferred to a stretch. (`opportunity-intersection`, feeds `what-to-probe`)

Every analytical read must be traceable to sourced facts. An interpretation is allowed; an unsourced assertion is not. Where the evidence is thin, say so.

## Step 4 - Quantify only what is sourced; the forecast is OPTIONAL and OFF by default
Quantify the present (estate size, lease book, maturity, owned-vs-leased where disclosed) from sourced figures, and label any derived figure as derived.

A forward, unannounced **forecast is an optional module, off by default.** Turn it on (`deck_meta.forecast_module: true`) only when every growth input is sourced AND the result sits inside a sector benchmark band; then run `helpers/forecasting.py`, write `forecasting_worklog.md`, and tag opportunity elements per `opportunity-classification.md`, which the forecast gate (G3) then checks. If you cannot source the inputs, do not run it; flag the intel gap instead. **Never present a forecast as a fact, and never pad the brief with a speculative one** - the default brief carries none, because a half-baked forecast is worse than an honest "we don't know, here is what to probe".

## Step 5 - Gaps
Flag every gap explicitly; these feed the "what we don't know / what to probe" slide and the Meeting Brief. An honest gap, phrased as an opening question, is more useful than a guess.
