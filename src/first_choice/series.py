"""Build the interim first-choice tables from the raw source table.

Input: data/raw/applicants_sources.csv, one row per value as printed.
Output: data/interim/peer_panel.csv and
data/interim/unilorin_first_choice_series.csv.

Rule, applied to each UTME year and institution:

(a) Accepted: two or more independent outlets print the same value.
    S09 (different measure) and S17 (year-shifted) are excluded.
(b) Rank-consistent: sources disagree, no value reaches two outlets, and
    exactly one value is consistent with the published rank order within
    its own source list. A value that would place an institution above a
    higher-ranked institution in the same list is rejected. The reason is
    recorded in notes.
(c) Single source: otherwise, the value printed by the first source in the
    raw file.
(d) Not established: University of Ilorin years with no usable value.

Notes are generated from the data: values from other sources that differ
from the kept value, including excluded sources, and the reason for any
rank-order decision. Hand-written notes in CURATED_NOTES are placed first
("curated; generated"); a part repeated or contained in another is dropped.

    python -m first_choice.series          # compare with data/interim
    python -m first_choice.series --write  # regenerate data/interim
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_APPLICANTS = ROOT / "data" / "raw" / "applicants_sources.csv"
PEER_PANEL = ROOT / "data" / "interim" / "peer_panel.csv"
UNILORIN_SERIES = ROOT / "data" / "interim" / "unilorin_first_choice_series.csv"

UNILORIN = "University of Ilorin"
EXCLUDED_SOURCES = {"S09": "different measure", "S17": "year-shifted"}
MIN_OUTLETS = 2

# Hand-written notes from Phase 1, keyed by (table, utme_year, institution).
CURATED_NOTES = {
    ("series", 2018, UNILORIN): "Not verified; one outlet",
    ("series", 2019, UNILORIN): "Not verified; Unilorin statement only",
    ("series", 2021, UNILORIN): "S05 gives 76,466 in an ambiguous sentence",
    ("series", 2022, UNILORIN): "S09's 97,351 is a different JAMB award measure; S17's 78,466 repeats the 2021 value",
    ("series", 2024, UNILORIN): "S11 list prints 63,143 but its body says 64,143",
    ("series", 2025, UNILORIN): "S17 gives 56,734",
    ("series", 2026, UNILORIN): "S17 gives 56,758, the 2025 value",
}

ACCEPTED = "accepted"
RANK_CONSISTENT = "rank-consistent"
SINGLE_SOURCE = "single source"
NOT_ESTABLISHED = "not established"

PEER_COLUMNS = ["utme_year", "institution", "first_choice_applicants", "sources", "n", "status", "notes"]
SERIES_COLUMNS = [
    "utme_year",
    "first_choice_applicants",
    "share_of_applicants_pct",
    "sources",
    "n_agreeing_sources",
    "status",
    "notes",
]


def load_sources(path: Path = RAW_APPLICANTS) -> pd.DataFrame:
    """Read the raw table, keeping shares and dates as printed."""
    df = pd.read_csv(
        path,
        dtype={"source_id": str, "share_of_applicants_pct": str, "publication_date": str},
        keep_default_na=False,
        na_values={"first_choice_applicants": [""], "rank": [""]},
    )
    df["first_choice_applicants"] = df["first_choice_applicants"].astype("Int64")
    df["rank"] = df["rank"].astype("Int64")
    df["file_order"] = range(len(df))
    return df


def usable(sources: pd.DataFrame) -> pd.DataFrame:
    """Rows from non-excluded sources that print a value."""
    keep = ~sources["source_id"].isin(EXCLUDED_SOURCES) & sources["first_choice_applicants"].notna()
    return sources[keep]


def fmt(value) -> str:
    return f"{int(value):,}"


def rank_violation(row: pd.Series, sources: pd.DataFrame) -> pd.Series | None:
    """A higher-ranked institution in the same source list that this value would rank above."""
    if pd.isna(row["rank"]):
        return None
    same_list = sources[
        (sources["source_id"] == row["source_id"])
        & (sources["utme_year"] == row["utme_year"])
        & (sources["rank"] < row["rank"])
        & (sources["first_choice_applicants"] < row["first_choice_applicants"])
    ]
    return None if same_list.empty else same_list.sort_values("rank").iloc[0]


def resolve(rows: pd.DataFrame, sources: pd.DataFrame) -> dict:
    """Apply rules (a) to (c) to the usable rows for one institution-year."""
    candidates = []
    for value, group in rows.groupby("first_choice_applicants", sort=False):
        group = group.sort_values("file_order")
        candidates.append({"value": int(value), "rows": group, "n_outlets": group["outlet"].nunique()})
    candidates.sort(key=lambda c: c["rows"]["file_order"].min())

    best = max(candidates, key=lambda c: c["n_outlets"])
    reasons = []
    if best["n_outlets"] >= MIN_OUTLETS:
        status, kept, agreeing = ACCEPTED, best, best["rows"]
    else:
        consistent = []
        for c in candidates:
            violations = [(r, rank_violation(r, sources)) for _, r in c["rows"].iterrows()]
            violations = [(r, v) for r, v in violations if v is not None]
            if violations:
                r, v = violations[0]
                reasons.append(
                    f"{r['source_id']}'s {fmt(r['first_choice_applicants'])} rejected: would rank above "
                    f"{v['institution']} (rank {v['rank']}, {fmt(v['first_choice_applicants'])}) in the same list"
                )
            else:
                consistent.append(c)
        if len(candidates) > 1 and len(consistent) == 1:
            status, kept = RANK_CONSISTENT, consistent[0]
        else:
            status, kept, reasons = SINGLE_SOURCE, candidates[0], []
        agreeing = kept["rows"].head(1) if status == SINGLE_SOURCE else kept["rows"]

    return {
        "value": kept["value"],
        "rows": agreeing,
        "sources": ";".join(agreeing["source_id"]),
        "n": len(agreeing),
        "status": status,
        "reasons": reasons,
    }


def other_values_note(mentions: pd.DataFrame, kept_value, kept_sources: set[str]) -> list[str]:
    """Describe values printed by other sources that differ from the kept value."""
    notes = []
    for _, r in mentions.sort_values("file_order").iterrows():
        v = r["first_choice_applicants"]
        if pd.isna(v) or v == kept_value:
            continue
        sid = r["source_id"]
        text = f"{sid} {'also gives' if sid in kept_sources else 'gives'} {fmt(v)}"
        if sid in EXCLUDED_SOURCES:
            text += f" (excluded: {EXCLUDED_SOURCES[sid]})"
        notes.append(text)
    return notes


def merge_notes(table: str, year: int, institution: str, generated: list[str]) -> str:
    """Curated notes first, then generated ones; drop parts repeated or contained in another part."""
    curated = CURATED_NOTES.get((table, year, institution), "")
    parts = [p.strip() for p in curated.split(";") if p.strip()] + generated
    kept = []
    for i, p in enumerate(parts):
        duplicate = p in parts[:i]
        contained = any(p != q and p in q for q in parts)
        if not duplicate and not contained:
            kept.append(p)
    return "; ".join(kept)


def resolve_cell(mentions: pd.DataFrame, sources: pd.DataFrame) -> dict | None:
    """Resolve one institution-year from all rows that mention it, with notes."""
    rows = usable(mentions)
    if rows.empty:
        return None
    r = resolve(rows, sources)
    kept_sources = set(r["rows"]["source_id"])
    if r["status"] == RANK_CONSISTENT:
        # Values rejected by rank order are explained by the reasons instead.
        notes = r["reasons"]
    else:
        notes = other_values_note(mentions, r["value"], kept_sources)
    r["notes"] = notes
    return r


def build_peer_panel(sources: pd.DataFrame) -> pd.DataFrame:
    """One row per institution-year with a usable value."""
    keys = usable(sources).sort_values("file_order")[["utme_year", "institution"]].drop_duplicates()
    keys = keys.sort_values("utme_year", kind="stable")
    out = []
    for year, institution in keys.itertuples(index=False):
        mentions = sources[(sources["utme_year"] == year) & (sources["institution"] == institution)]
        r = resolve_cell(mentions, sources)
        notes = merge_notes("peer_panel", year, institution, r["notes"])
        out.append([year, institution, r["value"], r["sources"], r["n"], r["status"], notes])
    panel = pd.DataFrame(out, columns=PEER_COLUMNS)
    panel["first_choice_applicants"] = panel["first_choice_applicants"].astype("Int64")
    return panel


def build_unilorin_series(sources: pd.DataFrame) -> pd.DataFrame:
    """One row per UTME year in which any source mentions the University of Ilorin."""
    unilorin = sources[sources["institution"] == UNILORIN]
    out = []
    for year in sorted(unilorin["utme_year"].unique()):
        mentions = unilorin[unilorin["utme_year"] == year].sort_values("file_order")
        r = resolve_cell(mentions, sources)
        if r is None:
            notes = merge_notes("series", year, UNILORIN, other_values_note(mentions, None, set()))
            out.append([year, pd.NA, "", ";".join(mentions["source_id"]), 0, NOT_ESTABLISHED, notes])
            continue
        notes = merge_notes("series", year, UNILORIN, r["notes"])
        shares = [s for s in r["rows"]["share_of_applicants_pct"] if s]
        out.append([year, r["value"], shares[0] if shares else "", r["sources"], r["n"], r["status"], notes])
    series = pd.DataFrame(out, columns=SERIES_COLUMNS)
    series["first_choice_applicants"] = series["first_choice_applicants"].astype("Int64")
    return series


def to_csv_text(df: pd.DataFrame) -> str:
    return df.to_csv(index=False, lineterminator="\n")


def compare(built: pd.DataFrame, path: Path) -> list[str]:
    """Differences between a built table and the file on disk, as text lines."""
    read = lambda f: pd.read_csv(f, dtype=str, keep_default_na=False)
    new = read(io.StringIO(to_csv_text(built)))
    old = read(path)
    diffs = []
    for c in old.columns.difference(new.columns, sort=False):
        diffs.append(f"column {c!r} dropped")
    for c in new.columns.difference(old.columns, sort=False):
        diffs.append(f"column {c!r} added")
    key = [c for c in ("utme_year", "institution") if c in old.columns]
    shared = [c for c in old.columns if c in new.columns and c not in key]
    merged = old.merge(new, on=key, how="outer", suffixes=("_existing", "_built"), indicator=True)
    for _, row in merged.iterrows():
        label = ", ".join(str(row[k]) for k in key)
        if row["_merge"] != "both":
            where = "existing only" if row["_merge"] == "left_only" else "built only"
            diffs.append(f"{label}: row in {where}")
            continue
        for c in shared:
            a, b = row[f"{c}_existing"], row[f"{c}_built"]
            if a != b:
                diffs.append(f"{label}: {c} existing {a!r} vs built {b!r}")
    return diffs


def build_all(sources_path: Path = RAW_APPLICANTS) -> dict[Path, pd.DataFrame]:
    sources = load_sources(sources_path)
    return {PEER_PANEL: build_peer_panel(sources), UNILORIN_SERIES: build_unilorin_series(sources)}


def write(tables: dict[Path, pd.DataFrame]) -> None:
    for path, table in tables.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(to_csv_text(table), encoding="utf-8", newline="")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="regenerate the interim files")
    args = parser.parse_args(argv)

    tables = build_all()
    if args.write:
        write(tables)
        for path in tables:
            print(f"{path.relative_to(ROOT).as_posix()}: written")
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
