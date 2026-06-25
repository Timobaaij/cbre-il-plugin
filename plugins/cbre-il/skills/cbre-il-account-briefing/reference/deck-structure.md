# Deck composition (the story-led scene method, v8)

This skill produces a business-intelligence account brief that explains a company's story so the reader understands it, and that preps a conversation. The deck is **composed from the story, not poured into a fixed template**: each slide is built from what that slide needs to say, so the slide count and the shape of each slide flex with the company. Two companies should look different; two slides should rarely look the same.

## The governing idea: the story makes the layout
- **Story-led, not template-led.** The narrative outline (Stage 2.5) decides the chapters, their order, and how many slides each earns. There is no fixed slide list.
- **Explain, do not tabulate.** Prose carries the story (especially the M&A); tables are evidence behind the narrative, never the way to make a point.
- **Density from substance, never from tricks.** Fill a slide with more real, relevant content if it makes sense, never with spacing, ballooned fonts, or padding. Leftover space is a signal to write more, not to stretch what is there (see the depth pass in `content-plan-spec.md`).
- **No lazy repetition.** A given scene layout appears at most twice, ideally once. The three persona slides (below) share one layout on purpose, the single deliberate exception, so they read as a family.

## The answer contract (the content floor, not a template)
The deck stays story-led, but a business-intelligence brief is only credible if it lands a fixed set of **questions**, however the composer chooses to slide them. These are the **mandatory answers**. They are checked as CONTENT, never as a template: each is a question the deck must answer somewhere, and the composer still decides how many slides each earns, in what order, and in what layout. Two companies still look different; a thin brief still fails.

Tag the slide, or the specific cell, that lands each answer with an `answers` array (for example `"answers": ["financial-story"]`). `gate_runner.py spine` asserts every REQUIRED answer is carried by a substantive slide or cell; G0 (outline) and G4 (substance) judge whether it is actually said well.

**Required (the spine gate blocks if any is missing):**
- `bluf` - the executive read: the thesis, the two or three big movers, and the single opportunity, in one slide near the front. The "if you read one slide" payoff.
- `company-profile`, `strategy-priorities`, `financial-story` - who they are and the business model; the stated strategy and the three to five priorities; the multi-year financial trajectory read (a direction, not single figures).
- `big-movers` - what is really going on: the handful of vectors reshaping the company (M&A, divestiture, reshoring, channel shift, large capex, rationalisation, ESG), each with its demand direction (created / destroyed / transferred).
- `supply-chain-signature` - what is structurally distinctive about THIS company's supply chain and what it means for how the network is designed and run (capacity and peak-vs-base, node count and role, inventory positioning, make-vs-buy, in-house vs 3PL). Supply-chain intelligence so the lead can talk credibly to a CSCO; NOT the real-estate angle (that is `challenge-to-real-estate`). Works for makers and sellers alike. See `reference/supply-chain-signatures.md`.
- `operating-model`, `network-footprint` - make / move / rebalance and who holds each lease; the physical footprint as it stands.
- `challenge-to-real-estate`, `property-setup`, `recent-movements` - each pressure's property consequence; owned vs leased, IFRS 16 lease liability, WALT, any S&LB; the dated register of moves.
- `stakeholders-governance` - who runs real estate / supply chain / logistics / FM, the reporting line, and any incumbent advisor, acknowledged honestly.
- `opportunity-intersection` - where logistics or industrial demand is being created, destroyed or transferred, each angle tied to a specific sourced fact and incumbents named. Evidence-bound, NOT the speculative forecast module (off by default) and NOT a pitch.
- `what-to-probe` - the intel gaps as opening questions, so the deck itself preps the conversation.
- the three persona answers `persona-ceo`, `persona-csco`, `persona-head-re` (asserted by `gate_runner.py personas`; see below).

**Expected (strongly recommended; the story may justify the omission, and G0/G4 adjudicate):** `why-now` (often folded into the BLUF), `competitive-position`, `company-challenges`. `spine` prints these as an advisory when absent rather than blocking.

