import datetime

import pytest

import wikiviews.util as util


def test_parse_iso_date():
    assert util.parse_iso_date("2021-10-01") == datetime.date(2021, 10, 1)


def test_parse_bad_iso_date():
    with pytest.raises(util.BadDate):
        util.parse_iso_date("2021/01/01")


def test_iso_date():
    assert util.iso_date(datetime.date(2021, 10, 1)) == "2021-10-01"
