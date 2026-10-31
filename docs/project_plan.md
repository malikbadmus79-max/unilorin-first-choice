# Project plan

## Research questions

1. How much did first-choice UTME demand for the University of Ilorin change from 2020 to 2026, in number and as a share of all candidates?
2. Is the change specific to the University of Ilorin compared with its peers?
3. Where are candidates lost between first choice, the 180 cut-off, Post-UTME screening and admission?
4. Which explanations can public data support or rule out: new universities nearby, insecurity in Kwara, cost, admission rules, changing search interest?

## Data sources

| Data | Source | File | Used for |
|---|---|---|---|
| First-choice applicants by institution and year | JAMB policy-meeting figures as reported by news outlets (S01–S17) | `data/raw/applicants_sources.csv` | Q1, Q2 |
| National UTME totals (registered, sat, results released) | News reports of JAMB statements (N01–N09) | `data/raw/national_totals_sources.csv` | Q1 (shares) |
| Post-UTME screening and admission at the University of Ilorin | University statements and news reports (P01, P02, T01, U01, S01, S02) | `data/raw/funnel_sources.csv` | Q3 |
| JAMB policy-meeting documents | jamb.gov.ng (not yet retrieved) | — | Q1–Q3 confirmation |
| New universities near Ilorin, licensing dates | NUC lists of approved universities | — | Q4 |
| Security incidents in Kwara State | ACLED or comparable event data | — | Q4 |
| Fees and charges | University announcements, press | — | Q4 |
| Admission rules (cut-offs, catchment, quotas) | JAMB and university announcements | — | Q4 |
| Search interest | Google Trends, Nigeria | — | Q4 |

Every source is listed in [source_log.md](source_log.md).

## Methods

1. Collection. Each published figure is copied as printed, with source_id, outlet, URL, publication date, attribution and the measure as stated. Nothing is corrected in `data/raw`.
2. Acceptance rule. A value is accepted when two or more independent sources print the same value for the same UTME year and institution. Single-source values are kept and marked "single source". S09 (different measure) and S17 (year-shifted) are excluded. Conflicts are recorded, not resolved silently. `src/first_choice/series.py` applies the rule and checks it against `data/interim`.
3. Shares. JAMB's printed shares are used where they exist. Elsewhere shares are computed against registered candidates, the base JAMB's printed shares imply.
4. Peer comparison. Change from 2021 to 2026 is compared for universities in JAMB's top 10 in both years. Results are reported for this balanced set only.
5. Funnel. For each year with data, the University of Ilorin's counts are lined up across first choice, candidates at or above 180, Post-UTME screening and admission. Stage definitions are recorded as stated because they differ between years.
6. Explanations. Each candidate explanation is stated with a prediction that public data could contradict (for example, if new nearby universities explain the fall, demand should fall most after they open and most among candidates from nearby states). Each explanation is reported as supported, not supported, or not testable with available data.

## Phases

| Phase | Content | Status |
|---|---|---|
| 1 | Source collection; University of Ilorin series 2018–2026; peer panel; national totals; first figure | Complete |
| 2 | Retrieve JAMB policy documents; fill 2022 and missing national totals; build the funnel (Q3); rebuild figures from code | Next |
| 3 | Explanation tests (Q4): new universities, insecurity, cost, admission rules, search interest | Planned |
| 4 | Write-up and release of data and code | Planned |

## Limitations

- Published data can test explanations but cannot establish cause.
- Most figures are JAMB statements reported in news, not JAMB's own documents. Outlets sometimes print different numbers for the same value, or label the wrong year.
- JAMB's own policy documents have not yet been retrieved.
- Universities that left the top 10 have no published figures, so the peer comparison covers only universities that stayed in it.
