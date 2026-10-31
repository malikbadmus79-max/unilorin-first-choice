"""Build the University of Ilorin admission funnel and the screening index.

Inputs: data/raw/funnel_sources.csv, data/raw/national_scores_sources.csv and
data/interim/unilorin_first_choice_series.csv.

Outputs in data/interim:

- funnel_by_year.csv: one row per UTME year 2018-2026. Screening counts are
  UTME candidates only (Direct Entry excluded). Where a year has several
  screening counts, the measure used is the first available of sat,
  attended, registered, unspecified, expected.
- national_200plus.csv: national candidates scoring 200 or more. Published
  counts are used where they exist; otherwise the count is derived as
  published percentage x results total, rounded to a whole candidate. A year
  with two published counts keeps both as low and high.
- screening_index.csv: candidates screened per 100 national 200+ candidates.
  With two national counts, index_low uses the high count and index_high the
  low count.
- unilorin_share_180plus.csv: the University of Ilorin's first-choice 180+
  candidates as a share of national 180+ candidates. A national count missing
  as a single figure is summed from published score bands.

    python -m first_choice.funnel          # compare with data/interim
    python -m first_choice.funnel --write  # regenerate data/interim
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

from first_choice.series import ROOT, UNILORIN_SERIES, compare, write

RAW_FUNNEL = ROOT / "data" / "raw" / "funnel_sources.csv"
RAW_NATIONAL_SCORES = ROOT / "data" / "raw" / "national_scores_sources.csv"
INTERIM = ROOT / "data" / "interim"
FUNNEL_BY_YEAR = INTERIM / "funnel_by_year.csv"
NATIONAL_200PLUS = INTERIM / "national_200plus.csv"
SCREENING_INDEX = INTERIM / "screening_index.csv"
SHARE_180PLUS = INTERIM / "unilorin_share_180plus.csv"

YEARS = range(2018, 2027)

# Screening stages (UTME candidates only) and the measure each one reports.
# "registered" covers candidates who applied or registered for screening.
# S02's count is not stated as registered or attended, so it is "unspecified".
SCREENING_STAGES = {
    "Post-UTME candidates who sat": "sat",
    "Post-UTME candidates who attended": "attended",
    "Post-UTME registered": "registered",
    "Post-UTME applicants": "registered",
    "Post-UTME screening applicants": "registered",
    "Post-UTME screening candidates, UTME": "registered",
    "Post-UTME candidates, UTME": "registered",
    "Post-UTME screening candidates": "unspecified",
    "Post-UTME candidates expected to sit": "expected",
}
MEASURE_PREFERENCE = ["sat", "attended", "registered", "unspecified", "expected"]

FIRST_CHOICE_180PLUS_STAGES = {
    "UTME candidates with 180 and above, first choice",
    "First-choice candidates scoring 180 and above",
}
ADMITTED_STAGES = {"Admitted"}
MATRICULATED_STAGES = {"Matriculated"}

# National 180+ counts summed from bands where no single figure is published.
BANDS_180PLUS = ["200 and above", "190-199", "180-189"]

FUNNEL_COLUMNS = [
    "utme_year",
    "first_choice",
    "first_choice_180plus",
    "screened",
    "screened_measure",
    "admitted",
    "matriculated",
    "sources",
]


def load_funnel(path: Path = RAW_FUNNEL) -> pd.DataFrame:
    df = pd.read_csv(path, dtype={"source_id": str}, keep_default_na=False, na_values={"count": [""]})
    df["count"] = df["count"].astype("Int64")
    df["file_order"] = range(len(df))
    return df


def load_national_scores(path: Path = RAW_NATIONAL_SCORES) -> pd.DataFrame:
    df = pd.read_csv(
        path,
        dtype={"source_id": str},
        keep_default_na=False,
        na_values={"count": [""], "percent": [""], "total_base": [""]},
    )
    df["count"] = df["count"].astype("Int64")
    df["total_base"] = df["total_base"].astype("Int64")
    df["file_order"] = range(len(df))
    return df


def join_ids(ids) -> str:
    return ";".join(dict.fromkeys(i for i in ids if i))


def stage_value(rows: pd.DataFrame, stages: set[str]) -> tuple:
    """First value printed for any of the stages, with the sources that print it."""
    match = rows[rows["stage"].isin(stages) & rows["count"].notna()].sort_values("file_order")
    if match.empty:
        return pd.NA, []
    value = match["count"].iloc[0]
    return value, list(match.loc[match["count"] == value, "source_id"])


def screening_value(rows: pd.DataFrame) -> tuple:
    """Screening count by measure preference; returns (count, measure, sources)."""
    screening = rows[rows["stage"].isin(SCREENING_STAGES) & rows["count"].notna()].copy()
    screening["measure"] = screening["stage"].map(SCREENING_STAGES)
    for measure in MEASURE_PREFERENCE:
        match = screening[screening["measure"] == measure].sort_values("file_order")
        if not match.empty:
            value = match["count"].iloc[0]
            return value, measure, list(match.loc[match["count"] == value, "source_id"])
    return pd.NA, "", []


def build_funnel(funnel: pd.DataFrame, series: pd.DataFrame) -> pd.DataFrame:
    series = series.set_index("utme_year")
    out = []
    for year in YEARS:
        rows = funnel[funnel["utme_year"] == year]
        first_choice, fc_sources = pd.NA, []
        if year in series.index and pd.notna(series.loc[year, "first_choice_applicants"]):
            first_choice = series.loc[year, "first_choice_applicants"]
            fc_sources = series.loc[year, "sources"].split(";")
        fc180, fc180_sources = stage_value(rows, FIRST_CHOICE_180PLUS_STAGES)
        screened, measure, screened_sources = screening_value(rows)
        admitted, admitted_sources = stage_value(rows, ADMITTED_STAGES)
        matriculated, matric_sources = stage_value(rows, MATRICULATED_STAGES)
        sources = join_ids(fc_sources + fc180_sources + screened_sources + admitted_sources + matric_sources)
        out.append([year, first_choice, fc180, screened, measure, admitted, matriculated, sources])
    df = pd.DataFrame(out, columns=FUNNEL_COLUMNS)
    for c in ("first_choice", "first_choice_180plus", "screened", "admitted", "matriculated"):
        df[c] = df[c].astype("Int64")
    return df


def build_national_200plus(scores: pd.DataFrame) -> pd.DataFrame:
    rows = scores[scores["band"] == "200 and above"].sort_values("file_order")
    out = []
    for year, group in rows.groupby("utme_year", sort=True):
        published = group[group["count"].notna()]
        if not published.empty:
            counts = sorted(dict.fromkeys(int(c) for c in published["count"]))
            low, high = counts[0], counts[-1]
            value = low if low == high else pd.NA
            method = "published" if low == high else "published (two values)"
            used = published
        else:
            derivable = group[group["percent"].notna() & group["total_base"].notna()]
            if derivable.empty:
                continue
            r = derivable.iloc[0]
            low = high = value = round(r["percent"] / 100 * int(r["total_base"]))
            method = f"derived ({r['percent']:g}% x {int(r['total_base']):,})"
            used = derivable.head(1)
        notes = "; ".join(n for n in used["notes"] if n)
        out.append([year, value, low, high, method, join_ids(used["source_id"]), notes])
    df = pd.DataFrame(
        out,
        columns=[
            "utme_year",
            "national_200plus",
            "national_200plus_low",
            "national_200plus_high",
            "method",
            "sources",
            "notes",
        ],
    )
    for c in ("national_200plus", "national_200plus_low", "national_200plus_high"):
        df[c] = df[c].astype("Int64")
    return df


def build_screening_index(funnel: pd.DataFrame, national: pd.DataFrame) -> pd.DataFrame:
    df = funnel[["utme_year", "screened", "screened_measure"]].merge(national, on="utme_year", how="inner")
    df = df[df["screened"].notna()].copy()
    per_100 = lambda num, den: (num.astype(float) / den.astype(float) * 100).round(3)
    df["index"] = per_100(df["screened"], df["national_200plus"])
    df["index_low"] = per_100(df["screened"], df["national_200plus_high"])
    df["index_high"] = per_100(df["screened"], df["national_200plus_low"])
    return df[
        [
            "utme_year",
            "screened",
            "screened_measure",
            "national_200plus",
            "national_200plus_low",
            "national_200plus_high",
            "index",
            "index_low",
            "index_high",
        ]
    ].reset_index(drop=True)


def build_share_180plus(funnel: pd.DataFrame, raw_funnel: pd.DataFrame, scores: pd.DataFrame) -> pd.DataFrame:
    out = []
    for year in (2020, 2021):
        unilorin, unilorin_sources = stage_value(raw_funnel[raw_funnel["utme_year"] == year], FIRST_CHOICE_180PLUS_STAGES)
        year_scores = scores[(scores["utme_year"] == year) & scores["count"].notna()]
        single = year_scores[year_scores["band"] == "180 and above"]
        if not single.empty:
            national, national_sources, method = int(single["count"].iloc[0]), list(single["source_id"]), "published"
        else:
            bands = year_scores[year_scores["band"].isin(BANDS_180PLUS)]
            assert set(bands["band"]) == set(BANDS_180PLUS), f"{year}: missing 180+ bands"
            national = int(bands["count"].sum())
            national_sources = list(bands["source_id"])
            method = "sum of bands " + " + ".join(f"{int(c):,}" for c in bands["count"])
        share = round(int(unilorin) / national * 100, 3)
        out.append([year, int(unilorin), national, share, method, join_ids(unilorin_sources + national_sources)])
    return pd.DataFrame(
        out, columns=["utme_year", "unilorin_180plus", "national_180plus", "share_pct", "national_method", "sources"]
    )


def build_all() -> dict[Path, pd.DataFrame]:
    raw_funnel = load_funnel()
    scores = load_national_scores()
    series = pd.read_csv(UNILORIN_SERIES, dtype={"sources": str}, keep_default_na=False, na_values={"first_choice_applicants": [""]})
    series["first_choice_applicants"] = series["first_choice_applicants"].astype("Int64")
    funnel = build_funnel(raw_funnel, series)
    national = build_national_200plus(scores)
    return {
        FUNNEL_BY_YEAR: funnel,
        NATIONAL_200PLUS: national,
        SCREENING_INDEX: build_screening_index(funnel, national),
        SHARE_180PLUS: build_share_180plus(funnel, raw_funnel, scores),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="regenerate the interim files")
    args = parser.parse_args(argv)

    tables = build_all()
    if args.write:
        write(tables)
        for path, table in tables.items():
            print(f"{path.relative_to(ROOT).as_posix()}: written ({len(table)} rows)")
    changed = False
    for path, table in tables.items():
        name = path.relative_to(ROOT).as_posix()
        diffs = compare(table, path) if path.exists() else ["file missing"]
        if diffs:
            changed = True
            print(f"{name}: {len(diffs)} difference(s)")
            for d in diffs:
                print(f"  {d}")
        else:
            print(f"{name}: reproduced")
    return 1 if changed else 0


if __name__ == "__main__":
    sys.exit(main())
