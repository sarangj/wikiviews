import datetime
import typing as t

import wikiviews.wikipedia as api
import wikiviews.models as models


def iter_page_views_between(
    project: str,
    start: datetime.date,
    end: datetime.date,

) -> t.Iterator[t.Tuple[datetime.date, list[models.ArticleDayViews]]]:
    """Convenience wrapper to return API results per date in a range"""
    for i in range((end-start).days):
        date = start + datetime.timedelta(days=i)
        most_viewed = api.get_most_viewed_on_date(
            project,
            date,
        )
        yield (
            date,
            most_viewed
        )
