import collections
import datetime
import typing as t

import wikiviews.wikipedia as api
import wikiviews.models as models


def get_most_viewed_between_dates(
    project: str,
    start: datetime.date,
    end: datetime.date,
) -> list[dict]:
    # Build a map of article to page count
    results = collections.defaultdict(int)
    most_viewed_by_day = iter_page_views_between(
        project,
        start,
        end,
    )
    for day, most_viewed in most_viewed_by_day:
        for article in most_viewed:
            results[article.article] += article.page_views

    results = dict(results)

    return sorted(
        (
            {
                "article": article,
                "views": views,
            }
            for article, views in results.items()
        ),
        key=lambda item: item["views"],
        reverse=True,
    )


def get_article_view_num_between_dates(
    project: str,
    article: str,
    start: datetime.date,
    end: datetime.date,
) -> int:
    most_viewed_by_day = iter_page_views_between(
        project,
        start,
        end,
    )
    num_views = 0
    for _, most_viewed in most_viewed_by_day:
        num_views += next(
            (
                adv.page_views for adv in most_viewed
                if adv.article == article
            ),
            0,
        )

    return num_views


def iter_page_views_between(
    project: str,
    start: datetime.date,
    end: datetime.date,
) -> t.Iterator[t.Tuple[datetime.date, list[models.ArticleDayViews]]]:
    """Convenience wrapper to return API results per date in a range"""
    for i in range((end-start).days + 1):
        date = start + datetime.timedelta(days=i)
        most_viewed = api.get_most_viewed_on_date(
            project,
            date,
        )
        yield (
            date,
            most_viewed
        )
