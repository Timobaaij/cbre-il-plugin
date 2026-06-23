# Localisation (i18n) - bundled languages, the fallback, and the G-i18n gate

The dashboard renders its CHROME (the fixed UI vocabulary - tabs, filters, sort options,
the KPI strip labels, section titles, row labels, the compare table, map controls, the
footer disclaimer) in a chosen European Latin-script language. **Only chrome is localised;
DATA is never translated** (property/developer/landlord/region/city/POI names, every
figure, date, unit, source citation, and the canonical `tbd`/`—` sentinel stay exactly as
sourced). The machinery lives in `helpers/i18n.py`; see also `reference/config.md`
("Dashboard language") and `reference/gates.md` (G-i18n).

## Supported vs bundled
`i18n.py` carries a `SUPPORTED` registry - the AUTHORITATIVE list of every base language the
skill can present, each with a default BCP-47 locale and the accepted names/endonyms.

- **Bundled (instant, 12):** `en` (the authoritative English baseline) + `de fr es it nl pl
  pt cs sk hu ro`, each shipped as `assets/i18n/<code>.json`. These render with zero extra
  round-trips; `is_bundled(code)` is true.
- **Fallback-eligible (translated on demand):** the other SUPPORTED European Latin-script
  languages - currently Danish `da`, Swedish `sv`, Norwegian `nb`, Finnish `fi`, Icelandic
  `is`, Irish `ga`, Croatian `hr`, Slovenian `sl`, Estonian `et`, Latvian `lv`, Lithuanian
  `lt`, Maltese `mt`, Catalan `ca`, Galician `gl`, Luxembourgish `lb`. `is_supported` is
  true, `is_bundled` is false, so `needs_fallback` is true.
- **Unsupported (non-Latin / nonsense):** anything that does not resolve (e.g. Greek,
  Klingon, gibberish) -> `normalize_lang` returns `'en'` and the dashboard renders in
  English. No request, no crash - English is the correct answer.

`normalize_lang` resolves a SUPPORTED language (bundled OR fallback-eligible) to ITS OWN
code (Danish/`da`/`da-DK` -> `da`); only a genuinely unknown value returns `'en'`.

## The translate-once-cache fallback (exit 11) - byte-stable by construction
A fallback language is translated ONCE in Cowork, cached in the work dir, and BAKED into
`canonical.meta.ui_overrides` by `merge.py` so that `render()` - and `validate-html`'s
re-run of it - reproduce the localised chrome from `canonical` ALONE. This is what keeps the
fallback byte-stable: `validate-html` re-runs `render(canonical)` and asserts byte-identity,
so anything render consumes for a language must ride canonical.

Flow (mirrors the exit 3/9/10 request-manifest pattern):

1. **`run.py` resolves the language** right after Stage-0 intake, before the expensive
   merge/enrich (fail fast). If it `needs_fallback` and there is no valid work-dir cache,
   it writes a **request manifest** and **exits 11**.
   - Manifest: `work/i18n/<code>_request.json` =
     `{"code", "language", "locale", "en_sha", "instructions", "cache_path", "skip_path",
     "strings": <the 175 EN chrome strings>}`.
   - The orchestrator dispatches an ISOLATED translation sub-agent: translate every value in
     `strings` to the language; keep the JSON KEYS, the `{area}`/`{unit}` placeholders, the
     `&amp;`/`&lt;`/`&gt;` entities, any leading glyph (the `●` bullet), and the invariants
     `CBRE / OSRM / BREEAM / HGV / PPS / EU27 / REIT / km` verbatim; never translate DATA or
     the `tbd`/`—` sentinel; add a top-level `"_en_sha":"<en_sha>"`; write the flat
     `{key: value}` to `work/i18n/<code>.json`; then re-run the SAME command.
   - Decline instead with `type nul > work/i18n/<code>.SKIP` to fall back to English.
2. **On the re-run** the cache exists and its `_en_sha` matches `i18n.en_sha()` ->
   `run.py` passes `--ui-overrides work/i18n/<code>.json` to `merge.py`. Merge bakes
   `meta.ui_overrides` = the EN-keyed entries only (a leading `_en_sha`/any `_*` meta key and
   any non-EN/DATA key are dropped - CHROME only). `render()` layers it over EN.
3. **Graceful degradation:** a `.SKIP` decline -> English (a printed note); a
   missing/corrupt/empty cache -> re-requested (or English once declined) - never a crash.

### The cache key (`_en_sha`) and resume
- The cache is keyed by `_en_sha` = `i18n.en_sha()`, a short stable hash of the EN baseline
  + `I18N_SCHEMA_VERSION`. If the EN baseline ever changes, `en_sha()` changes, the cached
  `_en_sha` no longer matches, and the stale cache is **re-requested** (exit 11) rather than
  silently used.
- The cache file is a `merge_inputs` member (alongside `work/.language`, `requirements.json`
  etc.), so a CHANGED translation re-fires merge -> canonical changes -> the build re-runs.
- `meta.ui_overrides` rides canonical, so `render()`/`validate-html` are byte-identical
  across runs and two offline builds of the same fallback canonical are byte-identical.

## The G-i18n quality gate
Confirms the rendered chrome reads as a fluent, correct, complete, in-language dashboard.

- **Deterministic floor** (`gate_runner.py i18n`, in the post-build sequence + the eval
  battery): `const UI` is the exact EN key set (175); no UI value carries an unfilled
  `{{token}}`; `const LOCALE` is a well-formed BCP-47 tag whose primary subtag matches the
  resolved language; for a language EXPECTED to be localised (bundled, or `meta.ui_overrides`
  present) the UI differs from EN in >= 40% of non-invariant keys (the **silent-fallback
  catch** - a translation that collapsed back to English is blocked); `{area}`/`{unit}`
  survive in the format keys.
- **Blind LLM rubric** (the live counterpart, **Cowork-only**): an ISOLATED reviewer (NOT
  the translator) judges fluency, completeness (no English chrome beyond the invariants),
  local-market house terms, intact placeholders/entities, and that DATA + the `tbd` sentinel
  are untouched. Output `pass`/`pass-with-notes`/`fail` + a term list. See `reference/gates.md`
  for the full rubric and verdict mapping; the visual surface (truncation/overflow,
  leaked-English) is also checked by G-visual (`reference/visual-qa.md`).

This applies to BOTH bundled and fallback languages.
