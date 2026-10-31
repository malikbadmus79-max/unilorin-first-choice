"""Draw the project figures from the interim tables.

- figures/fig1_change_2021_2026.png/.svg from data/interim/peer_panel.csv
- figures/fig2_screening_share.png/.svg from data/interim/screening_index.csv
  and data/raw/strike_events.csv
- figures/fig3_search_share.png/.svg from data/interim/trends_yearly.csv
  and data/raw/strike_events.csv

Uses Inter from assets/fonts/ (or an installed copy), otherwise the first
available fallback font.

    python -m first_choice.figures
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib import font_manager  # noqa: E402

from first_choice.funnel import SCREENING_INDEX  # noqa: E402
from first_choice.series import PEER_PANEL, RAW_APPLICANTS, ROOT, UNILORIN, load_sources  # noqa: E402
from first_choice.trends import RAW_TRENDS, TERMS, TRENDS_YEARLY  # noqa: E402

FIGURES = ROOT / "figures"
RAW_STRIKES = ROOT / "data" / "raw" / "strike_events.csv"
FONTS = ROOT / "assets" / "fonts"

BLUE = "#2a78d6"
ORANGE = "#eb6834"
BACKGROUND = "#f7f4ee"
BAND = "#e2ddd2"
INK = "#1a1a1a"
MUTED = "#555555"
FAINT = "#888888"
GRID = "#dedad2"

# Figure 3: Unilorin highlighted, LASU in blue, the other terms in greys.
TERM_COLOURS = {"Unilorin": ORANGE, "LASU": BLUE, "UNILAG": "#6f6f6f", "OAU": "#a3a3a3", "KWASU": "#4a4a4a"}

FONT_PREFERENCE = ["Inter", "Segoe UI", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
DPI = 200

SHORT_NAMES = {
    "University of Ilorin": "Unilorin",
    "University of Lagos": "UNILAG",
    "Obafemi Awolowo University": "OAU",
    "Nnamdi Azikiwe University": "UNIZIK",
    "University of Benin": "UNIBEN",
    "University of Nigeria, Nsukka": "UNN",
    "Federal University Oye-Ekiti": "FUOYE",
    "Ahmadu Bello University": "ABU",
    "Bayero University Kano": "Bayero",
    "University of Jos": "Jos",
    "Lagos State University": "LASU",
    "University of Ibadan": "UI",
    "University of Port Harcourt": "UNIPORT",
}

# Footnote wording for screening measures.
MEASURE_NOUNS = {"registered": "registrants", "sat": "candidates who sat"}

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def register_fonts(directory: Path = FONTS) -> list[str]:
    """Add the bundled fonts to matplotlib; returns the family names registered."""
    names = []
    for path in sorted(directory.glob("*.ttf")):
        font_manager.fontManager.addfont(str(path))
        names.append(font_manager.FontProperties(fname=path).get_name())
    return list(dict.fromkeys(names))


def pick_font() -> str:
    register_fonts()
    installed = {f.name for f in font_manager.fontManager.ttflist}
    return next(name for name in FONT_PREFERENCE if name in installed or name == "DejaVu Sans")


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": pick_font(),
            "figure.facecolor": BACKGROUND,
            "axes.facecolor": BACKGROUND,
            "savefig.facecolor": BACKGROUND,
            "text.color": INK,
            "axes.edgecolor": GRID,
            "xtick.color": INK,
            "ytick.color": INK,
            "svg.hashsalt": "first_choice",
        }
    )


def header(fig, title: str, subtitle: str, x: float = 0.02) -> None:
    fig.text(x, 0.965, title, fontsize=15, fontweight="bold", va="top")
    fig.text(x, 0.905, subtitle, fontsize=11, color=MUTED, va="top")


def footer(fig, note: str, source: str, x: float = 0.02) -> None:
    fig.text(x, 0.045, note, fontsize=8.5, color=MUTED, va="bottom")
    fig.text(x, 0.015, source, fontsize=8, color=FAINT, va="bottom")


def save(fig, stem: str) -> list[Path]:
    paths = [FIGURES / f"{stem}.png", FIGURES / f"{stem}.svg"]
    FIGURES.mkdir(exist_ok=True)
    fig.savefig(paths[0], dpi=DPI, metadata={"Software": None})
    fig.savefig(paths[1], metadata={"Date": None})
    plt.close(fig)
    return paths


def fig1_change_2021_2026(panel: pd.DataFrame, sources: pd.DataFrame) -> list[Path]:
    """Change 2021-2026 for universities in JAMB's top 10 in both years."""
    y0, y1 = 2021, 2026
    a = panel[panel["utme_year"] == y0].set_index("institution")
    b = panel[panel["utme_year"] == y1].set_index("institution")
    both = [i for i in a.index if i in b.index]
    left = [SHORT_NAMES.get(i, i) for i in a.index if i not in b.index]
    df = pd.DataFrame(
        {
            "start": a.loc[both, "first_choice_applicants"].astype(int),
            "end": b.loc[both, "first_choice_applicants"].astype(int),
        }
    )
    df["change"] = (df["end"] / df["start"] - 1) * 100
    df = df.sort_values("change")

    used = set(";".join(a.loc[both, "sources"]).split(";")) | set(";".join(b.loc[both, "sources"]).split(";"))
    outlets = list(dict.fromkeys(sources.loc[sources["source_id"].isin(used)].sort_values("file_order")["outlet"]))

    fig = plt.figure(figsize=(9, 5.4))
    ax = fig.add_axes([0.13, 0.14, 0.80, 0.72])
    colours = [ORANGE if i == UNILORIN else BLUE for i in df.index]
    ypos = range(len(df))
    ax.barh(ypos, df["change"], color=colours, height=0.62, zorder=2)
    ax.axvline(0, color=FAINT, linewidth=1.2, zorder=3)
    for y, (inst, r) in zip(ypos, df.iterrows()):
        label = f"{r['change']:+.0f}%  ({int(r['start']):,} → {int(r['end']):,})".replace("-", "−", 1)
        offset = 1.5 if r["change"] >= 0 else -1.5
        ax.text(r["change"] + offset, y, label, va="center", ha="left" if r["change"] >= 0 else "right", fontsize=11)
    ax.set_yticks(list(ypos), [SHORT_NAMES.get(i, i) for i in df.index], fontsize=12, fontweight="bold")
    span = max(df["change"].max(), -df["change"].min())
    ax.set_xlim(-span * 2.2, span * 2.0)
    ax.set_xticks([])
    ax.tick_params(axis="y", length=0, pad=10)
    for s in ax.spines.values():
        s.set_visible(False)

    n_top = len(a)
    header(
        fig,
        "Only Unilorin lost first-choice applicants among its top-10 peers",
        f"Change in first-choice UTME applications, {y0} to {y1}. "
        f"Universities in JAMB's top 10 in both years ({len(both)} of {n_top}).",
    )
    footer(
        fig,
        f"Universities that left the top 10 ({', '.join(left)}) have no published {y1} figure and are not shown.",
        f"Source: JAMB policy-meeting figures as reported by {', '.join(outlets)} (data/interim/peer_panel.csv).",
    )
    return save(fig, "fig1_change_2021_2026")


