import pytest
import requests

import wikiviews.server as server


@pytest.mark.e2e
def test_most_viewed_week(client):
    response = client.get("/most-viewed/week-ending/2022-10-08")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    most_viewed = response.json["most_viewed"]
    assert most_viewed["start_date"] == "2022-10-01"
    assert most_viewed["end_date"] == "2022-10-08"
    for article in most_viewed["articles"]:
        assert isinstance(article["article"], str)
        assert isinstance(article["views"], int)


@pytest.mark.e2e
def test_most_viewed_month(client):
    response = client.get("/most-viewed/month-ending/2022-10-08")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    most_viewed = response.json["most_viewed"]
    assert most_viewed["start_date"] == "2022-09-08"
    assert most_viewed["end_date"] == "2022-10-08"
    for article in most_viewed["articles"]:
        assert isinstance(article["article"], str)
        assert isinstance(article["views"], int)


@pytest.mark.e2e
def test_article_views_week(client):
    response = client.get("/articles/Main_Page/views/week-ending/2022-10-08")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    views = response.json["article_views"]
    assert views["start_date"] == "2022-10-01"
    assert views["end_date"] == "2022-10-08"
    assert views["article"] == "Main_Page"
    assert isinstance(views["views"], int)


@pytest.mark.e2e
def test_article_views_month(client):
    response = client.get("/articles/Main_Page/views/month-ending/2022-10-08")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    views = response.json["article_views"]
    assert views["start_date"] == "2022-09-08"
    assert views["end_date"] == "2022-10-08"
    assert views["article"] == "Main_Page"
    assert isinstance(views["views"], int)


@pytest.mark.e2e
def test_bad_date(client):
    response = client.get("/articles/Main_Page/views/month-ending/20221004")
    assert response.status_code == 400
    assert response.json == {"error": {"msg": "Bad date string '20221004'"}}


@pytest.fixture
def app():
    return server.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
