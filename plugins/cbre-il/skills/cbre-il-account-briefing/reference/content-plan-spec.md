# Content Plan Specification (Stage 3, v8 scene / story-led)

The content plan is what the pre-build gates inspect. It states, slide by slide, exactly what each slide says, with every factual or evaluative element tied to a ledger Claim ID. Catching a defect here costs one line; catching it after the build costs a rebuild.

It is preceded by `narrative_outline.md` (Stage 2.5), reviewed by **G0**, which decides the thesis, the chapters and the slide allocation **before** the detailed plan is written. The plan is written to `intermediate/content_plan.json`; the machine schema is `templates/content_plan.schema.json`. After the pre-build gate passes it is **frozen**; the build renders only what it contains.

## Structure
`deck_meta` plus an ordered `slides` array composed from the story per `deck-structure.md`: a minimal spine (cover, references) plus chapters whose layout each slide composes from its own content. Slide count flexes; the schema `minItems` guards against a degenerate plan.

`deck_meta`: `target`, `subtitle`, `audience`, `date`, `prepared_by`, `meeting_context`.

Each slide carries `slide_no`, `kind` (`cover` | `divider` | `references` | `scene`) and `tone` (`dark` | `light`). A `scene` slide also carries `eyebrow` (e.g. "03 | WHAT IS ON THE CEO'S MIND"), `headline` (the serif claim), an optional `lead` (the one-line so-what), an optional `footer` (source/as-of), `claim_ids` + `confidence` (sourcing the headline), an optional `answers` array (the answer-contract ids this slide lands, e.g. `["financial-story"]`; see `deck-structure.md`), and `scene` (the rows). A cell may also carry `answers` when one slide lands more than one answer in different cells. `cover` carries `subtitle` and `contents` (up to four); `divider` carries `number`/`title`/`lead`/`items`; `references` is generated from the ledger.

## The scene: rows and cells
`scene` is an ordered array of **rows**. Each row has a `weight` (vertical share, default 1) and a list of `cells`. Each cell has a `kind`, an optional `span` (horizontal share, default 1), the content fields for that kind, and `claim_ids` + `confidence` when it carries sourced content.

Cell content fields by kind:
- `prose` - `text` (the paragraph); optional `label` (a bold lead-label, e.g. "THE SITUATION", "WHY", "WHAT IT MEANS FOR US"); optional `max_size`.
- `stat` - `value` (the hero number or short phrase) + `label` (caption, unit in the label).
- `list` - `items` of {`title`, `text`}; `numbered` (bool).
- `table` - `headers`, `rows` (each an array of cell strings; the last column is the analytical read); optional `aligns`, `font_size`.
- `panel` - `title` + `items` of {`label`, `value`} (or a `text` body).
- `quote` - `text` + `attrib`.
- `heading` - `text`; optional `size`, `uppercase`.
- `rule` - no content.

`confidence` is the floor of the cited claims' bands (`helpers/confidence.py`).

## Rules
1. **Every sourced content cell cites at least one Claim ID and carries a confidence band.** `prose`, `stat`, `list`, `table`, `panel` and `quote` cells that carry content are claims, as is the scene `headline`. Structural-only text (cover/divider titles, a `heading`, a `rule`) may be unsourced.
2. **The analytical-read rule.** On every `table` the last column is the analytical read, and the last cell of every data row is non-empty (the density check enforces this). It is a read, never a restatement.
3. **The prose rule.** Every `prose` cell is a full explanatory paragraph (at least 60 characters, full sentences); a fragment fails the density check.
4. **The evaluative rule.** No evaluative cell (`prose`, `stat`, `quote`) states a claim without a Claim ID (`qa2`).
5. **The spine and the answer contract.** The deck carries a `cover` and a `references` slide (the density check asserts both), the three mandatory persona slides ("what is on the mind of the CEO / CSCO / Head of Real Estate", which share one family layout and sit at their act capstones, see `deck-structure.md`), AND every REQUIRED answer in the answer contract, each tagged on the substantive slide or cell that lands it via `answers`. `gate_runner.py personas` asserts the three personas; `gate_runner.py spine` asserts every required answer is carried; the Final Gate re-asserts both. This is a content floor only: slide count, order and layout stay composer-led.
6. **The ledger `slide` column is derived from the plan**, not entered by hand: each cited row's slide is the `slide_no` of the FIRST slide citing it; struck (`verified=no`) and uncited rows stay blank. `gate_runner.py qa1` back-fills it from the plan before checking (default on; `--no-backfill` to skip), or run `helpers/ledger.py backfill-slides intermediate/content_plan.json intermediate/source_ledger.csv` explicitly and re-run after any plan edit. The references slide lists only cited, verified rows.
7. **The plan contains nothing the build may add.** If it is not in the plan it does not reach a slide; this keeps post-build reconciliation light.
8. **Empty/unknown data is an explicit intel-gap element** (a prose or panel note with a readiness action), never a zero or a silent omission.