def month_position(value: str, end: bool = False) -> float:
    """Calendar position of 'YYYY-MM' or 'YYYY-MM-DD' in years; end=True gives the end of the month."""
    year, month = int(value[:4]), int(value[5:7])
    return year + (month - (0 if end else 1)) / 12


def strike_bands(strikes: pd.DataFrame) -> list[tuple[float, float, str]]:
    """Completed national strikes the University of Ilorin joined."""
    rows = strikes[
        (strikes["institution"] == UNILORIN)
        & (strikes["joined"] == "yes")
        & (strikes["scope"] == "ASUU national strike")
        & (strikes["end"] != "")
    ]
    bands = []
    for _, r in rows.iterrows():
        start, end = r["start"], r["end"]
        label = f"Strike {MONTHS[int(start[5:7]) - 1]}–{MONTHS[int(end[5:7]) - 1]} {end[:4]}"
        bands.append((month_position(start), month_position(end, end=True), label))
    return bands


def fig2_screening_share(index: pd.DataFrame, strikes: pd.DataFrame) -> list[Path]:
    """Screening index by UTME year, with the national strikes the university joined."""
    df = index.copy()
    df["value"] = df["index"].fillna(df["index_low"])
    # UTME sittings fall in March-May; points sit at the start of April.
    df["x"] = df["utme_year"] + 0.25

    fig = plt.figure(figsize=(9, 5.2))
    ax = fig.add_axes([0.06, 0.12, 0.92, 0.60])
    top = 13
    for x0, x1, label in strike_bands(strikes):
        ax.axvspan(x0, x1, color=BAND, zorder=0, linewidth=0)
        ax.text((x0 + x1) / 2, top * 1.08, label, ha="center", va="bottom", fontsize=10, color=MUTED, clip_on=False)
    ax.plot(df["x"], df["value"], color=BLUE, linewidth=2.5, zorder=2)
    for _, r in df.iterrows():
        hollow = r["screened_measure"] == "expected"
        ax.plot(
            r["x"], r["value"], "o", markersize=9, zorder=3,
            markerfacecolor="white" if hollow else BLUE, markeredgecolor=BLUE, markeredgewidth=2,
        )
        label = f"{r['value']:.1f}"
        if hollow:
            label += " (expected)"
        elif pd.isna(r["index"]):
            label += " (lower bound)"
        ax.annotate(label, (r["x"], r["value"]), xytext=(0, 12), textcoords="offset points",
                    ha="center", fontsize=11, fontweight="bold")
    ax.set_xticks(df["x"], df["utme_year"].astype(str), fontsize=11)
    ax.set_xlim(df["x"].min() - 0.4, df["x"].max() + 0.5)
    ax.set_ylim(0, top)
    ax.set_yticks([0, 4, 8, 12])
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=11)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)

    header(
        fig,
        "After 2022, Unilorin drew far fewer of Nigeria's qualified candidates",
        "Candidates at Unilorin's Post-UTME screening per 100 candidates nationally scoring 200+ in UTME",
    )
    notes = []
    for _, r in df.iterrows():
        if r["screened_measure"] == "expected":
            notes.append(f"{r['utme_year']}: projected attendance (about {r['screened']:,}).")
        if pd.isna(r["index"]):
            notes.append(
                f"{r['utme_year']}: {r['screened']:,} UTME {MEASURE_NOUNS.get(r['screened_measure'], r['screened_measure'])}; range "
                f"{r['index_low']:.1f}–{r['index_high']:.1f} depending on the national 200+ count used."
            )
    footer(
        fig,
        " ".join(notes),
        "Sources: data/raw/funnel_sources.csv, data/raw/national_scores_sources.csv. "
        "National 200+ counts for 2023–24 derived from published percentages.",
    )
    return save(fig, "fig2_screening_share")


