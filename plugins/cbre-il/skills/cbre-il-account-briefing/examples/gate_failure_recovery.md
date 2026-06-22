# Gate failure and recovery (v6)

How the independent gates catch defects and how the orchestrator recovers, with independence preserved on re-runs. Illustrative, fictional company "Atlas Components".

## G0 (narrative outline) returns RED
The outline is a pile of facts with no through-line, and two slides restate the public profile. The isolated reviewer returns RED with concrete instructions: state a single thesis on slide 2, cut or merge the two boilerplate slides. The orchestrator rewrites the outline and re-dispatches **a fresh G0 reviewer** (never the one that failed it), which returns GREEN. Cost: a paragraph, not a rebuild. Recorded on `gate1_scorecard.md`, re-run count 1.

## G1b (source verification) strikes a claim
Draft slide 6 asserts "a new automated hub in Lyon", sourced only to an SEO listicle. The reviewer traces it: no tier 1-4 source confirms it and the FY report lists no Lyon site. It is **struck** (verified=no); the annual-report DC figure replaces it on the slide, and the struck item moves to the Meeting Brief: "Unconfirmed: reported Lyon hub. Probe: confirm whether a Lyon facility exists or is planned." `gate_runner.py qa1` re-run: clean.

## G4 (content substance) blocks on a HIGH
The senior-strategist reviewer finds slide 6 "lists facilities but draws no implication" (a HIGH: a slide that says nothing) and slide 9 restates a peer's press release. It returns concrete instructions: add the I&L read ("value concentrates in two owned plants, so the property exposure sits there") and sharpen slide 9 to the company's distinctive position. The orchestrator edits the plan lines; `density` confirms the I&L-read cells are populated; a **fresh** G4 reviewer re-scores with no open HIGH. The plan freezes only then.

## G7 (visual render) finds a layout defect
The rendered references slide runs into the footer band. The orchestrator fixes the renderer (paginate to columns), rebuilds, re-renders, and a fresh G7 reviewer confirms no HIGH/MED defect. This class of defect is invisible to the text gates; only the rendered-PNG check catches it.

## Optional forecast module (only if turned on): an anti-pattern (G3)
If the module were on and a slide forecast a new DC in a region the company is exiting, `forecasting.py` flags anti-pattern 3 and the independent G3 reviewer blocks it; the orchestrator removes it and records the discarded attempt with the reason in `forecasting_worklog.md`. By default the module is off and no forecast appears.

## The rules that keep recovery honest
- Every judgement re-run uses a **new** isolated reviewer with fresh context; the agent that raised a defect never confirms its own fix.
- Reviewers return verdicts and defect rows; they never edit the artefact. The orchestrator applies the fix.
- Loops are bounded (cap ~3). On continued failure the item is struck to the Meeting Brief or escalated to the user in writing. A pass criterion is never loosened to get through, and the re-run count is on the scorecard.
- These are pre-build wherever possible (G0, G1-G4 on the plan), so a fix costs a plan line, not a rebuild.
