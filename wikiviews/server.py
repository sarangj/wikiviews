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
    views = aggregator.get_most_viewed_between_dates(
        project=_PROJECT,
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
    views = aggregator.get_most_viewed_between_dates(
        project=_PROJECT,
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
    num_views = aggregator.get_article_view_num_between_dates(
        project=_PROJECT,
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
    num_views = aggregator.get_article_view_num_between_dates(
        project=_PROJECT,
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