def spread_labels(values: dict[str, float], gap: float) -> dict[str, float]:
    """Label positions at least `gap` apart, kept as close to the values as possible."""
    order = sorted(values, key=values.get)
    pos = {k: values[k] for k in order}
    for _ in range(50):
        moved = False
        for lo, hi in zip(order, order[1:]):
            if pos[hi] - pos[lo] < gap:
                shift = (gap - (pos[hi] - pos[lo])) / 2
                pos[lo] -= shift
                pos[hi] += shift
                moved = True
        if not moved:
            break
    return pos


def raw_download_date(path: Path = RAW_TRENDS) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# Downloaded "):
            return line.removeprefix("# Downloaded ").split()[0]
    return "date not recorded"


def fig3_search_share(yearly: pd.DataFrame, strikes: pd.DataFrame) -> list[Path]:
    """Yearly share of Google search interest among the five terms."""
    shares = yearly.pivot(index="year", columns="term", values="share_pct")[TERMS]
    x = shares.index + 0.5  # yearly averages sit mid-year
    last = shares.index.max()

    fig = plt.figure(figsize=(9, 5.2))
    ax = fig.add_axes([0.06, 0.12, 0.80, 0.60])
    top = 40
    for x0, x1, label in strike_bands(strikes):
        if int(x0) != 2022:
            continue
        ax.axvspan(x0, x1, color=BAND, zorder=0, linewidth=0)
        ax.text((x0 + x1) / 2, top * 1.04, label, ha="center", va="bottom", fontsize=10, color=MUTED, clip_on=False)
    for term in reversed(TERMS):
        unilorin = term == "Unilorin"
        ax.plot(x, shares[term], color=TERM_COLOURS[term], linewidth=3 if unilorin else 2,
                zorder=4 if unilorin else 2, marker="o", markersize=5 if unilorin else 3.5)
    ends = spread_labels({t: shares.loc[last, t] for t in TERMS}, gap=2.1)
    for term in TERMS:
        ax.annotate(
            f"{term} {shares.loc[last, term]:.0f}%", (last + 0.5, ends[term]), xytext=(8, 0),
            textcoords="offset points", va="center", fontsize=10.5, color=TERM_COLOURS[term],
            fontweight="bold" if term == "Unilorin" else "normal", annotation_clip=False,
        )
    first = shares.index.min()
    ax.annotate(f"{shares.loc[first, 'Unilorin']:.0f}%", (first + 0.5, shares.loc[first, "Unilorin"]),
                xytext=(0, 9), textcoords="offset points", ha="center", fontsize=10.5,
                fontweight="bold", color=ORANGE)
    ax.set_xticks(x, shares.index.astype(str), fontsize=11)
    ax.set_xlim(first + 0.2, last + 0.8)
    ax.set_ylim(0, top)
    ax.set_yticks([0, 10, 20, 30, 40], ["0", "10", "20", "30", "40%"])
    ax.yaxis.grid(True, color=GRID, linewidth=1)
    ax.set_axisbelow(True)
    ax.tick_params(length=0, labelsize=11)
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)

    rows = yearly[yearly["year"] == last].iloc[0]
    coverage = f"{last} covers {rows['months']} months" + (
        f" ({rows['partial_months']} partial)" if rows["partial_months"] else ""
    )
    header(
        fig,
        f"Unilorin's share of searches fell from {shares.loc[first, 'Unilorin']:.1f}% to "
        f"{shares.loc[last, 'Unilorin']:.1f}%, {first}–{last}",
        "Share of Google search interest in Nigeria among five university names, yearly average of monthly values",
    )
    footer(
        fig,
        f"Search terms, not topics, compared in one request. {coverage}.",
        f"Source: Google Trends via pytrends, downloaded {raw_download_date()} (data/raw/google_trends_ng.csv).",
    )
    return save(fig, "fig3_search_share")


def main() -> int:
    style()
    panel = pd.read_csv(PEER_PANEL, keep_default_na=False)
    index = pd.read_csv(SCREENING_INDEX)
    strikes = pd.read_csv(RAW_STRIKES, dtype=str, keep_default_na=False)
    sources = load_sources(RAW_APPLICANTS)
    yearly = pd.read_csv(TRENDS_YEARLY)
    print(f"font: {plt.rcParams['font.family'][0]}")
    paths = (
        fig1_change_2021_2026(panel, sources)
        + fig2_screening_share(index, strikes)
        + fig3_search_share(yearly, strikes)
    )
    for path in paths:
        print(f"{path.relative_to(ROOT).as_posix()}: written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
