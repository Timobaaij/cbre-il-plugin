# Source Ledger columns (single source of truth)

The canonical column order, matched by `helpers/ledger.py` (`COLUMNS`). Agent
`*.sources.csv` files use the same header; the Orchestrator fills `slide`,
`confidence_band`, `binding_test`, and `verified` during later stages.

| # | Column | Filled by | Notes |
|---|---|---|---|
| 1 | `claim_id` | research agent | Stable unique ID, agent-prefixed (e.g. `R2-014`). |
| 2 | `slide` | Stage 3 (derived) | Slide number the claim appears on; blank if struck. |
| 3 | `claim` | research agent | The claim as it will be stated. |
| 4 | `source_url` | research agent | Exact retrievable URL. Required at merge. |
| 5 | `source_tier` | research agent | 1-6 per source-hierarchy.md. Required at merge. |
| 6 | `figure_or_quote_at_source` | research agent | Exact figure/quote as it appears at source. |
| 7 | `source_pub_date` | research agent | Source's own publication/as-of date, or "undated". |
| 8 | `retrieved_date` | research agent | When fetched. Required at merge. |
| 9 | `confidence_band` | Stage 4 (QA1) | High/Medium/Low from confidence.py. |
| 10 | `binding_test` | Stage 4 (QA1) | tier / recency / corroboration / plausibility. |
| 11 | `verified` | Stage 4 (QA1) | yes / no. "no" = struck, goes to readiness sheet, blank slide. |

Required-at-merge fields (a row missing any is rejected by `ledger.py merge`):
`claim_id`, `claim`, `source_url`, `source_tier`, `retrieved_date`.
