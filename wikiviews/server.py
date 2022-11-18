import collections
import datetime

import dateutil.relativedelta as delt
import flask

import wikiviews.wikipedia as api

_PROJECT = "en.wikipedia"

app = flask.Flask(__name__)


@app.route('/')
def hello():
    return f'Hello there'


@app.route('/most-viewed/week-ending/<date>')
def get_most_viewed_in_week_ending(date: str):
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        flask.abort(400, description="Invalid date string")

    start = date - delt.relativedelta(weeks=+1)
    views = get_most_viewed_between_dates(
        start=start,
        end=date,
    )
    return success(
        {
            "most_viewed": {
                "start_date": start,
                "end_date": date,
                "articles": views,
            },
        },
    )


@app.route('/most-viewed/month-ending/<date>')
def get_most_viewed_in_month_ending(date: str):
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        flask.abort(400, description="Invalid date string")

    start = date - delt.relativedelta(months=+1)
    views = get_most_viewed_between_dates(
        start=start,
        end=date,
    )
    return success(
        {
            "most_viewed": {
                "start_date": start,
                "end_date": date,
                "articles": views,
            },
        },
    )


def success(data) -> flask.Response:
    data = flask.jsonify(data)
    response = app.make_response(data)
    response.mime_type = "application/json"
    return response


def get_most_viewed_between_dates(start: datetime.date, end: datetime.date):
    # Build a map of article to page count
    results = collections.defaultdict(int)
    for i in range((end-start).days):
        most_viewed = api.get_most_viewed_on_date(_PROJECT, start + datetime.timedelta(days=i))
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
