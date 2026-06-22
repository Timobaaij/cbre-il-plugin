# Agent Architecture (v6 - independent, shift-left)

The pipeline runs in eight stages. The governing principles are **separation of author and reviewer** (judgement checks run as isolated sub-agents with fresh context) and **shift-left** (the story and substance are reviewed before any slide is built). Research and review agents are dispatched as real parallel sub-agents in Cowork or Code; in plain chat they run as sequential passes.

## Who does what

- **Orchestrator (this thread).** Owns the research plan, the single Source Ledger, conflict adjudication at synthesis, the narrative outline and content plan, the deterministic gate scripts, adjudication of every independent reviewer's verdict (fix / strike / deviate-with-reason), the build, and assembly. It **authors** the plan, so it never **certifies** a judgement review of that plan.
- **Research sub-agents R1-R5.** Parallel, single-slice, fresh context. Emit findings + `*.sources.csv`; never edit the ledger.
- **Independent reviewers (isolated sub-agents, fresh context).** G0 outline, G1b source verification, G2 evidence & honesty, G4 content substance, G6b editorial, G7 visual render, G8 red-team. Each returns a verdict and defect rows; **none edits the artefact**. On a non-English run (`deck_meta.language`), dispatch G0/G2/G4/G6b/G8 to judge the prose **in that language**; G1b and G7 are language-agnostic (see `gates.md` §Language).

## Model and effort assignment

Spend the most where a wrong answer compounds across the deck or the next twelve months of team activity; economise on retrieval and mechanical checks.

| Agent / reviewer | Model | Effort | Why |
|---|---|---|---|
| Orchestrator | Opus | High | Research plan, conflict adjudication, ledger ownership, assembly. |
| R1 Financials & Filings | Opus | High | The multi-year financial table (revenue, growth, margin, capex, net debt/leverage), revenue by geography, IFRS 16 lease extraction, S&LB signal reading. Number precision is load-bearing for the financial-performance slide. |
| R2 Network & Facilities | Opus | High | Facility facts and the operating-model evidence that anchor Acts III-IV. |
| R3 Strategy & Corporate Actions | Opus | High | Carries the whole company profile now: mission/vision, the 3-5 strategic priorities, growth model and pivots, business model and channels, pricing position, competitive landscape (lead vs challenger, recent moves), plus M&A, company-wide challenges and recent movements. The added Act II load justifies High. |
| R4 Stakeholders & CBRE Relationship | Sonnet | Medium | Name/role finding plus the corporate structure (focus-region HQ/legal entity, subsidiaries, sub-regions, regional headcount); role-currency justifies Medium. |
| R5 Local-Language & Primary Source | Opus | Medium | Multilingual primary-source reading; Sonnet acceptable if cost is tight. |
| Synthesis & Analysis | Opus | High | Conflict resolution, the fact base, the analytical reads. |
| Narrative outline | Opus | High | Decides the thesis and the storyline; cheapest place to be right. |
| **G0 outline review** | Opus | High | Storyline quality; the cheapest save in the pipeline. |
| **G1b source verification** | Opus | Medium | Tier-authority judgement; volume-bound, so Medium. |
| **G2 evidence & honesty** | Opus | High | No recommendation stated as fact; incumbents acknowledged. |
| **G4 content substance** | Opus | High | The senior-strategist read; the credibility-with-MDs check. |
| **G6b editorial** | Sonnet | Low | Sentence quality, lead-with-insight, register. |
| **G7 visual render** | Opus | High | Layout and whitespace judgement on rendered pixels. |
| **G8 red-team / pre-mortem** | Opus | High | Adversarial reasoning; the hardest task in the pipeline. |

Never step down G2, G4, G7 or G8. If cost must be cut, step R5 to Sonnet and G6b to Haiku first.

## Stage detail

**Stage 0-1** as in `SKILL.md`. Dispatch notes for a research sub-agent: give it (1) the company and variables, (2) its remit, (3) its question slice, (4) the output contract (`templates/findings_schema.md`), (5) its exact output paths. Tell it to fetch the IR page first and return explicit gaps. It must not edit the ledger.

**Stage 2 Synthesis & Analysis** - `reference/synthesis-and-analysis.md`.

**Stage 2.5 Narrative outline + G0.** The orchestrator writes `narrative_outline.md`, which **composes the deck from the story**: the thesis, the meeting's intelligence questions, the chapter breakdown, and each slide's one-sentence thesis and intended layout with Claim IDs (which events become dedicated prose-led scenes, how many slides each chapter earns). Dispatch G0 as an isolated reviewer: give it the outline and the fact base, tell it to judge storyline quality and whether the structure fits the story, and return GREEN/AMBER/RED with concrete per-slide instructions and any under-used or omitted fact. The orchestrator applies the fixes before Stage 3.