## The depth / coverage pass (required, after the plan is drafted)
Synthesis validates far more material than a first plan draft uses, and that material is the brief's depth. Once the plan is drafted, run a deliberate coverage pass before the plan is frozen:

1. Run `helpers/gate_runner.py coverage intermediate/content_plan.json intermediate/source_ledger.csv`. It lists every validated (`verified` != no) claim the plan does NOT yet cite, grouped by research agent. (`intermediate/source_ledger.csv` is the canonical ledger location, written by `ledger.py merge` and read by every gate.)
2. Go through the unused claims **cluster by cluster** and record the call in `coverage_log.md`:
   - **work it into a slide** (more real substance, no duplication), or
   - **add a slide** (a distinct, relevant topic the deck is missing), or
   - **leave it out, with a written reason** (it duplicates a slide, or it is not relevant enough: registration numbers, granular sub-items, thin tier-6 micro-facts).
3. **Never drop sourced material silently, and never pad to fill.** An under-filled slide is filled with real validated content where it genuinely fits the slide's argument; where nothing real fits, the space is left balanced (never stretched, ballooned or padded). Coverage and length are a judgement call, but the call must be made and recorded.
4. Apply the decisions (edit the plan), then re-run the gates. G4 reads `coverage_log.md` and blocks if relevant validated material was dropped without reason, or if the deck pads or repeats a layout to fill space.

## Validation before build
The plan is validated by the cheapest gates first: `gate_runner.py validate-plan content_plan.json templates/content_plan.schema.json` (schema), `gate_runner.py self-check templates/content_plan.schema.json helpers/build_deck.py` (slide-kind and cell-kind drift vs the renderer's `KIND`/`CELL`), and `build_deck.py --dry-run` (every slide resolves, no sparse scene), then `gate_runner.py personas content_plan.json` (the three persona slides) and `gate_runner.py spine content_plan.json` (the answer contract: every required answer carried by a substantive slide), before the judgement reviewers G1b/G2/G4 are dispatched. Each reviewer writes its verdict to `intermediate/reviews/<gate>.md`.

## Example scene (a deal explainer: a hero-stat terms row, then a labelled prose block)
```json
{ "slide_no": 9, "kind": "scene", "tone": "dark",
  "eyebrow": "08 | THE DEAL THAT RESHAPES EUROPE",
  "headline": "Kimberly-Clark is handing its European tissue estate to a new owner",
  "claim_ids": ["R2-007", "R2-009"], "confidence": "High",
  "scene": [
    { "weight": 0.5, "cells": [
      { "kind": "stat", "value": "51 / 49", "label": "Suzano control / K-C stake",
        "claim_ids": ["R2-007"], "confidence": "High" },
      { "kind": "stat", "value": "~US$3.4bn", "label": "implied enterprise value",
        "claim_ids": ["R2-007"], "confidence": "High" } ] },
    { "weight": 1.3, "cells": [
      { "kind": "prose", "span": 1.0, "label": "THE DEAL",
        "text": "In June 2025 Kimberly-Clark agreed to carve substantially all of its international tissue and professional business into a Netherlands-based company and sell control to Suzano, keeping 49% and licensing five global brands back to the venture.",
        "claim_ids": ["R2-007", "R2-008"], "confidence": "High" } ] }
  ] }
```
A `table` metric row; the last cell is the trend/read and stays to one short line:
```json
{ "kind": "table",
  "headers": ["Metric", "FY2024", "FY2025", "Trend / read"],
  "rows": [["Adj. gross margin", "38.3%", "37.3%", "Down 100bps on price and tariffs"]],
  "aligns": ["left", "right", "right", "left"],
  "claim_ids": ["R1-004"], "confidence": "High" }
```
