# Research agent output contract (Stage 1)

Each research agent (R1-R5) writes two files to `intermediate/agents/`:

1. `R{n}_<slice>.findings.md` — the structured findings, human-readable.
2. `R{n}_<slice>.sources.csv` — one row per claim, matching the Source Ledger header (`templates/source_ledger_columns.md`).

The contract between stages is: **findings travel with source records attached, never bare claims.** Every assertion in the findings file must have a corresponding row in the sources CSV, keyed by the same Claim ID.

## findings.md structure

```markdown
# R2 Network and Facilities — <Company>

## Summary
Three to five sentences: the I&L-relevant headline of what this agent found.

## Findings
- [R2-001] <claim as a full sentence>. (tier 1; FY2024 annual report p.42)
- [R2-002] <claim>. (tier 4; developer press release)
- ...

## Recent-moves register (R2 only; openings/closures/expansions, last 24 months)
| date | site | country | what happened | RE implication | claim_id |
|------|------|---------|---------------|----------------|----------|

## Gaps (explicit; never guess)
- Owned vs leased split not disclosed in any tier 1-3 source. Priority intel gap.
- ...
```

## sources.csv

Header (exact): `claim_id,slide,claim,source_url,source_tier,figure_or_quote_at_source,source_pub_date,retrieved_date,confidence_band,binding_test,verified`

The agent fills `claim_id, claim, source_url, source_tier, figure_or_quote_at_source, source_pub_date, retrieved_date`. Leave `slide, confidence_band, binding_test, verified` blank; the Orchestrator fills them in later stages. Claim IDs are agent-prefixed: R1-001, R2-014, etc.

## Rules for agents

- Fetch the company IR page first.
- Trace each claim to the highest source tier on which it should exist; cite the originator, not the echo.
- Record the source's publication/as-of date separately from the retrieved date.
- Return explicit gaps, never guesses. A gap is a finding.
- Do not edit the ledger; the Orchestrator merges your `*.sources.csv`.
