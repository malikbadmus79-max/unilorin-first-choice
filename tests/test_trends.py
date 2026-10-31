import pandas as pd
import pytest

from first_choice import trends


@pytest.fixture(scope="module")
def yearly():
    return pd.read_csv(trends.TRENDS_YEARLY)


def test_all_terms_and_years(yearly):
    assert set(yearly["term"]) == set(trends.TERMS)
    for term, rows in yearly.groupby("term"):
        assert sorted(rows["year"]) == list(range(2019, 2027)), term


def test_shares_sum_to_100(yearly):
    totals = yearly.groupby("year")["share_pct"].sum()
    assert totals.sub(100).abs().max() < 0.01


def test_interim_matches_raw(yearly):
    built = trends.build_yearly(trends.load_raw())
    pd.testing.assert_frame_equal(built.round(3), yearly, check_dtype=False)
