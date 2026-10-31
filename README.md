# From first choice to fading choice: UTME demand for the University of Ilorin, 2020–2026

For years the University of Ilorin was the institution named most often as first choice in Nigeria's Unified Tertiary Matriculation Examination (UTME). This project rebuilds the number of candidates who chose it first in each UTME year from 2020 to 2026, using figures published by the Joint Admissions and Matriculation Board (JAMB) as reported in the press. It records every figure with its source, accepts a value only when independent sources agree, compares the University of Ilorin with peer universities, and tests which explanations for the change public data can support or rule out.

## Key findings

- First-choice applications fell from 103,582 (2020) to 52,514 (2026) and the university's rank from first to seventh, while all six of its peers in JAMB's top 10 in both 2021 and 2026 gained applicants.
- The 2021 fall followed a national fall in UTME scores; from 2022 the university drew far fewer of the country's qualified candidates (10.8 screened per 100 candidates nationally scoring 200+ in 2021, 3.6 in 2024).
- The timing is most consistent with the loss of its reputation for a calendar without strikes after the 2022 strike: Lagos State University, which stayed open, gained applications, and Kwara State University gained search interest (its applications are not published). New private universities and insecurity do not explain the fall; fees are not supported as a cause, on limited evidence. The data shows patterns, not candidates' reasons.
- Full results with sources: [docs/findings.md](docs/findings.md). Recommendations: [docs/policy_brief.md](docs/policy_brief.md).

## Research questions

1. How much did first-choice UTME demand for the University of Ilorin change from 2020 to 2026, in number and as a share of all candidates?
2. Is the change specific to the University of Ilorin compared with its peers?
3. Where are candidates lost between first choice, the 180 cut-off, Post-UTME screening and admission?
4. Which explanations can public data support or rule out: new universities nearby, insecurity in Kwara, cost, admission rules, changing search interest?

## Headline results

First-choice applications to the University of Ilorin fell from 103,582 in 2020 to 52,514 in 2026, a fall of 49.3%. Its share of all applicants fell from 5.31% to 2.34%, and it dropped from first place (2018–2024) to seventh (2026).

Seven universities were in JAMB's top 10 in both 2021 and 2026. Of these, only the University of Ilorin had fewer first-choice applications in 2026 than in 2021: 78,466 down to 52,514 (−33%). The other six rose by between 5% (Federal University Oye-Ekiti) and 42% (Obafemi Awolowo University). Universities that left the top 10 have no published 2026 figure, so they are not part of this comparison.

![Change in first-choice applications, 2021 to 2026, universities in JAMB's top 10 in both years](figures/fig1_change_2021_2026.png)

After 2021 the University of Ilorin also drew fewer of the country's qualified candidates to its own screening: candidates at its Post-UTME screening fell from 10.8 per 100 candidates nationally scoring 200 or more in 2021 to 3.6 in 2024.

![Candidates at the University of Ilorin's Post-UTME screening per 100 candidates nationally scoring 200+, 2020–2025](figures/fig2_screening_share.png)

Figure 2: Post-UTME screening at the University of Ilorin per 100 candidates nationally scoring 200 or more, 2020–2025, with the 2020 and 2022 strikes shaded.

![Share of Google search interest in Nigeria among Unilorin, LASU, UNILAG, OAU and KWASU, 2019–2026](figures/fig3_search_share.png)

Figure 3: Unilorin's share of Google search interest in Nigeria among five university names, 2019–2026 (2026 is January to October), with the 2022 strike shaded.

First-choice figures for 2022 are not established: no source prints a comparable University of Ilorin value for that year. See [docs/phase1_notes.md](docs/phase1_notes.md) for the series, the acceptance rule and the conflicts found in published figures.

## Repository map

```
assets/
  fonts/                Inter typeface used in the figures (SIL Open Font License)
data/
  raw/                  figures copied as printed, one row per source and value
    applicants_sources.csv        first-choice applicants by institution and UTME year
    fees_sources.csv              published tuition and charges, 2023 and 2025
    funnel_sources.csv            Post-UTME screening, admission and matriculation, University of Ilorin
    google_trends_ng.csv          Google Trends monthly search interest, Nigeria, five university names
    kwara_insecurity_sources.csv  published counts of violence in Kwara State
    kwara_universities.csv        universities in Kwara State with licence year
    national_scores_sources.csv   national UTME score bands
    national_totals_sources.csv   national UTME totals by year and measure
    strike_events.csv             strikes at the University of Ilorin and comparison universities
  interim/              values derived from data/raw by src/first_choice
    peer_panel.csv                    institution-year panel
    unilorin_first_choice_series.csv  University of Ilorin series, 2018–2026
    funnel_by_year.csv                first choice to matriculation, 2018–2026
    national_200plus.csv              national candidates scoring 200+
    screening_index.csv               screened per 100 national 200+ candidates
    unilorin_share_180plus.csv        share of national 180+ candidates, 2020–2021
    trends_yearly.csv                 yearly search interest and share per term, 2019–2026
  validation/           Phase 3 recheck
    phase3_recheck.csv                38 sampled values with verdict and note
docs/
  findings.md           findings with the source of every figure
  policy_brief.md       policy brief and recommendations
  phase1_notes.md       Phase 1 notes: sources, rule, series, problems found
  phase2_notes.md       Phase 2 notes: funnel, national scores, strikes, explanations, search interest
  phase2_conclusion.md  Phase 2 conclusion: verdict on each explanation
  phase3_validation.md  Phase 3 independent recheck of 38 sampled values
  project_plan.md       research questions, data, methods, phases, limitations
  source_log.md         every source_id with outlet, URL and publication date
figures/
  fig1_change_2021_2026.png/.svg
  fig2_screening_share.png/.svg
  fig3_search_share.png/.svg
src/first_choice/
  series.py             first-choice series and peer panel
  funnel.py             funnel, national 200+ counts, screening index
  trends.py             Google Trends download and yearly shares
  figures.py            figures 1 to 3
tests/
  test_series.py
  test_funnel.py
  test_trends.py
```

## Reproduce

Set up the environment once:

```
python -m venv .venv
.venv/Scripts/activate        # Windows; on macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
```

Then run, in order:

```
python -m first_choice.series    # checks the first-choice tables against data/interim (--write regenerates them)
python -m first_choice.funnel    # checks the funnel, national 200+ and screening index tables (--write regenerates them)
python -m first_choice.trends    # checks the yearly search shares (--write regenerates them)
python -m first_choice.figures   # redraws figures/ from data/interim
pytest
```

`python -m first_choice.trends --download` fetches a new `data/raw/google_trends_ng.csv` from Google Trends. It needs the `trends` extra (`pip install -e ".[trends]"`) and an internet connection, and it does not overwrite an existing download.

The acceptance rule is stated in the docstring of `src/first_choice/series.py`; the funnel rules in `src/first_choice/funnel.py`.

## Status

v1.0: analysis complete. Phase 1 (first-choice series and peer panel), Phase 2 (funnel, national scores, strikes, new universities, insecurity, fees, search interest) and Phase 3 (independent recheck) are done. See [docs/findings.md](docs/findings.md) and [docs/project_plan.md](docs/project_plan.md).

## Licence

Code is released under the MIT Licence (see [LICENSE](LICENSE)). Data and documentation in `data/`, `docs/` and `figures/` are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); the underlying figures remain the statements of JAMB and the outlets cited in [docs/source_log.md](docs/source_log.md).

The Inter fonts in `assets/fonts/` are released under the SIL Open Font License 1.1 (see [assets/fonts/LICENSE.txt](assets/fonts/LICENSE.txt)).
