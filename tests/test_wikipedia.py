import datetime

import pytest
import requests

import wikiviews.models as models
import wikiviews.wikipedia as api


def test_get_most_viewed_on_date(mocker):
    response = mocker.create_autospec(requests.Response)
    response.json.return_value = {
        "items": [
            {
                "year": "2022",
                "month": "10",
                "day": "01",
                "articles": [
                    {
                        "article": "Bikes",
                        "views": 10,
                    },
                    {
                        "article": "Dogs",
                        "views": 5,
                    },
                ],
            },
        ],
    }
    get = mocker.patch("requests.get", return_value=response)
    date = datetime.date(2022, 10, 1)
    api.get_most_viewed_on_date.cache_clear()
    most_viewed_1 = api.get_most_viewed_on_date(
        project="en.wikipedia",
        date=date,
    )
    most_viewed_2 = api.get_most_viewed_on_date(
        project="en.wikipedia",
        date=date,
    )
    assert most_viewed_1 == most_viewed_2 == [
        models.ArticleDayViews(
            article="Bikes",
            date=date,
            page_views=10,
        ),
        models.ArticleDayViews(
            article="Dogs",
            date=date,
            page_views=5,
        ),
    ]
    get.assert_called_once_with(
        f"{api.BASE_URL}/top/en.wikipedia/all-access/2022/10/01",
        headers={"User-Agent": api.USER_AGENT},
    )


def test_http_error(mocker):
    response = mocker.create_autospec(requests.Response)
    response.raise_for_status.side_effect = requests.exceptions.HTTPError
    get = mocker.patch("requests.get", return_value=response)


    date = datetime.date(2022, 10, 1)
    api.get_most_viewed_on_date(
        project="en.wikipedia",
        date=date,
    )
    api.get_most_viewed_on_date.cache_clear()
    with pytest.raises(api.WikiHTTPError):
        api.get_most_viewed_on_date(
            project="en.wikipedia",
            date=date,
        )
    get.assert_called_once_with(
        f"{api.BASE_URL}/top/en.wikipedia/all-access/2022/10/01",
        headers={"User-Agent": api.USER_AGENT},
    )


def test_parse_error(mocker):
    response = mocker.create_autospec(requests.Response)
    response.json.return_value = {
        "items": [
            {
                "year": "2022",
                "month": "10",
                "day": "01",
                "articles": [
                    {
                        "_article": "Bikes",
                        "_views": 10,
                    },
                ],
            },
        ],
    }
    get = mocker.patch("requests.get", return_value=response)
    date = datetime.date(2022, 10, 1)
    api.get_most_viewed_on_date.cache_clear()
    with pytest.raises(api.WikiParseError):
        api.get_most_viewed_on_date(
            project="en.wikipedia",
            date=date,
        )
    get.assert_called_once_with(
        f"{api.BASE_URL}/top/en.wikipedia/all-access/2022/10/01",
        headers={"User-Agent": api.USER_AGENT},
    )
