import pandas as pd
import pytest

from first_choice import series


@pytest.fixture(scope="module")
def sources():
    return series.load_sources()


@pytest.fixture(scope="module")
def unilorin(sources):
    return series.build_unilorin_series(sources).set_index("utme_year")


@pytest.fixture(scope="module")
def panel(sources):
    return series.build_peer_panel(sources).set_index(["utme_year", "institution"])


def test_every_row_has_source_id_and_url(sources):
    assert (sources["source_id"].str.strip() != "").all()
    assert (sources["url"].str.strip() != "").all()


def test_unilorin_endpoints(unilorin):
    assert unilorin.loc[2020, "first_choice_applicants"] == 103582
    assert unilorin.loc[2026, "first_choice_applicants"] == 52514


def test_2022_not_established(unilorin):
    assert unilorin.loc[2022, "status"] == "not established"
    assert pd.isna(unilorin.loc[2022, "first_choice_applicants"])


def test_unilorin_2024_accepted(unilorin):
    row = unilorin.loc[2024]
    assert row["first_choice_applicants"] == 64143
    assert row["status"] == "accepted"
    assert row["sources"] == "S10;S11"


def test_nnamdi_azikiwe_2024_rank_consistent(panel):
    row = panel.loc[(2024, "Nnamdi Azikiwe University")]
    assert row["first_choice_applicants"] == 54495
    assert row["status"] == "rank-consistent"
