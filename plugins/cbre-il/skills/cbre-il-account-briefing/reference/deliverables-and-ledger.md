# Deliverables, Source Ledger, and Meeting Brief (Stage 7)

Three artefacts ship, every time, in `deliverables/`.

## 1. The CBRE-branded deck
`<Company>_IL_Briefing.pptx` - the story-led intelligence brief per `deck-structure.md`, built via `helpers/build_deck.py` (which calls the `cbre-corporate-pptx` library, inheriting the org sensitivity label and baking fit-to-text on save). Claims are traced in the Source Ledger and surfaced on the references slide (inline `[N]` markers are off by default). Dense by construction: every table carries an analytical-read column and every scene leads with its so-what.

## 2. The Source Ledger
`<Company>_Source_Ledger.xlsx` - every material claim mapped to one row. Built and exported by `helpers/ledger.py export`. Columns (also in `templates/source_ledger_columns.md`):

| Column | Meaning |
|---|---|
| `claim_id` | Stable unique ID (e.g. `R2-014`); matches the inline `[N]` mapping. |
| `slide` | Slide the claim appears on (the `slide_no` of the first slide citing it; blank if struck or uncited). Derived from the plan by `helpers/ledger.py backfill-slides`, which `qa1` also runs automatically. Not entered by hand. |
| `claim` | The claim as stated. |
| `source_url` | The exact retrievable URL. |
| `source_tier` | 1-6 per `source-hierarchy.md` (the tier verified at). |
| `figure_or_quote_at_source` | The exact figure/quote as it appears at source. |
| `source_pub_date` | The source's own publication/as-of date (or "undated"). |
| `retrieved_date` | When fetched. |
| `confidence_band` | High / Medium / Low, from `helpers/confidence.py`. |
| `binding_test` | Which rubric test set the band (tier / recency / corroboration / plausibility). |
| `verified` | yes / no. Struck (no) claims do not appear on a slide; they go to the Meeting Brief. |

The working ledger lives at `intermediate/source_ledger.csv` (the canonical location `ledger.py merge` writes and every gate plus `final_gate.py` reads); the shipped `.xlsx` is exported from it. No copy to the briefing root is needed.

The references slide is the trimmed public face of this ledger (domain, tier, date, matched to `[N]`); the `.xlsx` is the full audit trail.

**Multilingual runs (`deck_meta.language`).** When the brief is authored in another language, translation applies to the **authored** text only: the deck prose/headlines/labels/tables, the Meeting Brief, and the ledger `claim` column are written in the target language. The **source-verbatim** fields are NEVER translated: `figure_or_quote_at_source` stays exactly as it appears at source (a Danish report's "150 lagre" stays "150 lagre"), as do `source_url`, dates, tiers and `claim_id`. That preserves the audit trail. The renderer chrome (the references slide's "Sources"/tier label, the cover, the footer) is localised automatically from `build_deck.py`'s `STRINGS` table; the reader-facing tier label is localised while the tier *number* is unchanged.

## 3. The Meeting Brief
`<Company>_Meeting_Brief.md` - the one-page conversation-prep sheet. It is what the person walking into the meeting reads. Three sections:
- **Probe in the meeting** - the intelligence gaps phrased as opening questions (owned vs leased split, current lease maturity, S&LB intent, the permanent real-estate head, etc.), each with the Phase 1 action that closes it.
- **Be ready for** - the likely objections and the honest answer (stale figures, an incumbent advisor, "isn't this just the recall", "we're growing now").
- **Struck and thin items** - every `verified=no` ledger item and every thin tier-5/6 claim, with a "do not assert / reconfirm" note.

Build it from the G1b strikes, the Data-Gap items, and the G8 red-team soft spots routed to readiness. **Order by meeting context** if provided (a Head of Supply Chain meeting leads with network and operating-model items; a CFO or CRE meeting leads with lease, S&LB and RE-value items); otherwise by severity. Keep it to one page; it is a working sheet, not a narrative.

## Output bundle
```
<Company>_briefing/deliverables/
  <Company>_IL_Briefing.pptx
  <Company>_Source_Ledger.xlsx
  <Company>_Meeting_Brief.md
```
Every `verified=no` ledger item must appear on the Meeting Brief, and every readiness item that closes a gap must map to a probe question.