**Stage 3 Content plan** - `reference/content-plan-spec.md`.

**Stage 4 Pre-build gate.** Run the mechanical halves in-thread (`gate_runner.py qa1 / qa2 / density`). Dispatch the judgement reviewers as isolated sub-agents:
- G1b: give it the plan, the ledger, and web access; tell it to trace each claim to the highest tier on which it should exist, confirm the figure appears there, mark tier-5/6-only claims thin and unconfirmable claims struck.
- G2: give it the plan and ledger; tell it to flag any evaluative line or recommendation not backed by a Claim ID, any bluffed gap, and any place an incumbent or CBRE's actual standing is overstated.
- G4: give it the whole content plan; tell it to score the six substance dimensions and return per-slide `[OK]/[ISSUE HIGH/MED/LOW]` findings, each with a concrete instruction and a routing tag; any HIGH blocks the freeze.
The orchestrator adjudicates and re-dispatches the affected reviewer (fresh agent) until clean, then freezes.

**Stage 5 Build** - `helpers/build_deck.py`.

**Stage 6 Post-build gate.** Run reconciliation and the dash scripts in-thread **against `deck_text.txt`** (written by `build_deck.py` next to the `.pptx` on every build; regenerate with `build_deck.py --dump-text <pptx> deck_text.txt` if the deck was hand-edited), and the density script against the plan. Dispatch G6b (editorial, reads `deck_text.txt`), G7 (visual render, `reference/visual-qa.md` - render PNGs first, and hand the reviewer the `g7_index` table from `build_report.json` so it cites slides by deck position, never by the on-slide eyebrow), and G8 (red-team) as isolated sub-agents. For G8, give it the rendered deck, the plan and the ledger, and tell it to hunt over-claiming and omission only, not to re-verify cleared facts, returning a ranked list each routed to fix or to the Meeting Brief.

**Stage 7 Deliver** - `reference/deliverables-and-ledger.md` and `reference/final-gate.md`.

## Every reviewer writes a verdict file
Each independent reviewer (G0, G1b, G2, G4, G6b, G7, G8, and G3 if the forecast module is on) MUST write its verdict to `intermediate/reviews/<gate>.md` (a one-line verdict plus its per-slide/defect findings). The file MUST carry one explicit machine-read line, `VERDICT: <outcome>` (e.g. `VERDICT: GREEN`, `VERDICT: AMBER, slides 6 and 9 to strengthen`, `VERDICT: RED`, `VERDICT: clean, no open HIGH`, `VERDICT: BLOCKED, fix-required`), mirroring the scorecard `STATUS:` contract. This is not bookkeeping: `gate_runner.py reviews` and `final_gate.py` assert these files exist, are non-empty, and that the `VERDICT:` line is not a blocking outcome (`red` / `blocked` / `fix-required` / `reject`; a reviewer still holding an open HIGH records its line as `BLOCKED` or `fix-required`, never the bare phrase `open HIGH`, because `no open HIGH` is itself a clear and the check would otherwise invert it). So the gate cannot reach `STATUS: ALL-PASS` unless the reviewer actually ran AND its recorded bottom line is a clear: the orchestrator may not self-certify a pass over a reviewer that blocked. A re-run after a fix overwrites the file with the FRESH reviewer's verdict, so the latest line is always the current reviewer's word. The orchestrator pastes each verdict into the scorecard; the file is the proof of independence.

## Independence on re-runs (the subtle rule)
Every re-run of a judgement gate is a **new** isolated sub-agent with fresh context: the agent that raised a defect must not be the one that confirms the patch cleared it. Reviewers never edit; the orchestrator applies the fix and overwrites the verdict file with the fresh reviewer's verdict. Loops are bounded (cap ~3); on continued failure, strike to the Meeting Brief or escalate to the user in writing, never loosen a pass criterion.

## Plain-chat is a labelled DEGRADED mode
Genuine author/reviewer separation requires dispatching the reviewers as sub-agents (Cowork or Claude Code). In plain single-thread chat there is no second context, so the "independent reviewer" is the same model continuing the conversation: the verdict files still get written, but the independence guarantee is weaker. State this plainly to the user when running in plain chat; do not present it as fully independent. Prefer the sub-agent path whenever available.

## Cost discipline
A full run is reviewer-heavy (5 research agents + synthesis + 6-7 Opus reviewers). Default to the full profile. If cost must be cut, set `deck_meta.cost_profile: "lite"` and step down only R5 (to Sonnet) and G6b (to Haiku); **never** step down G2, G4, G7 or G8, which is the floor. The mechanical scripts run first and free, so judgement agents never burn tokens on a plan that fails a deterministic check. On re-runs, only the affected stage and its reviewer re-run (edit, do not rebuild).
