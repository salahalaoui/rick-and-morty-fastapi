import random
import string
from typing import Dict
from fastapi.testclient import TestClient
from datetime import date, datetime, timedelta
from app.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_date() -> date:
    start_date = date(2000, 1, 1)
    end_date = date(2020, 2, 1)

    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    return datetime.combine(start_date + timedelta(days=random_number_of_days), datetime.min.time())
