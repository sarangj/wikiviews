import dataclasses
import datetime
import functools

import requests

import wikiviews.models as models

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews"

# See https://meta.wikimedia.org/wiki/User-Agent_policy
# Might wanna make this an env var
USER_AGENT = (
    "Sarang Joshi (sarangjoshi22@gmail.com); "
    "https://github.com/sarangj/"
)


@functools.cache
def get_most_viewed_on_date(
    project: str,
    date: datetime.date,
) -> list[models.ArticleDayViews]:
    url = (
        f"{BASE_URL}/top/{project}/all-access/"
        f"{date.year}/{date.strftime('%m')}/{date.strftime('%d')}"
    )
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise WikiHTTPError()

    payload = response.json()
    try:
        return format_most_viewed(payload)
    # This could be more granular
    except Exception:
        raise WikiParseError()


def format_most_viewed(payload) -> list[models.ArticleDayViews]:
    # Everything is in a singleton list for some reason
    items = payload["items"][0]
    date = datetime.date(
        int(items["year"]),
        int(items["month"]),
        int(items["day"]),
    )
    return [
        models.ArticleDayViews(
            article=article["article"],
            date=date,
            page_views=article["views"],
        )
        for article in items["articles"]
    ]


class WikiError(Exception):
    pass


class WikiHTTPError(WikiError):
    pass


class WikiParseError(WikiError):
    pass

