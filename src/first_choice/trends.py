"""Google Trends search interest in Nigeria for five universities.

The five terms are requested together so that Google scales them against one
another (0-100, 100 = the highest month of any term). A timeframe longer than
five years returns monthly values.

- data/raw/google_trends_ng.csv: the download as returned, with a header
  comment giving the download date and the exact query. A download is never
  overwritten; delete the file to download again (Google samples searches, so
  a new download can differ slightly).
- data/interim/trends_yearly.csv: yearly mean interest per term and each
  term's share of the five-term total for that year. Months Google marks as
  partial are included and counted in `partial_months`.

    python -m first_choice.trends --download  # fetch data/raw (needs pytrends)
    python -m first_choice.trends             # compare with data/interim
    python -m first_choice.trends --write     # regenerate data/interim
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
import time
from pathlib import Path

import pandas as pd

from first_choice.series import ROOT, compare, write

RAW_TRENDS = ROOT / "data" / "raw" / "google_trends_ng.csv"
TRENDS_YEARLY = ROOT / "data" / "interim" / "trends_yearly.csv"

TERMS = ["Unilorin", "LASU", "UNILAG", "OAU", "KWASU"]
GEO = "NG"
TIMEFRAME = "2019-01-01 2026-10-31"
HL = "en-US"
TZ = -60  # minutes behind UTC as pytrends expects; Nigeria is UTC+1
RETRY_WAITS = [60, 120, 240]  # seconds before each of up to three retries


def query_description() -> str:
    return (
        f"pytrends TrendReq(hl={HL!r}, tz={TZ}).build_payload(kw_list={TERMS!r}, "
        f"cat=0, timeframe={TIMEFRAME!r}, geo={GEO!r}, gprop=''); interest_over_time()"
    )


def download(path: Path = RAW_TRENDS) -> pd.DataFrame:
    """Fetch the raw series; retries after rate limiting, then raises."""
    from pytrends.exceptions import ResponseError, TooManyRequestsError
    from pytrends.request import TrendReq

    attempts = len(RETRY_WAITS) + 1
    for attempt in range(1, attempts + 1):
        try:
            client = TrendReq(hl=HL, tz=TZ)
            client.build_payload(TERMS, cat=0, timeframe=TIMEFRAME, geo=GEO, gprop="")
            data = client.interest_over_time()
            break
        except (TooManyRequestsError, ResponseError) as err:
            if attempt == attempts:
                raise RuntimeError(f"Google Trends failed after {attempts} attempts: {err}") from err
            wait = RETRY_WAITS[attempt - 1]
            print(f"attempt {attempt} failed ({type(err).__name__}); retrying in {wait}s", flush=True)
            time.sleep(wait)
    if data.empty:
        raise RuntimeError("Google Trends returned no data")

    data = data.reset_index().rename(columns={"date": "month"})
    data["month"] = data["month"].dt.strftime("%Y-%m")
    data["isPartial"] = data["isPartial"].astype(bool)
    header = (
        f"# Google Trends, interest over time, Nigeria (geo={GEO}), monthly, terms compared in one request.\n"
        f"# Downloaded {dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.\n"
        f"# Query: {query_description()}\n"
    )
    path.write_text(header + data.to_csv(index=False, lineterminator="\n"), encoding="utf-8", newline="")
    return data


def load_raw(path: Path = RAW_TRENDS) -> pd.DataFrame:
    return pd.read_csv(path, comment="#", dtype={"month": str})


def build_yearly(raw: pd.DataFrame) -> pd.DataFrame:
    raw = raw.copy()
    raw["year"] = raw["month"].str[:4].astype(int)
    partial = raw.groupby("year")["isPartial"].apply(lambda s: s.astype(str).str.lower().eq("true").sum())
    months = raw.groupby("year").size()
    means = raw.groupby("year")[TERMS].mean()
    shares = means.div(means.sum(axis=1), axis=0) * 100
    out = []
    for year in means.index:
        for term in TERMS:
            out.append(
                [year, term, round(means.loc[year, term], 3), round(shares.loc[year, term], 3),
                 int(months[year]), int(partial[year])]
            )
    return pd.DataFrame(
        out, columns=["year", "term", "mean_interest", "share_pct", "months", "partial_months"]
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--download", action="store_true", help="download data/raw/google_trends_ng.csv")
    parser.add_argument("--write", action="store_true", help="regenerate the interim file")
    args = parser.parse_args(argv)

    name = lambda p: p.relative_to(ROOT).as_posix()
    if args.download:
        if RAW_TRENDS.exists():
            print(f"{name(RAW_TRENDS)} exists; delete it to download again")
        else:
            try:
                data = download()
            except RuntimeError as err:
                print(err)
                return 2
            print(f"{name(RAW_TRENDS)}: downloaded ({len(data)} months)")

    tables = {TRENDS_YEARLY: build_yearly(load_raw())}
    if args.write:
        write(tables)
        print(f"{name(TRENDS_YEARLY)}: written")
    diffs = (
        compare(tables[TRENDS_YEARLY], TRENDS_YEARLY, key=["year", "term"])
        if TRENDS_YEARLY.exists()
        else ["file missing"]
    )
    if diffs:
        print(f"{name(TRENDS_YEARLY)}: {len(diffs)} difference(s)")
        for d in diffs:
            print(f"  {d}")
        return 1
    print(f"{name(TRENDS_YEARLY)}: reproduced")
    return 0


if __name__ == "__main__":
    sys.exit(main())
