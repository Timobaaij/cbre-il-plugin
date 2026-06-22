# G7 - Visual Render QA (rendered-PNG check)

The mechanical and editorial gates inspect the content plan and the extracted text. They cannot see **layout**: text overflow, shapes colliding, white-on-white text, tables overrunning, content crashing into the footer, or a slide left mostly empty. Those defects only exist once the slides are rendered to pixels. G7 closes that gap.

G7 runs in the post-build gate (Stage 6), alongside reconciliation, the editorial check and the red-team (G8). It is **blocking for HIGH or MED layout defects**: a deck that renders broken or sparse is not shippable however clean its data. It is an **independent reviewer** (isolated sub-agent, fresh context, Opus); it must write its verdict to `intermediate/reviews/G7.md` so the gate can confirm it ran.

## Step 1 - Render every slide to PNG
Windows (PowerPoint COM, the renderer the deck is built for):
```
& "C:/Users/<user>/.claude/skills/cbre-corporate-pptx/scripts/to_png.ps1" `
    -In  "<Company>_briefing/deliverables/<Company>_IL_Briefing.pptx" `
    -OutDir "<Company>_briefing/intermediate/slide_imgs" -Width 1600 -Height 900
```
This writes `01.png ... NN.png`, one per physical slide, in **deck order**. The integer in the filename is the slide's **deck position** and is its authoritative identity. The deck length flexes with the story (each content-plan entry renders exactly one slide), so there are as many PNGs as slides in the plan. The whole-deck render first clears stale PNGs from the folder, so the PNG count always equals the slide count; if it does not, the render is stale, so re-render before reviewing rather than filing issues against a phantom slide. Re-render a single slide with `-SlideIndex N` after a fix (this does NOT clear the folder; it overwrites that one PNG). The build inherits the org sensitivity label and bakes fit-to-text on save, so the rendered PNGs match how the deck opens interactively; G7 inspects that baked result.

**Hand the reviewer the slide-identity index.** Every build writes `build_report.json` next to the `.pptx` with a `g7_index` array: one row per physical slide carrying `png` (`NN.png`), `deck_position` (1-based, the authoritative identity, equal to the filename integer), `slide_no` (the plan's own number, which may be non-numeric like `A`/`ref`), `eyebrow` (the human chapter counter shown on the slide, which can differ from both) and a one-line `thesis`. The orchestrator passes this index to the reviewer so it cites slides unambiguously and never has to infer identity.

## Step 2 - Dispatch an isolated Opus visual-QA reviewer
The reviewer opens each PNG with the Read tool and inspects, per slide: (1) text overflow or clipping; (2) overlapping or colliding shapes; (3) empty, broken, or placeholder boxes; (4) illegible or low-contrast text (e.g. white on a light slide); (5) table problems (columns overrunning, cells clipped, ragged rows); (6) citation markers `[N]` breaking layout; (7) misalignment or content crashing into the footer/wordmark; (8) **whitespace: any content slide left more than ~40 percent empty**; (9) anything unprofessional for a premium client deck. Give it the `g7_index` table and the slide-by-slide plan (each slide's scene) so it knows what each slide should look like.

Pay particular attention to the financial-performance scene: the multi-year table numbers must be right-aligned and unclipped, any hero-stat row must not collide with the table or the footer, and the source/as-of footnote must be legible.

**Cite every slide by `deck_position`, taken from the `g7_index` table** (it equals the integer in the PNG filename). Quote the `slide_no` and `eyebrow` from the index for context, but NEVER infer a slide's identity from the filename digits alone or from the on-slide eyebrow number: the eyebrow is a human chapter counter and routinely differs from both `deck_position` and `slide_no`. Output: a one-line verdict, then per slide `Slide <deck_position> [slide_no <slide_no>]: [OK]` or `[ISSUE - HIGH/MED/LOW]` with specific, located bullets, then a ranked fix list. Written to `intermediate/reviews/G7.md`.

### Known render artefacts to ignore (not defects)
- **Full-bleed dark backgrounds are intended.** Roughly half the deck is dark by design; a dark slide is not a "broken background".
- **Do not judge absolute scale, image stretch, or letterboxing.** `to_png.ps1` exports each slide to a fixed 1600x900 with no aspect/letterbox logic; the deck is natively 16:9 and the PNG is 16:9, so there is no real letterboxing. Any apparent "scale difference" between slides is a render artefact of the exporter, not a deck defect, and must not be filed.
- **A PNG count that disagrees with the slide count, or a cropped/partial PNG, means a stale or interrupted render** (the whole-deck render pre-cleans, so this is rare). Re-render; do not file layout issues against it.
- **G7 reads ONLY `intermediate/slide_imgs`** (the `to_png.ps1` output). The build's internal resolve scratch (`.cbre_resolve` PNGs in the system temp dir) is never part of the review and any leftover there is irrelevant.

## Step 3 - Fix and re-render
- **Content overflow** (a value or note too long for its box): shorten in the content plan. Example: a `stat` hero value is width-capped, so prefer a short value ("17.8") with the unit in the label rather than "EUR 17.8bn".
- **Renderer defect** (a box sized wrong, a colour/tone bug, content into the footer): fix the slide's renderer in `helpers/build_deck.py` (permitted by `deck-structure.md`), then re-render. `helpers/gate_runner.py density` and the `build_report.json` catch the common sparse-slide case mechanically, but G7 is the backstop on the rendered pixels.

Re-render and re-run with a **fresh** reviewer until no HIGH or MED defect remains. Record the pass, defects and fixes on `gate2_scorecard.md`; LOW cosmetic items may be accepted with a note.

## Pass criterion
Zero HIGH or MED layout defects; every fix re-rendered and re-checked by a fresh reviewer; `intermediate/reviews/G7.md` present with the verdict.
