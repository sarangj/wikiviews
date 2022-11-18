import dataclasses
import datetime


@dataclasses.dataclass
class ArticleDayViews:

    article: str
    date: datetime.date
    page_views: int
