import datetime
import os
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Usage:
    time: str
    percentage: float


@dataclass
class Weather:
    weather: str
    temperature: float
    feels_like: float
    humidity: float


@dataclass
class Summary:
    last_updated_at: datetime.datetime
    current_usage: Usage
    demand_peak_usage: Usage
    usage_peak_usage: Usage
    weather: Optional[Weather]


WEATHER_URL: Optional[str] = None
OPEN_WEATHER_MAP_API_KEY = os.environ.get("OPEN_WEATHER_MAP_API_KEY")
if OPEN_WEATHER_MAP_API_KEY is not None:
    WEATHER_URL = (
        "https://api.openweathermap.org/data/2.5/weather?"
        "lat=35.6853482&"
        "lon=139.7457665&"
        "units=metric&"
        f"appid={OPEN_WEATHER_MAP_API_KEY}"
    )

TEPCO_CSV_DATA_URL = "https://www.tepco.co.jp/forecast/html/images/juyo-d1-j.csv"
TZ_JAPAN_STANDARD_TIME = datetime.timezone(datetime.timedelta(seconds=60 * 60 * 9))

# When you run this app on AWS Lambda, this cache does not work
CACHED_DATA: Optional[Summary] = None


def fetch_latest_data() -> Summary:
    response = requests.get(TEPCO_CSV_DATA_URL)
    response.encoding = "Shift_JIS"
    text = response.text
    lines = text.split("\r\n")
    last_updated_at_string = lines[0].replace(" UPDATE", " +0900")
    last_updated_at = datetime.datetime.strptime(
        last_updated_at_string, "%Y/%m/%d %H:%M %z"
    )
    demand_peak_line_values = lines[2].split(",")
    usage_peak_line_values = lines[8].split(",")
    current: Usage = Usage(time="-", percentage=0)
    for i in range(14, 38):
        line_values = lines[i].split(",")
        if len(line_values[4]) == 0:
            break
        hour = int(line_values[1].split(":")[0])
        time = line_values[1] + "〜" + str(hour + 1) + ":00"
        current = Usage(time=time, percentage=float(line_values[4]))

    weather: Optional[Weather] = None
    if WEATHER_URL is not None:
        weather_response = requests.get(WEATHER_URL)
        weather_data = weather_response.json()
        weather = Weather(
            weather=weather_data.get("weather")[0].get("main"),
            temperature=weather_data.get("main", {}).get("temp"),
            feels_like=weather_data.get("main", {}).get("feels_like"),
            humidity=weather_data.get("main", {}).get("humidity"),
        )

    latest = Summary(
        last_updated_at=last_updated_at,
        current_usage=current,
        demand_peak_usage=Usage(
            time=demand_peak_line_values[1],
            percentage=float(demand_peak_line_values[5]),
        ),
        usage_peak_usage=Usage(
            time=usage_peak_line_values[1], percentage=float(usage_peak_line_values[5])
        ),
        weather=weather,
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
