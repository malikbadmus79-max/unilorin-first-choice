# Phase 3: independent recheck

As of 31 October 2026.

## Method

38 values were drawn at random (seed 20261031) from the raw tables: 20 from `applicants_sources.csv`, 6 from `funnel_sources.csv`, 4 from `national_scores_sources.csv`, 3 from `fees_sources.csv`, 3 from `kwara_insecurity_sources.csv` and 2 from `strike_events.csv`. A separate agent, given only each claim and its URL, opened every page and classified the claim as MATCH, MISMATCH, NOT FOUND or FAILED, quoting the page. Results are in `data/validation/phase3_recheck.csv`.

The recheck was carried out by an AI agent, not by a human coder.

## Result

| Verdict | Count |
|---|---|
| MATCH | 38 |
| MISMATCH | 0 |
| NOT FOUND | 0 |
| FAILED | 0 |

All 38 sampled values match their sources (100%; 95% Wilson interval 90.8–100%).

## Corrections made

- V35: the January 2026 abduction report concerns the Isanlu–Isin–Omu-Aran road in Kwara South, not the Ilorin–Ogbomoso highway. The area in `kwara_insecurity_sources.csv` and the wording in `phase2_notes.md` (Result 5) were corrected. The December 2025 Ilorin–Ogbomoso report is unaffected.

## Points confirmed but worth noting

- V08: ThisDay's sentence describes the 2021 figure of 78,466 as "total UTME applications", with first-choice wording in the preceding sentence. Other sources describe the same figure as first-choice.
- V17: Legit.ng's 2024 list prints 63,143 for the University of Ilorin while its text says 64,143 (already recorded).
- V28 and V30: two different published values for candidates scoring 200 and above in 2025 (420,415 of 1,955,069; 565,988 of 1,931,467 including resits), already carried as a low–high range.
