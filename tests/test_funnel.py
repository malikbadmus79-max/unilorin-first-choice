import pytest

from first_choice import funnel


@pytest.fixture(scope="module")
def tables():
    return funnel.build_all()


@pytest.fixture(scope="module")
def index(tables):
    return tables[funnel.SCREENING_INDEX].set_index("utme_year")


@pytest.fixture(scope="module")
def share(tables):
    return tables[funnel.SHARE_180PLUS].set_index("utme_year")


@pytest.mark.parametrize("year, expected", [(2020, 11.4), (2021, 10.8), (2024, 3.6)])
def test_screening_index(index, year, expected):
    assert round(index.loc[year, "index"], 1) == expected


@pytest.mark.parametrize("year, expected", [(2020, 9.2), (2021, 8.7)])
def test_share_of_national_180plus(share, year, expected):
    assert round(share.loc[year, "share_pct"], 1) == expected


def test_every_funnel_row_has_a_source(tables):
    rows = tables[funnel.FUNNEL_BY_YEAR]
    assert list(rows["utme_year"]) == list(funnel.YEARS)
    assert (rows["sources"].str.strip() != "").all()
