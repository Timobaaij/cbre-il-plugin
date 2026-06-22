# Worked example - happy path end to end (v6 intelligence brief)

A bar-setter showing the shape of a clean run. Illustrative company "Northwind Industrial" (a fictional European manufacturer); numbers are placeholders, not real research.

## Stage 0 - Orchestrator
Variables validated to `variables.yaml`: company, today's date, type MANUFACTURER, geographic focus Europe, trigger, meeting context "first meeting with the Group Head of Real Estate". Research plan written.

## Stage 1 - Five parallel research sub-agents
Each writes `R{n}_*.findings.md` + `*.sources.csv`. R1 financials and leases (IFRS 16 liability, WALT, any S&LB); R2 network and the operating model (sites, 3PLs, who holds the lease); R3 strategy, recent movements, challenges, competitors; R4 stakeholders and any incumbent advisor; R5 home-language primary sources. Gaps returned explicitly.

## Stage 2 - Synthesis & Analysis
`ledger.py merge` builds `source_ledger.csv`. A trade-press "12 plants" loses to the annual report's "14"; both kept, resolution noted. The four analytical reads are written into `fact_base.md`: strategy-to-space, the supply-chain operating model, challenge-to-real-estate, and the competitive read. The forecast module stays off.

## Stage 2.5 - Narrative outline + G0 (independent)
`narrative_outline.md` written: deck thesis, the meeting's intelligence questions, each slide's one-sentence thesis with Claim IDs. G0 (isolated reviewer) returns AMBER: the supply-chain operating-model slide is under-developed and the S&LB programme is under-used. The orchestrator strengthens both in the outline before writing the plan.

## Stage 3 - Content plan
`content_plan.json` composed from the story per the outline: chapters led by prose explainers, the two transactions told as dedicated prose-led scenes, tables only for the network list and the recent-moves register. Prose explains; every table carries an analytical-read column; every scene leads with its so-what. No forecast fields (forecast module off).

## Stage 4 - Pre-build gate (independent where it is judgement)
- Mechanical: `gate_runner.py qa1` (integrity) and `qa2` (no evaluative claim unsourced) and `density` (scenes have content, analytical-read cells populated, prose full paragraphs) all pass.
- G1b (isolated): a facility-count claim resting on tier-5 trade press is re-traced to the annual report and re-cited; one unconfirmable claim is struck to the Meeting Brief.
- G2 (isolated): flags one recommendation stated as fact with no Claim ID; reworded.
- G4 content-substance (isolated senior strategist): scores the six dimensions, flags one HIGH ("slide 9 lists peers but draws no I&L read"); the orchestrator adds the read. Re-run with a fresh reviewer: clean.
`gate1_scorecard.md` records the fixes and ends `STATUS: ALL-PASS`. Plan frozen.

## Stage 5 - Build
`build_deck.py` renders the frozen plan to `%TEMP%` then copies to `deliverables/`; the dash sweep runs before save, the org sensitivity label is inherited and fit-to-text is baked into the file.

## Stage 6 - Post-build gate (independent where it is judgement)
- `reconcile` and `qa4` (dashes) and `density` pass.
- G7 visual-render (isolated Opus): renders all slides to PNG, confirms no overflow, contrast or whitespace defect.
- G8 red-team (isolated Opus): flags that no incumbent-advisor position is acknowledged; routed to the Meeting Brief as a "be ready for this" item.
`gate2_scorecard.md` ends `STATUS: ALL-PASS`.

## Stage 7 - Deliver
`ledger.py export` writes the Source Ledger `.xlsx`. The Meeting Brief is written, ordered for a Head of Real Estate meeting (lease, S&LB and RE-value items first). `final_gate.py <dir> --deck-text deck_text.txt` prints all green. Delivered: deck, Source Ledger, Meeting Brief.