The contract raises the floor; it does not touch the freedom above it. Everything not on this list is wholly story-discretionary, and how each answer is rendered (one slide or three, prose or table, where inside its act) is the composer's call.

## The mandatory persona family (always present, no matter what)
Every deck MUST carry three persona slides, always, regardless of company or story:
1. **What is on the mind of the CEO**
2. **What is on the mind of the CSCO** (Chief Supply Chain Officer; if the target has no titled CSCO, use the nearest equivalent and say so)
3. **What is on the mind of the Head of Real Estate** (or the nearest real-estate/property owner; if real estate sits under another role, say so)

They are the conversation-prep payoff: they put the reader in the shoes of each decision-maker and translate everything above into "here is what this person is worried about, and here is how CBRE meets it". Compose them as one shared family layout (the deliberate layout-repetition exception): a `panel` introducing the person (name, role, mandate), a `list` of three or four agenda items (what is on their mind, each a sourced priority), and a closing `prose` "what it means for CBRE" read. Every agenda item is an inference traced to sourced Claim IDs, framed as the priority the evidence puts on that role's agenda, never a fabricated direct quote; carry a footer such as "Priorities inferred from public evidence, not direct statements."

**Placement: distribute each persona to the capstone of the act that earns it; do not bunch them at the end.** Each persona lands immediately after the evidence that justifies its agenda, so the deck builds three times to a "what this means for a real decision-maker, and how CBRE meets it" beat:
- the **CEO** persona closes the company-and-strategy act (after the financial story, competitive position and challenges);
- the **CSCO** persona closes the supply-chain act (after the signature, the operating model and the network);
- the **Head of Real Estate** persona closes the property act (after the set-up, the lease book and the recent movements), flowing into the opportunity and probe close.

They keep their shared family layout wherever they sit (the deliberate layout-repetition exception). Group them as a single block at the end ONLY when `deck_meta.meeting_context` argues for it (for example a single named stakeholder you can then elevate, or a multi-stakeholder panel), and say why in the narrative outline. Tag each persona slide with its `answers` id (`persona-ceo` / `persona-csco` / `persona-head-re`). The mechanical check `gate_runner.py personas` and the Final Gate assert all three are present; G0 and G4 also block if any is missing or hollow.

## A slide is a scene
A scene slide is an ordered list of **rows**; each row splits into **cells** by span; each cell holds one styled primitive. The renderer (`helpers/build_deck.py`) draws the CBRE chrome (eyebrow, fit-to-text serif headline, lead line, footer, wordmark), then lays the scene on a safe grid and sizes each cell's text up to fill its space. The grid only prevents overlap and off-canvas; it is not a template.

