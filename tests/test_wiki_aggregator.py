import datetime

import pytest

import wikiviews.models as models
import wikiviews.wiki_aggregator as aggregator

_START = datetime.date(2022, 10, 1)
_END = datetime.date(2022, 10, 5)


def test_get_most_viewed_between_dates(_api):
    assert aggregator.get_most_viewed_between_dates(
        "en.wikipedia",
        _START,
        _END,
    ) == [
        {
            "article": "Bikes",
            "views": 15,
        },
        {
            "article": "Dogs",
            "views": 10,
        },
    ]


def test_get_article_view_num_between_dates(_api):
    assert aggregator.get_article_view_num_between_dates(
        "en.wikipedia",
        "Bikes",
        _START,
        _END,
    ) == 15


@pytest.fixture
def _api(mocker):
    test_data = {
        _START: [
            models.ArticleDayViews(
                article="Dogs",
                date=_START,
                page_views=10,
            ),
            models.ArticleDayViews(
                article="Bikes",
                date=_START,
                page_views=10,
            ),
        ],
        _END: [
            models.ArticleDayViews(
                article="Bikes",
                date=_END,
                page_views=5,
            ),
        ],
    }
    def _get_most_viewed(_p, date):
        return test_data.get(date, {})

    mocker.patch(
        "wikiviews.wikipedia.get_most_viewed_on_date",
        side_effect=_get_most_viewed,
    )
    yield _get_most_viewed
