import datetime
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Peak:
    time: str
    percentage: float


@dataclass
class Summary:
    last_updated_at: datetime.datetime
    peak_demand: Peak
    peak_usage: Peak


CACHED_DATA: Optional[Summary] = None
CSV_DATA_URL = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"
TZ_JAPAN_STANDARD_TIME = datetime.timezone(datetime.timedelta(seconds=60 * 60 * 9))


def fetch_latest_data() -> Summary:
    response = requests.get(CSV_DATA_URL)
    response.encoding = "Shift_JIS"
    text = response.text
    lines = text.split("\r\n")
    last_updated_at_string = lines[0].replace(" UPDATE", " JST")
    last_updated_at = datetime.datetime.strptime(
        last_updated_at_string, "%Y/%m/%d %H:%M %Z"
    )
    peak_demand_line_values = lines[2].split(",")
    peak_usage_line_values = lines[8].split(",")
    latest = Summary(
        last_updated_at=last_updated_at,
        peak_demand=Peak(
            time=peak_demand_line_values[1],
            percentage=float(peak_demand_line_values[5]),
        ),
        peak_usage=Peak(
            time=peak_usage_line_values[1], percentage=float(peak_usage_line_values[5])
        ),
    )
    global CACHED_DATA
    CACHED_DATA = latest
    return latest


def load_latest_data():
    if CACHED_DATA is None:
        return fetch_latest_data()
    now = datetime.datetime.now(tz=TZ_JAPAN_STANDARD_TIME)
    if now.timestamp() - CACHED_DATA.last_updated_at.timestamp() > 60 * 5:
        return fetch_latest_data()
    return CACHED_DATA


if __name__ == "__main__":
    print(load_latest_data())
    print(load_latest_data())