**Slide kinds** (the renderer's `KIND` dict; the schema enum; kept in lock-step by `gate_runner.py self-check`):
- `cover`, `divider`, `references` keep their fixed chrome.
- `scene` is a freely composed slide.

**Cell kinds** (the renderer's `CELL` dict; the schema enum):
- `prose` - a full paragraph (`text`, optional bold lead `label` such as "THE SITUATION", "WHY", "WHAT IT MEANS"). The explainer workhorse of the deck.
- `stat` - a hero `value` plus a caption `label` (unit in the label).
- `list` - `items` of {title, text}, `numbered` or bulleted.
- `table` - `headers` plus `rows`; the last column is the analytical read.
- `panel` - a dark accent side box; `title` plus `items` of {label, value}, or a `text` body.
- `quote` - a pull `quote` text plus `attrib`.
- `heading` - a small section label.
- `rule` - a thin divider line.

## Row and cell layout
- Rows fill the body by `weight` (relative vertical share, default 1).
- Cells split a row by `span` (relative horizontal share, default 1).
- A scene with no content degrades to a clean intel-gap callout, never a bare header.

## The minimal spine (for auditability)
`cover` first; `references` last (built from the cited, verified Source Ledger rows); the **answer contract** above carried in full (every required answer, including the three persona slides); and the schema floor (`minItems`) so a degenerate plan fails. Beyond the contract there is no fixed slide count, order or list: the story composes the rest. Dividers are optional, used only when the story has clear acts.

## Renderer behaviours that matter (all in `helpers/build_deck.py`)
- **Fit-to-text titles** via `build.editorial_header`, which measures the title and returns the true body-top, so there is no reserved-whitespace gap under the headline.
- **Prose** fills up to a readable cap (about 16pt) and floors near 12.5pt; thin text in a tall cell is a signal to write more substance, not to balloon the font.
- **Panels** stack their items from the top, measured so they never collide; the value font scales within caps.
- **Stats** size to the cell but are width-capped, so a long value (for example "~US$3.4bn") never wraps to a stray second line.
- **Autofit and label bake.** The build inherits the organisation's sensitivity label and bakes "fit shape to text" into the saved file via PowerPoint COM (`cbre-corporate-pptx`: `save(label_from=..., bake=True)`), so the deck opens with every box already fitted and carries its label, with no manual step. See `content-and-tone.md` and `visual-qa.md`.

## Composing the chapters
Open the deck on the executive read (`bluf`) so the reader gets the thesis, the big movers and the one opportunity before any detail. Open each chapter by explaining its argument in prose, then place the evidence: a `table` for a list or register, a `stat` row for the hero numbers, a `panel` for an at-a-glance lens. Open the supply-chain act on the **supply-chain signature** (`reference/supply-chain-signatures.md`): the two to four characteristics that actually dictate this network's shape, and the **network / operating consequence** of each (capacity, nodes, inventory positioning, make-vs-buy, in-house vs 3PL), before the operating model and the footprint explain how it runs and where it sits. Keep this slide on the supply chain - the real-estate translation is the later `challenge-to-real-estate` slide, not here. It must read as well for a manufacturer as for a retailer. Tell the big events (an acquisition, divestiture, JV, large committed capex) as dedicated prose-led scenes that say what happened, why, and what it means, never a single table row, and bring them together in the `big-movers` read so the reader sees the handful of vectors at once. Length follows the story; G0 judges whether the allocation fits it.

## Per-company-type adaptation (driven by the story, not a switch)
- **Manufacturer / industrial:** chapters on strategy, the financial story, the operating model and footprint, and the real-estate read; prose-led scenes for reshoring / divestiture / M&A; tables for the plant network and recent moves.
- **Retailer / restaurant:** format and channel strategy, the financial story, the store-and-DC network and fulfilment model; prose-led scenes for major acquisitions or estate programmes; tables for the store/DC network and openings/closures.
- **B2B distributor / wholesaler:** the service model, the financial story, the branch/depot network; tables for the depot network and contract wins/losses.
- **E-commerce / omnichannel:** the channel and fulfilment strategy, the financial story, the fulfilment and last-mile network; prose-led scenes for fulfilment build-outs or acquisitions.

The story decides which chapters exist and how long each runs; do not force a company into a chapter it does not have.

## The two enforceable insight rules
1. **Prose explains; it never fragments.** Every `prose` cell is a full, connected explanation (the density gate rejects a prose cell too short to be a sentence). Every `table` carries a rightmost analytical-read column, written as a read and never a restatement, and its last cell is always populated.
2. **Every slide lands its point.** A `lead` line states the so-what under the headline; the visual gate (G7) confirms no slide is left mostly empty. Where a slide under-fills, the fix is real validated content, not stretching (see the depth pass).

## Changing the cell library
The cell library is intentionally small and each primitive renderer is documented in `helpers/build_deck.py` (the `CELL` dict; slide kinds in `KIND`). If a beat genuinely needs a primitive the library lacks, add or edit the renderer, update `templates/content_plan.schema.json` (the slide-`kind` and cell-`kind` enums) together, and re-run `gate_runner.py self-check` so the schema, renderer and docs stay in lock-step. Do not improvise per run, and do not leave a retired primitive half-removed.
