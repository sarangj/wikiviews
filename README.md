# Wikiviews API

A simple API to do some basic data aggregation around wikipedia page views

## API Docs

The API is read-only and thus, all below resources only support GET. Additionally, all data will be returned as JSON

All instances of the `date` parameter require an ISO style date stamp (e.g., '2022-10-01'). Any other format will result in a
400.

## Endpoints

### Most views per week

  - '/most-viewed/week-ending/<date>'

Returns a sorted list of articles by page view in the last week (as determined by the given date).

  - Success: 200
  ```json
  {
    "most_viewed": {
      "start_date": <date>,
      "end_date": <date>,
      "articles": [
        {
          "article": <str>,
          "views": <int>
        }
      ]
    }
  }

  ```

### Most views per month

  - '/most-viewed/month-ending/<date>'

Returns a sorted list of articles by page view in the last month (as determined by the given date).

  - Success: 200
  ```json
  {
    "most_viewed": {
      "start_date": <date>,
      "end_date": <date>,
      "articles": [
        {
          "article": <str>,
          "views": <int>
        }
      ]
    }
  }

  ```

### Article views per week

  - '/articles/<article>/views/week-ending/<date>'

Returns the number of views for the given article in the last week (as determined by the given date).

  - Success: 200
  ```json
  {
    "article_views": {
      "start_date": <date>,
      "end_date": <date>,
      "article": <str>,
      "views": <int>
    }
  }

  ```

### Article views per month

  - '/articles/<article>/views/month-ending/<date>'

Returns the number of views for the given article in the last month (as determined by the given date).

  - Success: 200
  ```json
  {
    "article_views": {
      "start_date": <date>,
      "end_date": <date>,
      "article": <str>,
      "views": <int>
    }
  }

  ```

## Development

To run locally for testing and dev, first clone the repo and [install poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

To run the server locally, run `. local.sh` as provided in the repo.

Similarly, to run tests, run the provided `unit.sh` and `e2e.sh` for unit and end to end tests, respectively (the end to end
tests will be pretty slow).

## Improvements

Some things I didn't have time for

  - Replace in memory cache with something better (e.g. Redis, or even PostgreSQL)
  - Fetch data from the API in the background and just use the cache
  - add a linter
  - Maybe use threads or asyncio to speed up the bits where we're making a bunch of HTTP calls in a loop
  - Consider OpenAPI for the docs
  - Consider Pydantic or something for JSON slinging
