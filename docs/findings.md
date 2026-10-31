# Findings: UTME demand for the University of Ilorin, 2020–2026

As of 31 October 2026. Each figure cites the table it comes from. Sources for every raw value are listed in [source_log.md](source_log.md); an independent recheck of 38 randomly drawn values found all 38 matched their sources ([phase3_validation.md](phase3_validation.md)).

## Summary

The University of Ilorin was the university most often named as first choice in the Unified Tertiary Matriculation Examination (UTME), ranking first in every year from 2018 to 2024 for which this study has figures. First-choice applications to it halved between 2020 and 2026, and its rank fell from first to seventh. The first part of the fall, in 2021, followed a national fall in UTME scores and was not specific to the university. From 2022 the university drew a shrinking share of the country's qualified candidates while comparable universities gained. The timing and the pattern of gains are most consistent with the loss of the university's reputation for an academic calendar without strikes after it joined the eight-month 2022 strike. New private universities and insecurity do not explain the fall, and the available fee data does not support fees as a cause. The data shows timing and patterns, not candidates' reasons.

## 1. First-choice applications halved and the university fell from first to seventh

| UTME year | First-choice applicants | Share of all candidates | Rank |
|---|---|---|---|
| 2020 | 103,582 | 5.31% | 1 |
| 2021 | 78,466 | | 1 |
| 2022 | not established | | 1 |
| 2023 | 73,749 | | 1 |
| 2024 | 64,143 | | 1 |
| 2025 | 56,758 | 2.79% | 3 |
| 2026 | 52,514 | 2.34% | 7 |

Source: `data/interim/unilorin_first_choice_series.csv`; shares are JAMB's published percentages. Applications fell by 49.3% between 2020 and 2026. No comparable figure for 2022 was published.

## 2. Among its peers, only the University of Ilorin lost applicants

Seven universities were in JAMB's top 10 in both 2021 and 2026. Six gained first-choice applications over that period: Obafemi Awolowo University (+42%), the University of Lagos (+32%), Nnamdi Azikiwe University (+24%), the University of Benin (+11%), the University of Nigeria, Nsukka (+9%) and the Federal University Oye-Ekiti (+5%). The University of Ilorin fell by 33%, from 78,466 to 52,514 (`data/interim/peer_panel.csv`; figure 1). Universities that left the top 10 have no published 2026 figure and are not compared.

## 3. The 2021 fall was national

The number of University of Ilorin first-choice candidates scoring 180 or more in the UTME fell from about 72,000 in 2020 to 28,048 in 2021. Nationally, candidates scoring 180 or more fell from 781,327 to 323,624 over the same year. The university's share of the national 180+ pool was 9.2% in 2020 and 8.7% in 2021 (`data/interim/unilorin_share_180plus.csv`). This part of the fall is not specific to the university.

## 4. From 2022 the university drew far fewer of the country's qualified candidates

Candidates at the university's Post-UTME screening per 100 candidates nationally scoring 200 or more (`data/interim/screening_index.csv`; figure 2):

| UTME year | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| Per 100 | 11.4 | 10.8 | 6.6 (projected) | 4.8 | 3.6 | 3.6–4.8 |

The index is stable in 2020–2021 and falls by about two-thirds by 2024. Admissions stayed at about 13,000 a year (13,429 in 2020/2021; 12,856 in 2024/2025), so competition for a place eased: about 3.4 candidates sat the screening per admission in 2020, against about 1.3 who attended it per admission in 2024. The counts are not defined identically: admissions may include Direct Entry and, in 2020, international candidates (`data/interim/funnel_by_year.csv`).

## 5. Search interest moved towards Kwara State University and Lagos State University

Among five universities searched together on Google in Nigeria, the University of Ilorin's share of search interest fell from 25.3% in 2019 to 14.5% in 2026. It dipped in the strike years 2020 and 2022, recovered in the following year, and then fell every year from 2023 (23.7%, 19.4%, 15.8%, 14.5%). Kwara State University's share rose from 4.8% to 22.6%, with its largest rise in 2022; Lagos State University's rose from 16.3% in 2021 to 24.2% in 2022 and stayed near that level (`data/interim/trends_yearly.csv`; figure 3). Searches are not applications, and searches for the University of Ilorin include those by its own students.

## 6. Universities that stayed open during the 2022 strike gained

The University of Ilorin joined the February–October 2022 national strike of the Academic Staff Union of Universities. Lagos State University and Kwara State University did not (`data/raw/strike_events.csv`). In July 2022 the Lagos governor's education adviser said Lagos State University and two new Lagos universities were oversubscribed in the 2022 UTME because they were not on strike. Lagos State University's first-choice applications rose from below 38,309 in 2021, when it was outside the top 10, to 84,426 in 2026, when it ranked first (`data/interim/peer_panel.csv`). Federal universities that also struck in 2022 gained applications as well, so a strike alone did not reduce demand for them. The University of Ilorin had joined a national strike in 2020 for the first time in 20 years; a former registrar has since said that its "no-strike policy" "attracted admission seekers", referring to 2012–2017 (ThisDay, 16 June 2026; `data/raw/strike_events.csv`, E09). This is an opinion, not data.

## 7. Explanations ruled out or weakly supported

| Explanation | Assessment | Basis |
|---|---|---|
| Fees | Not supported, on limited evidence | One outlet gives its charges as ₦98,350–₦120,000 as of June 2025, below UNILAG (₦170,000–₦190,250) and UNIBEN (₦180,000–₦195,000). This conflicts with the university's revised 2023 charges for new students (₦114,720–₦215,820), whose upper value is above both, so the comparison rests on a single source (`data/raw/fees_sources.csv`) |
| New private universities in Kwara | Unlikely to be a main cause | Eight universities were licensed in Kwara in 2021–2025, but private universities drew under 1.5% of UTME candidates in 2014–2015 (`docs/phase2_notes.md`, Result 4), and three opened only in 2025/2026 (`data/raw/kwara_universities.csv`) |
| Insecurity in Kwara | Too late to explain 2022–2024 | Recorded violence was low until 2024 and rose sharply in 2025 (207 deaths and 177 abductions from 1 January to 7 November 2025) (`data/raw/kwara_insecurity_sources.csv`) |
| Candidates staying closer to home | Cannot be tested | Published 2021 and 2026 state figures use different bases |

## 8. Published admission figures contain errors

Building the series required resolving conflicts between outlets reporting the same JAMB release. A five-year review printed figures shifted by one year; one outlet labelled 2025 figures as 2024; one list printed a value that its own text contradicted; and a value reported by the university for "2022/2023" measured a different JAMB award category (`docs/phase1_notes.md`). JAMB's own policy-meeting documents could not be retrieved.

## Limitations

- Cause. The data shows timing and patterns. A survey of applicants would be needed to establish why candidates chose other universities.
- Sources. Almost all figures are JAMB or university statements as reported in news outlets.
- Gaps. There is no comparable 2022 figure for the university, and Kwara State University's application figures are not published.
- Approximations. The 2020 screening figures (72,000; 46,000) are rounded numbers from a speech; national 200+ counts for 2023 and 2024 are derived from published percentages, and 2025 has two published values.
- Validation. The recheck was carried out by an AI agent, not a human coder.
