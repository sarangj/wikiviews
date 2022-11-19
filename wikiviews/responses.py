import datetime

import flask

import wikiviews.util as util


def most_viewed(
    app: flask.Flask,
    start: datetime.date,
    end: datetime.date,
    views: list[dict],
) -> flask.Response:
    payload = {
        "most_viewed": {
            "start_date": util.iso_date(start),
            "end_date": util.iso_date(end),
            "articles": views,
        },
    }
    return success(app, payload)


def article_views(
    app: flask.Flask,
    article: str,
    start: datetime.date,
    end: datetime.date,
    views: int,
) -> flask.Response:
    payload = {
        "article_views": {
            "article": article,
            "start_date": util.iso_date(start),
            "end_date": util.iso_date(end),
            "views": views,
        },
    }
    return success(app, payload)


def success(app, data) -> flask.Response:
    data = flask.jsonify(data)
    response = app.make_response(data)
    response.content_type = "application/json"
    return response


def error(app, status_code: int, msg: str) -> flask.Response:
    data = flask.jsonify({"error": {"msg": msg}})
    response = app.make_response(data)
    response.content_type = "application/json"
    response.status = status_code
    return response
