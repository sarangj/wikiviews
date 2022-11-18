import collections
import datetime

import dateutil.relativedelta as delt
import flask

import wikiviews.responses as responses
import wikiviews.wiki_aggregator as aggregator
import wikiviews.wikipedia as api
import wikiviews.util as util

_PROJECT = "en.wikipedia"

app = flask.Flask(__name__)


@app.route('/')
def hello():
    return f'Hello there'


@app.route('/most-viewed/week-ending/<date>')
def get_most_viewed_in_week_ending(date: str):
    date = util.parse_iso_date(date)

    start = date - delt.relativedelta(weeks=+1)
    views = get_most_viewed_between_dates(
        start=start,
        end=date,
    )
    return responses.most_viewed(
        app=app,
        start=start,
        end=date,
        views=views,
    )


@app.route('/most-viewed/month-ending/<date>')
def get_most_viewed_in_month_ending(date: str):
    date = util.parse_iso_date(date)
    start = date - delt.relativedelta(months=+1)
    views = get_most_viewed_between_dates(
        start=start,
        end=date,
    )
    return responses.most_viewed(
        app=app,
        start=start,
        end=date,
        views=views,
    )

@app.route('/articles/<article>/views/month-ending/<date>')
def get_article_views_in_month_ending(article: str, date: str):
    date = util.parse_iso_date(date)
    start = date - delt.relativedelta(months=+1)
    num_views = get_article_view_num_between_dates(
        article=article,
        start=start,
        end=date,
    )

    return responses.article_views(
        app=app,
        article=article,
        start=start,
        end=date,
        views=num_views,
    )


@app.route('/articles/<article>/views/week-ending/<date>')
def get_article_views_in_week_ending(article: str, date: str):
    date = util.parse_iso_date(date)
    start = date - delt.relativedelta(weeks=+1)
    num_views = get_article_view_num_between_dates(
        article=article,
        start=start,
        end=date,
    )

    return responses.article_views(
        app=app,
        article=article,
        start=start,
        end=date,
        views=num_views,
    )


@app.errorhandler(util.BadDate)
def handle_bad_date(e):
    return responses.error(
        app=app,
        status_code=400,
        msg=f"Bad date string '{e.s}'",
    )


@app.errorhandler(api.WikiError)
def handle_wiki_error(_e):
    return responses.error(
        app=app,
        status_code=500,
        msg="Couldn't talk to Wikipedia",
    )


def get_most_viewed_between_dates(start: datetime.date, end: datetime.date) -> list[dict]:
    # Build a map of article to page count
    results = collections.defaultdict(int)
    most_viewed_by_day = aggregator.iter_page_views_between(
        _PROJECT,
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
    article: str,
    start: datetime.date,
    end: datetime.date,
) -> int:

    most_viewed_by_day = aggregator.iter_page_views_between(
        _PROJECT,
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
