import pandas as pd
import requests
import pickle
import datetime
from matplotlib import pyplot as plt
from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import HistGradientBoostingRegressor


URL = "https://api.open-meteo.com/v1/forecast"
hourly = ["dewpoint_2m", "precipitation","pressure_msl","cloudcover","windspeed_10m","winddirection_10m", "temperature_2m"]
meters = ["electricity", "chilledwater", "steam", "hotwater"]
fields = ["primary_use_ordinal", "square_feet", "year_built", "floor_count", "air_temperature", "cloud_coverage", "dew_temperature",
"precip_depth_1_hr", "sea_level_pressure", "wind_speed", "day_of_week", "month", "day", "hour"]

conversion_dict = {
    "time": "timestamp",
    "temperature_2m": "air_temperature",
    "cloudcover": "cloud_coverage",
    "dewpoint_2m": "dew_temperature",
    "precipitation": "precip_depth_1_hr",
    "pressure_msl": "sea_level_pressure",
    "windspeed_10m": "wind_speed",
    "winddirection_10m": "wind_direction",
}

with open('models.pickle', 'rb') as f:
    models: list[HistGradientBoostingRegressor] = pickle.load(f)

with open('encoder.pickle', 'rb') as f:
    encoder: OrdinalEncoder = pickle.load(f)

def get_historical_weather(lat, long, days=1):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=days)
    params = dict(
        latitude=lat,
        longitude=long,
        hourly=",".join(hourly),
        windspeed_unit="ms",
        timeformat="unixtime",
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
    )
    param_str = "&".join(f"{k}={v}" for k, v in params.items())
    res = requests.get(f"{URL}?{param_str}")
    res.raise_for_status()
    res_json = res.json()
    df = pd.DataFrame(res_json["hourly"])
    print(df.columns)
    df.rename(columns=conversion_dict, inplace=True)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit="s")
    return df


def get_historical_predictions():
    df = get_historical_weather(33.77,  -84.3956)
    primary_use = ""
    square_feet = 7432
    year_built = 12344
    floor_count = 1
    df["day_of_week"] = df["timestamp"].dt.day_of_week
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month
    df["hour"] = df["timestamp"].dt.hour    
    print(df.head())
