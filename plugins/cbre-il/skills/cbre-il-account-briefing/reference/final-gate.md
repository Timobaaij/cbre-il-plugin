# The Final Gate (v6)

Owned by the Orchestrator (Stage 7). Do not deliver until both gate scorecards end `STATUS: ALL-PASS` and you can answer **yes** to all of the following. Run `helpers/final_gate.py <Company>_briefing/ --deck-text <Company>_briefing/deliverables/deck_text.txt` (the `deck_text.txt` that `build_deck.py` wrote next to the deck; regenerate with `build_deck.py --dump-text <pptx> deck_text.txt` if it is missing). It prints a green/red line for each mechanical check; the dash check (item 5) is red if `--deck-text` is not supplied. Any red line means surface it in writing and do not declare done.

1. Did the pre-build gate pass on the plan **before any slide was built** (G0 outline GREEN, G1-G4 all-pass, including the independent content-substance review with no open HIGH), and did the post-build gate (reconciliation, editorial, density, visual-render, red-team) confirm the rendered deck introduced no new claim and renders clean?
2. Has every claim been traced to the highest tier on which it should exist and confirmed there (G1b), with thin claims flagged, unconfirmed claims struck, and the Source Ledger complete?
3. Evidence and honesty (G2): is every evaluative line and recommendation backed by a Claim ID, every gap flagged not bluffed, and every incumbent and CBRE's actual standing acknowledged?
4. Density: does every table carry a populated analytical-read column, every scene a lead line, and is no slide left sparse (G6c mechanical + G7 visual)?
5. Does every slide read in full sentences, lead with the I&L "so what", and contain no em or en dashes (G6)?
6. Has the red-team run (G8), with every soft spot fixed or routed to the Meeting Brief?
7. Does every claim carry a confidence band set by the rubric, with role-currency and lease-event claims reconfirmed within their useful window?
8. Is every unverified or struck item on the Meeting Brief with an action?
9. If the optional forecast module was on, does every forecast show sourced inputs, visible math, sit inside its sector band, and carry no output stated as fact (G3)? (If off, this passes trivially.)

## Mechanical vs judgement
- **Mechanical (the script asserts):** both scorecards end `STATUS: ALL-PASS`; every plan claim has a complete verified ledger row; no evaluative claim is unsourced; analytical-read cells populated and prose cells are full paragraphs; zero em/en dashes; every ledger row has a band and binding test; the three persona slides and every required answer-contract item are present; every struck item is on the Meeting Brief; the three deliverables exist.
- **Judgement (the orchestrator confirms in writing on the scorecards, from the independent reviewers' verdicts):** the outline GREEN, the tier-tracing genuine, the substance review clean with no open HIGH, the visual render free of HIGH/MED defects, the red-team routing sound, and the Meeting Brief ordered by meeting context.

Both must be clean before Stage 7 delivers.
