# From first choice to fading choice: UTME demand for the University of Ilorin, 2020–2026

For years the University of Ilorin was the institution named most often as first choice in Nigeria's Unified Tertiary Matriculation Examination (UTME). This project rebuilds the number of candidates who chose it first in each UTME year from 2020 to 2026, using figures published by the Joint Admissions and Matriculation Board (JAMB) as reported in the press. It records every figure with its source, accepts a value only when independent sources agree, compares the University of Ilorin with peer universities, and tests which explanations for the change public data can support or rule out.

## Research questions

1. How much did first-choice UTME demand for the University of Ilorin change from 2020 to 2026, in number and as a share of all candidates?
2. Is the change specific to the University of Ilorin compared with its peers?
3. Where are candidates lost between first choice, the 180 cut-off, Post-UTME screening and admission?
4. Which explanations can public data support or rule out: new universities nearby, insecurity in Kwara, cost, admission rules, changing search interest?

## Headline result so far

First-choice applications to the University of Ilorin fell from 103,582 in 2020 to 52,514 in 2026, a fall of 49.3%. Its share of all applicants fell from 5.31% to 2.34%, and it dropped from first place (2018–2024) to seventh (2026).

Seven universities were in JAMB's top 10 in both 2021 and 2026. Of these, only the University of Ilorin had fewer first-choice applications in 2026 than in 2021: 78,466 down to 52,514 (−33%). The other six rose by between 5% (Federal University Oye-Ekiti) and 42% (Obafemi Awolowo University). Universities that left the top 10 have no published 2026 figure, so they are not part of this comparison.

![Change in first-choice applications, 2021 to 2026, universities in JAMB's top 10 in both years](figures/fig1_change_2021_2026.png)

Figures for 2022 are not established: no source prints a comparable University of Ilorin value for that year. See [docs/phase1_notes.md](docs/phase1_notes.md) for the series, the acceptance rule and the conflicts found in published figures.

## Repository map

```
data/
  raw/                  figures copied as printed, one row per source and value
    applicants_sources.csv       first-choice applicants by institution and UTME year
    funnel_sources.csv           Post-UTME screening and admission, University of Ilorin
    national_totals_sources.csv  national UTME totals by year and measure
  interim/              values after applying the acceptance rule
    peer_panel.csv                    institution-year panel
    unilorin_first_choice_series.csv  University of Ilorin series, 2018–2026
docs/
  phase1_notes.md       Phase 1 notes: sources, rule, series, problems found
  project_plan.md       research questions, data, methods, phases, limitations
  source_log.md         every source_id with outlet, URL and publication date
figures/
  fig1_change_2021_2026.png
src/first_choice/
  series.py             rebuilds the interim tables from data/raw
tests/
  test_series.py
```

## Reproducing the interim tables

```
python -m venv .venv
.venv/Scripts/activate        # Windows; on macOS/Linux: source .venv/bin/activate
pip install -e ".[dev]"
python -m first_choice.series          # compares the built tables with data/interim
python -m first_choice.series --write  # regenerates data/interim
pytest
```

The acceptance rule is stated in the docstring of `src/first_choice/series.py`.

## Status

Phase 1 complete (source collection, first-choice series, peer panel). Phase 2 next (funnel and explanations). See [docs/project_plan.md](docs/project_plan.md).

## Licence

Code is released under the MIT Licence (see [LICENSE](LICENSE)). Data and documentation in `data/`, `docs/` and `figures/` are released under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); the underlying figures remain the statements of JAMB and the outlets cited in [docs/source_log.md](docs/source_log.md).
