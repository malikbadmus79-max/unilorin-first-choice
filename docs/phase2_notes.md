# Phase 2 notes: admission funnel and the national score effect

As of 31 October 2026.

## Data added

- `data/raw/funnel_sources.csv`: 28 values on Post-UTME screening, admission and matriculation at the University of Ilorin, 2017–2026.
- `data/raw/national_scores_sources.csv`: national UTME score bands, 2019–2025.

## Result 1: the 2020–2021 fall was national

The number of University of Ilorin first-choice candidates scoring 180 or more fell from about 72,000 (2020, vice-chancellor's matriculation statement) to 28,048 (2021). Nationally, candidates scoring 180 or more fell from 781,327 to 323,624 (2021 figure summed from published bands). The university's share of the national 180+ pool was 9.2% in 2020 and 8.7% in 2021. The 2021 fall therefore follows the national fall in scores in the year after the COVID-19 closures and is not specific to the university. The first strike (March–December 2020) shows no clear effect on the share of qualified candidates.

## Result 2: the university-specific decline begins after 2021

Candidates at the university's Post-UTME screening per 100 candidates nationally scoring 200 or more:

| UTME year | Screened | National 200+ | Per 100 |
|---|---|---|---|
| 2020 | 46,000 | 404,542 | 11.4 |
| 2021 | 18,153 | 168,613 | 10.8 |
| 2022 | about 25,000 (projected) | 378,639 | 6.6 |
| 2023 | 16,920 | about 355,650 | 4.8 |
| 2024 | 16,097 | 442,167 | 3.6 |
| 2025 | 20,220 (UTME registrants) | 420,415–565,988 | 3.6–4.8 |

The ratio is stable in 2020–2021 and falls by about two-thirds between 2021 and 2024. The fall begins in the cycle that includes the February–October 2022 strike, which delayed the 2022 and 2023 screenings to February 2023 and February 2024. The timing is consistent with the strike explanation but does not establish it; new universities, insecurity and costs remain to be tested over the same years.

## Caveats

- The 2020 figures (72,000; 46,000) are rounded numbers from a speech.
- The ratio compares screened candidates (who scored 180+) with national candidates scoring 200+, so it is an index, not a share.
- National 200+ counts for 2023 and 2024 are derived from rounded percentages; 2025 has two published values.
- Screening counts mix "registered", "sat" and "attended" across years (see funnel_sources.csv).

## Result 3: the strike comparison (control group)

`data/raw/strike_events.csv` records strike participation for the University of Ilorin, Lagos State University (LASU) and Kwara State University (KWASU).

- LASU and KWASU did not join the February–October 2022 national strike; the University of Ilorin did. In July 2022 the Lagos governor's education adviser said LASU and the two new Lagos universities were "oversubscribed in the 2022 UTME application" because they were not on strike (a claim by an interested official, not independent data).
- LASU's first-choice applications rose from below 38,309 in 2021 (outside the top 10) to 55,964 in 2023, 62,601 in 2024, 70,080 in 2025 and 84,426 in 2026, moving from outside the top 10 to first.
- The federal peers (UNILAG, OAU, UNIBEN, UNN, UNIZIK, FUOYE) also struck in 2022, yet all gained first-choice applications between 2021 and 2026. A strike alone did not reduce demand for them.
- LASU itself struck in December 2024, July 2025 and September 2026, and its applications continued to rise.

Reading: the evidence is consistent with a narrower mechanism than "strikes reduce demand". The University of Ilorin's distinctive advantage was a calendar without strikes; the 2022 strike removed that advantage, while universities that had no such reputation were not penalised. The data cannot separate this from the other explanations still to be tested (new universities including KWASU's expansion, insecurity in Kwara, costs).

## Result 4: new universities in Kwara

`data/raw/kwara_universities.csv` lists 15 universities in Kwara State with ownership and licence year. Eight were licensed between 2021 and 2025: Thomas Adewumi University, Ahman Pategi University and University of Offa (2021); Muhammad Kamalud-deen University (2023); Kwara State University of Education (2024); Lens University, AbdulRasaq Abubakar Toyin University and Jimoh Babalola University (2025). Seven are private; one is state-owned.

Assessment:

- Scale: private universities have historically drawn a small share of UTME candidates (18,667 of over 1.6 million in 2014; under 20,000 of over 1.4 million in 2015). The University of Ilorin's first-choice applications fell by about 26,000 between 2021 and 2026. New private universities in Kwara, most of them small and fee-charging, are unlikely to account for a fall of that size on their own.
- Timing: the three 2025 universities took their first students in 2025/2026, after most of the decline (2022–2024) had already happened.
- Not tested: Kwara State University (KWASU), the state university in Malete, which stayed open during the 2022 strike, and the new Kwara State University of Education. Their first-choice application figures are not published (neither is in JAMB's top 10). This is the main gap in this explanation.

Verdict: new private universities are unlikely to be a main cause. A shift to KWASU cannot be assessed without its application figures.
