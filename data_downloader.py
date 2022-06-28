import datetime
from dataclasses import dataclass
from typing import Optional, Sequence

import requests


@dataclass
class Usage:
    time: str
    percentage: float


@dataclass
class Summary:
    last_updated_at: datetime.datetime
    demand_peak: Usage
    usage_peak: Usage
    current: Usage


CSV_DATA_URL = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"
TZ_JAPAN_STANDARD_TIME = datetime.timezone(datetime.timedelta(seconds=60 * 60 * 9))

# When you run this app on AWS Lambda, this cache does not work
CACHED_DATA: Optional[Summary] = None


def fetch_latest_data() -> Summary:
    response = requests.get(CSV_DATA_URL)
    response.encoding = "Shift_JIS"
    text = response.text
    lines = text.split("\r\n")
    last_updated_at_string = lines[0].replace(" UPDATE", " +0900")
    last_updated_at = datetime.datetime.strptime(
        last_updated_at_string, "%Y/%m/%d %H:%M %z"
    )
    demand_peak_line_values = lines[2].split(",")
    usage_peak_line_values = lines[8].split(",")
    current: Optional[Usage] = None
    for i in range(14, 28):
        line_values = lines[i].split(",")
        if len(line_values[4]) == 0:
            break
        hour = int(line_values[1].split(":")[0])
        time = line_values[1] + "〜" + str(hour + 1) + ":00"
        current = Usage(time=time, percentage=float(line_values[4]))

    latest = Summary(
        last_updated_at=last_updated_at,
        demand_peak=Usage(
            time=demand_peak_line_values[1],
            percentage=float(demand_peak_line_values[5]),
        ),
        usage_peak=Usage(
            time=usage_peak_line_values[1], percentage=float(usage_peak_line_values[5])
        ),
        current=current,
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
