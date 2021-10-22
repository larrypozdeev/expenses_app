from datetime import date, timedelta
from typing import Tuple


def get_month_days(
    month: int = date.today().month, year: int = date.today().year
) -> tuple:
    """Gets first and last dates of a month based on it's number.
    By default returns of a current month.

    Args:
        month (int, optional): Month of required date.
        year (int, optional): Year of required date.
    Returns:
        tuple: date of first day, date of last day
    """
    if month is None:
        month = date.today().month
    if year is None:
        year = date.today().year

    first_day = date(year=year, month=month, day=1)
    next_month = date(year=year, month=month + 1, day=1)
    last_day = next_month - timedelta(days=next_month.day)
    return (first_day, last_day)
