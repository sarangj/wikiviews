import datetime


class BadDate(Exception):

    def __init__(self, s: str):
        self.s = s


def parse_iso_date(s: str) -> datetime.date:
    try:
        dt = datetime.datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        raise BadDate(s)

    return dt.date()


def iso_date(date: datetime.date) -> str:
    return date.strftime("%Y-%m-%d")
